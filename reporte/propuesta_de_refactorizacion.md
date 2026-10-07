# Diagnóstico de *code smells* — "La Esquina"

## Panorama general

- **429 líneas en 4 módulos, 20 errores de ruff y 20 tests que pasan.**
- **El problema más grave no lo marca ruff:** la lógica de precios (descuentos e IVA) está **copiada en dos lugares**.
- **Los tests no cubren todo.** Nadie verifica el texto del ticket, el reporte de ventas ni el menú. Un cambio podría alterar esa salida sin que ningún test falle, así que hay que tener cuidado extra ahí.
- **Algunos patrones de diseño no se pueden cambiar sin romper el contrato.** Por ejemplo, devolver `False`/`None` y guardar el error en una variable global. Se mencionan, pero quedan fuera de alcance.

## Resumen priorizado

| # | *Code smell* | Dónde | Errores de ruff | Prioridad |
|---|---|---|---|---|
| 1 | Función gigante con muchas responsabilidades | `gestor.registrar_venta` | C901, 3× SIM102, SIM108 | 🔴 Alta |
| 2 | Lógica duplicada (precios) | `registrar_venta` / `cotizar` | — | 🔴 Alta |
| 3 | Números mágicos | `gestor`, `reportes` | — | 🔴 Alta |
| 4 | Función gigante (menú) | `main.menu` | C901, I001 | 🟠 Media-alta |
| 5 | Archivos abiertos sin `with` y `except` demasiado amplio | `almacen`, `reportes` | 3× SIM115, UP015 | 🟠 Media-alta |
| 6 | Código muerto | `gestor`, `reportes` | F401, N802 | 🟠 Media |
| 7 | Nombres crípticos y estilos mezclados | todos | N802, N816, SIM103 | 🟡 Media |
| 8 | Estado global modificado desde otros módulos | `almacen` → `gestor` | — | 🟡 Media |
| 9 | Reinventar la rueda (burbuja, contadores manuales) | `reportes` | — | 🟡 Media-baja |
| 10 | Lógica mezclada con `print` | `reportes` | — | 🟢 Baja |
| 11 | Sin type hints, docstrings incompletos | todos | — | 🟢 Baja |
| 12 | Detalles triviales (encoding, orden de imports) | todos | 4× UP009 | ⚪ Trivial |

---

## Detalle de cada problema

### 1. 🔴 `registrar_venta` hace demasiado ([gestor.py:86-161](../src/gestor.py#L86-L161))

**Qué pasa:** son 75 líneas que validan los datos, calculan descuentos, calculan el IVA, descuentan stock, generan el folio, arman el ticket en texto y guardan la venta. La propia docstring lo admite: *"Esta función hace de todo"*.

Además, la validación usa **código flecha**: `if` dentro de `if` dentro de `if`, con los `else` muy lejos de su condición ([gestor.py:96-112](../src/gestor.py#L96-L112)):

```python
if codigo is not None and codigo != "":
    if codigo in INVENTARIO:
        if cantidad is not None and cantidad > 0:
            if INVENTARIO[codigo]["stock"] >= cantidad:
                ...
            else:
                ultimo_error = "stock insuficiente"   # ¿de cuál if era este else?
```

**Por qué importa:** imagina que te piden cambiar solo el formato del ticket. Tienes que leer 75 líneas para encontrar las 10 que te importan, y cualquier error puede romper el cálculo del cobro, que está a unas líneas de distancia. El principio que se viola es el de **responsabilidad única**: cada función debe tener una sola razón para cambiar. El anidamiento obliga a llevar en la cabeza cuatro condiciones a la vez.

**Solución:** usar **cláusulas de guarda**, es decir, validar y salir temprano:

```python
if not codigo:
    ultimo_error = "codigo vacio"
    return None
if codigo not in INVENTARIO:
    ...
```

Después, extraer funciones: `_validar_venta()`, `_calcular_precios()` y `_armar_ticket()`.

⚠️ **Hay que cuidar el orden de las validaciones.** Hoy es: código vacío → no existe → cantidad inválida → stock insuficiente. Ese orden decide qué mensaje de error se ve cuando fallan varias cosas a la vez.

### 2. 🔴 Lógica de precios duplicada ([gestor.py:114-133](../src/gestor.py#L114-L133) y [gestor.py:173-182](../src/gestor.py#L173-L182))

**Qué pasa:** `cotizar` copia el cálculo de descuentos y de IVA de `registrar_venta`.

**Por qué importa:** si mañana el IVA cambia o se agrega un descuento, alguien lo cambia en un lugar y olvida el otro. La cotización dejaría de coincidir con el cobro real y el cliente vería un precio y pagaría otro. Es el principio **DRY** (*Don't Repeat Yourself*): cada regla de negocio debe vivir en un solo lugar.

**Solución:** extraer una función, por ejemplo `calcular_descuento_por_volumen(subtotal)`, y que ambas la usen.

⚠️ **Posible bug, no se arregla:** `cotizar` **no aplica el descuento VIP**. Para un cliente VIP, la cotización y el cobro real son distintos. Como en `CLAUDE.md` quedó que los bugs se documentan y se consultan, la refactorización debe conservar esa diferencia.

### 3. 🔴 Números mágicos

**Qué pasa:** aparecen `1000`, `500`, `0.10`, `0.05`, `0.16`, `"VIP"`, `200`, `0.02` en [gestor.py](../src/gestor.py), y `5` dos veces en [reportes.py:18](../src/reportes.py#L18) y [reportes.py:31](../src/reportes.py#L31).

**Por qué importa:** ¿qué significa `0.16`? Quien conoce el IVA de México lo sabe, pero el código no lo dice. Y el umbral de stock bajo (`5`) está repetido. Si el negocio decide que bajo es menos de 10 y solo se cambia uno, el reporte marca "STOCK BAJO" en productos que la alerta no muestra. Una constante con nombre como `TASA_IVA = 0.16` **documenta** el valor y garantiza que se cambie en un solo lugar.

### 4. 🟠 `menu()` tiene complejidad 17 ([main.py:21-80](../src/main.py#L21-L80))

**Qué pasa:** es una cadena de 8 `elif`, y cada uno tiene su propia lógica de `input`/`print`. Ruff permite una complejidad máxima de 10.

**Por qué importa:** la **complejidad ciclomática** cuenta cuántos caminos distintos tiene una función. 17 caminos significan 17 casos que habría que probar y mucho que leer para agregar una opción nueva.

**Solución:** una función por opción (`_opcion_agregar_producto()`, `_opcion_registrar_venta()`…) y un diccionario que asocie cada opción con su función:

```python
ACCIONES = {"1": _opcion_agregar_producto, "2": _opcion_registrar_venta, ...}
```

⚠️ Los tests no cubren el menú, así que hay que conservar exactamente los textos y probarlo a mano.

### 5. 🟠 Archivos sin `with` y `except Exception` ([almacen.py:16-37](../src/almacen.py#L16-L37))

**Qué pasa:** se usa `f = open(...)` con `f.close()` manual.

**Por qué importa:** si ocurre un error entre el `open` y el `close`, el archivo **queda abierto**. Por ejemplo, si `json.dump` falla con un dato que no se puede convertir, se escapa la excepción y nunca se llega al `close`. Con `with`, Python lo cierra **siempre**, haya error o no. Es la forma idiomática y segura.

**Bonus:** `except Exception` atrapa **cualquier** error, incluidos bugs del programador (un error de dedo en un nombre de variable se reportaría como "archivo corrupto"). Lo correcto es atrapar solo lo esperado (`json.JSONDecodeError` / `ValueError`).

⚠️ El cambio a `with` es seguro. Al reducir el `except` hay que confirmar qué errores de lectura atrapa hoy, para no cambiar el comportamiento.

### 6. 🟠 Código muerto

- `calcular_descuento_viejo` ([gestor.py:185-190](../src/gestor.py#L185-L190)): *"ya nadie la llama"*.
- `exportar_txt`, comentado ([gestor.py:193-198](../src/gestor.py#L193-L198)).
- `reporteViejoCSV` ([reportes.py:83-92](../src/reportes.py#L83-L92)): *"ya no se usa"*. Además genera 2 errores de ruff.
- `MODO_DEBUG` ([gestor.py:17](../src/gestor.py#L17)): nunca se usa.
- `import os` en [reportes.py:4](../src/reportes.py#L4): nunca se usa.

**Por qué importa:** el código muerto confunde. Un nuevo programador no sabe si `calcular_descuento_viejo` se usa y pierde tiempo investigando, o peor, la usa por error. *"Por si acaso"* no es razón para conservarlo: **para eso existe git**. Si algún día se necesita, está en el historial.

### 7. 🟡 Nombres crípticos y estilos mezclados

| Actual | Problema | Propuesta |
|---|---|---|
| `hacer_cosa(v)` | No dice qué hace (da formato de dinero) | `formatear_dinero(monto)` |
| `temp2`, `aux`, `x`, `d`, `t`, `s` | No dicen qué guardan | `producto`, `subtotal`, `venta`, `texto`… |
| `contadorVentas` | camelCase en un proyecto snake_case | `contador_ventas` |
| `hayArchivo` | camelCase, y su `if/else` es innecesario | `existe_archivo` → `return os.path.exists(ruta)` |

**Por qué importa:** el código se lee muchas más veces de las que se escribe. `aux - desc > 200` obliga a recordar qué es `aux`; `subtotal - descuento > MONTO_MINIMO_VIP` se entiende solo.

⚠️ **Trampa:** `contadorVentas` también se escribe desde [almacen.py:15](../src/almacen.py#L15) y [almacen.py:44](../src/almacen.py#L44), así que hay que renombrarlo en ambos módulos. `agregarProducto` y `buscarProducto` **no se tocan**.

### 8. 🟡 Estado global modificado desde fuera ([almacen.py:38-44](../src/almacen.py#L38-L44))

**Qué pasa:** `almacen` llena directamente `gestor.INVENTARIO` y `gestor.VENTAS` y asigna `gestor.contadorVentas` y `gestor.ultimo_error`.

**Por qué importa:** es como si otro departamento entrara a tu oficina y reacomodara tus archivos. Si `gestor` cambia cómo guarda sus datos, `almacen` se rompe sin aviso.

**Solución realista:** una función en `gestor`, por ejemplo `restaurar_estado(inventario, ventas, contador)`, para que solo `gestor` modifique su propio estado.

⚠️ **Riesgo alto si se exagera:** los tests leen `gestor.INVENTARIO` directamente, y `reiniciar_sistema` usa `.clear()` para conservar **el mismo objeto**. Si se reemplaza por `INVENTARIO = {}`, otros módulos quedarían apuntando al diccionario viejo. Convertir todo a clases **no** se recomienda en este reto.

### 9. 🟡 Reinventar la rueda ([reportes.py:48-66](../src/reportes.py#L48-L66))

**Qué pasa:** hay un **ordenamiento de burbuja** escrito a mano (el comentario dice *"TODO: algún día usar sorted"*) y un contador manual con `if in / else`.

**Por qué importa:** la burbuja es lenta (O(n²)), son 7 líneas propensas a errores y Python ya trae `sorted()`, que es probado y rápido:

```python
return sorted(unidades.items(), key=lambda par: par[1], reverse=True)[:n]
```

✅ Es equivalente: la burbuja solo intercambia cuando un elemento es estrictamente menor, así que es **estable**. `sorted(..., reverse=True)` también conserva el orden original de los empates.

Otros casos del mismo tipo: `x = {}; x["codigo"] = ...` puede ser un diccionario literal, y los `for` que suman pueden ser `sum(...)`.

### 10. 🟢 Lógica mezclada con `print` ([reportes.py:36](../src/reportes.py#L36), [reportes.py:79](../src/reportes.py#L79))

**Qué pasa:** `reporte_inventario` y `resumen_ventas` arman el texto **y además** lo imprimen.

**Por qué importa:** no se puede reutilizar el reporte (mandarlo por correo, guardarlo) sin que salga en la consola. Lo ideal es que la función **devuelva** el texto y que `main` decida imprimirlo.

⚠️ Hoy el test llama a `reporte_inventario()`, y que imprima es parte del comportamiento actual. Si se separa, `main` tiene que seguir imprimiendo lo mismo.

### 11. 🟢 Sin type hints y docstrings incompletos

`agregarProducto`, `buscarProducto` y otras usan comentarios `#` en lugar de docstrings, y no hay anotaciones de tipo. Con `def cotizar(codigo: str, cantidad: int) -> float | None:` el editor avisa de errores y el código se documenta solo.

### 12. ⚪ Triviales

Las 4 líneas `# -*- coding: utf-8 -*-` sobran (UP009: Python 3 ya usa UTF-8) y los imports de `main` están desordenados (I001). `ruff --fix` los corrige, pero **no cuentan como refactorización significativa**. Conviene corregirlos dentro de la refactorización que toque cada archivo.

### Observaciones fuera de alcance (posibles bugs: documentar, no arreglar)

- `cotizar` ignora el descuento VIP (punto 2).
- El dinero se maneja con `float`. Lo correcto sería `Decimal`, pero cambiarlo alteraría redondeos y salidas.
- `pedir_numero` + `int()` trunca: si se capturan 2.7 unidades, se registran 2.
- `cargar_datos` truena con `KeyError` si el JSON es válido pero le falta `"inventario"`.
- Al correr `cd src && python main.py` no se cargan los datos de ejemplo, porque el archivo está en la raíz.
- El patrón de "devolver `False` y guardar el error en una variable global" debería ser excepciones, pero los tests exigen `False`/`None`.

---

## Plan de implementación recomendado

**Estrategia:** primero lo de **bajo riesgo**, para ganar confianza. Luego lo **más valioso** (precios y ventas) en pasos pequeños, y al final lo cosmético. Cada paso es un commit, con `pytest` y `ruff` antes de pedir el visto bueno.

| Paso | Refactorización | Errores de ruff que elimina | Riesgo |
|---|---|---|---|
| **R1** | Eliminar código muerto e imports sin usar | F401, N802, SIM115 (reportes) + UP009 → **4** | Bajo |
| **R2** | Reemplazar números mágicos por constantes | — | Bajo |
| **R3** | Extraer el cálculo de descuentos compartido (cotizar/venta) | SIM108 → **1** | Medio |
| **R4** | Dividir `registrar_venta`: guardas + `_armar_ticket` | C901, 3× SIM102 → **4** | Medio |
| **R5** | Dividir `menu()` en una función por opción | C901, I001, UP009 → **3** | Medio |
| **R6** | `with` en `almacen`, `except` específico, `existe_archivo` | 2× SIM115, UP015, N802, SIM103, UP009 → **6** | Bajo-medio |
| **R7** | Nombres descriptivos y `contador_ventas` | N816, UP009 → **2** | Medio |
| **R8** | Python idiomático en `reportes`: `sorted`, `sum`, literales | — | Bajo |
| *Opcional* | Type hints, `restaurar_estado()` en gestor | — | Bajo / Medio |

**Total: 4 + 1 + 4 + 3 + 6 + 2 = 20 errores → ruff en 0 al terminar R7.**

R1 a R7 ya son 7 refactorizaciones significativas, dos más que el mínimo.

### Cómo cuidar que los tests sigan pasando (y lo que no cubren)

1. **Red de seguridad extra.** Antes de R3 y R4 se propone un script **temporal, fuera del repo y fuera de `tests/`**. Captura el ticket completo, los reportes y las cotizaciones (incluido un cliente VIP) antes del cambio y los compara después. Así se detectan cambios de texto que los 20 tests no verían.
2. **Cuidado con los formatos de texto.** `str(23.2)` produce `"23.2"`. Si al pasar a f-strings se escribe `f"{v:.2f}"`, sale `"23.20"` y cambia el ticket. Usar `f"{v}"` es equivalente.
3. **No reemplazar `INVENTARIO`/`VENTAS` por objetos nuevos.** Hay que seguir usando `.clear()` y mutaciones.

### Recomendación para empezar: **R1 (código muerto)**

- Es de riesgo casi nulo: nada lo llama, y se comprobará con `grep`.
- Limpia el terreno: se elimina código que estorbaría en R2 a R4.
- Baja ruff de 20 a 16 errores de inmediato.
- Es fácil de justificar en la bitácora.
