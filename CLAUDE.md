# CLAUDE.md

Guía para Claude Code al trabajar en este repositorio.

## Objetivo del reto

Aplicación de consola en Python para administrar el inventario y las ventas de
una tienda pequeña ("La Esquina"): alta de productos, ventas con descuentos e
IVA, cotizaciones, alertas de stock bajo, reporte de más vendidos y persistencia
en JSON.

Las pruebas existentes pasan, pero el código contiene *code smells* a propósito.
El objetivo es mejorar su calidad **sin cambiar su comportamiento observable**.
No agregar funcionalidades ni corregir comportamientos extraños como parte de
una refactorización. Si se detecta un posible bug, documentarlo y consultarlo
con la usuaria antes de cambiarlo.

## Entorno y comandos

Ejecutar los comandos desde la raíz del repositorio y usar siempre el entorno
virtual `.venv` con Python 3.12:

```bash
source .venv/bin/activate
python --version
pytest
ruff check src
```

Referencia del código original: `pytest` → 20 passed;
`ruff check src` → 20 errores. Verificar los resultados reales antes de editar;
no asumir que coinciden con esta referencia ni inventar resultados.

Si `.venv` no existe o las herramientas no están disponibles, informar el
problema antes de modificar el entorno o instalar paquetes.

Para correcciones automáticas triviales, como imports:

```bash
ruff check src --fix
```

Usar `--fix` únicamente dentro del cambio en curso. Revisar todo el diff y
validar nuevamente; no mezclar correcciones ajenas a la refactorización.

La aplicación interactiva puede ejecutarse de forma opcional:

```bash
(cd src && python main.py)
```

Este comando busca `datos_ejemplo.json` en `src/`; como el archivo de ejemplo
está en la raíz, la aplicación inicia sin datos y al guardar crea
`src/datos_ejemplo.json`. No ejecutarlo sobre datos reales sin autorización. Para una comprobación manual, usar una
copia temporal de los datos y conservar el archivo original.

## Arquitectura actual

Todo el código fuente está en `src/`. No hay paquete: los módulos se importan
directamente entre sí. Los tests agregan `src/` al `sys.path` en `conftest.py`.

- **gestor.py**: lógica de negocio. Maneja el estado global (`INVENTARIO`,
  `VENTAS`, `contadorVentas`, `ultimo_error`), productos, ventas y cotizaciones.
- **almacen.py**: persistencia en JSON. Lee y escribe el estado de `gestor`.
- **reportes.py**: inventario, resumen de ventas, más vendidos y alertas de stock
  bajo. Lee el estado de `gestor`.
- **main.py**: menú interactivo y punto de entrada. Lee y guarda
  `datos_ejemplo.json` en el directorio de trabajo de la aplicación.

El estado global de `gestor.py` es el almacén central de datos. Otros módulos
lo leen y modifican directamente. Los tests lo reinician mediante
`gestor.reiniciar_sistema()` antes y después de cada prueba.

Esta sección describe la arquitectura inicial, no exige conservar todos sus
problemas. Cualquier mejora interna debe mantener la compatibilidad existente.

## API pública y contrato de comportamiento

Conservar estos nombres, sus firmas y sus tipos de retorno:

- `gestor`: `INVENTARIO`, `VENTAS`, `agregarProducto`, `buscarProducto`,
  `actualizar_stock`, `eliminar_producto`, `registrar_venta`, `cotizar`,
  `reiniciar_sistema`.
- `almacen`: `guardar_datos`, `cargar_datos`.
- `reportes`: `reporte_inventario`, `total_vendido`, `mas_vendidos`,
  `productos_stock_bajo`.

Preservar también:

- Valores devueltos, incluidos los casos de error y los valores `None`.
- Mensajes de error, texto de tickets y reportes, y salida de consola.
- Cálculos de IVA y descuentos, orden de operaciones y redondeos.
- Estructura de diccionarios y JSON, nombres de claves y tipos de datos.
- Orden de resultados cuando sea observable por los consumidores.
- Efectos sobre inventario, ventas, contadores y estado de errores.
- Excepciones y comportamiento de lectura y escritura de archivos.
- Acceso y modificación del estado compartido desde los módulos existentes.

Si se reduce el estado global, `gestor.INVENTARIO` y `gestor.VENTAS` deben seguir
siendo compatibles con sus consumidores. No basta con que los atributos
existan: preservar las referencias compartidas y las mutaciones observables
cuando el código dependa de ellas.

Las pruebas existentes son una parte del contrato, no una garantía de cobertura
completa. Revisar también el código afectado y sus consumidores.

## Reglas críticas

- **Nunca modificar archivos en `tests/`**, incluido `conftest.py`.
- **Nunca modificar `pyproject.toml`**.
- Conservar `agregarProducto` y `buscarProducto` en camelCase: los tests los
  usan y están permitidos en `ignore-names` de `pyproject.toml`.
- No silenciar Ruff mediante `# noqa`, cambios de reglas, exclusiones nuevas
  ni otras supresiones. Resolver los problemas en el código.
- No agregar dependencias nuevas.
- No hacer cambios masivos de formato, nombres o arquitectura sin relación
  con el problema elegido.
- No sobrescribir cambios previos de la usuaria ni revertirlos para limpiar
  el repositorio.
- No cambiar este documento para relajar las restricciones del reto.

## Inicio del trabajo

El repositorio ya está preparado: `main` contiene el código original (commit
`db27683`) y el trabajo se hace en la rama `refactorizacion`, que será el
origen del PR hacia `main`.

Al iniciar una sesión:

1. Revisar `git status` y confirmar que la rama actual es `refactorizacion`.
   No descartar cambios locales de la usuaria.
2. Ejecutar `pytest` y `ruff check src` para conocer el estado real. Si las
   pruebas fallan, detener las modificaciones y reportarlo.
3. Proponer la siguiente refactorización y explicar por qué conviene hacerla.

## Flujo por refactorización

1. Proponer **un solo cambio significativo**, identificar el *code smell* y
   explicar el beneficio, los archivos afectados y los riesgos para el contrato.
2. Aplicarlo sin mezclar otros cambios. Si requiere varios pasos, mantenerlos
   dentro del mismo objetivo.
3. Revisar el diff para comprobar que solo contiene el cambio previsto y que
   no modifica archivos protegidos.
4. Ejecutar toda la suite con `pytest` y ejecutar `ruff check src`.
5. Reportar los resultados reales: pruebas aprobadas o fallidas, errores de
   Ruff resueltos y pendientes. No introducir nuevos diagnósticos de Ruff;
   la meta final es **0 errores**. No exigir cero en cada paso si todavía
   existen errores de la línea base.
6. Agregar o actualizar la entrada correspondiente en `BITACORA.md`.
7. Presentar el cambio y la validación para revisión. **No hacer commit hasta
   que la usuaria dé el visto bueno para ese cambio**.
8. Tras la aprobación, crear un commit atómico con mensaje en español,
   incluyendo el código y su fila de bitácora. Agregar archivos específicos
   al staging para evitar incluir cambios ajenos. No modificar commits ya
   creados sin autorización.

Si falla una prueba, detener la siguiente refactorización, investigar y corregir
el cambio en curso. Si la solución exige modificar archivos protegidos o cambiar
el comportamiento, explicar el bloqueo antes de continuar. No ocultar fallos
ni presentar validaciones pendientes como aprobadas.

## Bitácora

Git registra cambios de archivos y commits; **no registra automáticamente los
prompts de Claude**. Guardar el texto real de los prompts en `BITACORA.md`.
No reconstruir ni inventar un prompt que no esté disponible: solicitarlo o
marcarlo como pendiente.

Respetar exactamente el formato de `BITACORA_TEMPLATE.md`, sin agregar ni
quitar columnas o secciones. Una fila por refactorización en la tabla:

| # | Prompt usado | Cambio realizado | Justificación | Tests OK |

- **Prompt usado**: el prompt tal cual se escribió, o un resumen fiel si fue
  una conversación larga.
- **Cambio realizado**: qué se modificó en el código.
- **Justificación**: por qué mejora la calidad (qué *code smell* resuelve).
- **Tests OK**: resultado real de `pytest` después del cambio.

Agregar filas si hay más de 5 refactorizaciones. Si se corrige o se vuelve a
validar un cambio, actualizar su misma fila. La reflexión final (10-15 líneas)
la escribe la usuaria; no redactarla por ella.

## Convenciones de código

- Para nombres nuevos o internos, usar español y `snake_case`, con nombres
  descriptivos y sin abreviaturas crípticas. Constantes en `MAYUSCULAS`.
- Mantener los nombres públicos existentes; no renombrar todo el proyecto
  únicamente para cumplir una preferencia de estilo.
- Sustituir números mágicos por constantes con nombre cuando corresponda,
  conservando sus valores y su significado original.
- Abrir archivos con `with`, preservando modo, codificación y manejo de errores.
- Mantener funciones con una responsabilidad clara y complejidad ciclomática
  máxima de 10. Evitar extraer funciones sin un beneficio concreto.
- Usar type hints compatibles con Python 3.10+, como `str | None` y
  `list[dict]`, sin agregar conversiones o validaciones que cambien el contrato.
- Separar lógica de negocio de `print` e `input` cuando sea parte del cambio
  elegido, conservando la salida y la interacción actuales.
- Preferir la solución más sencilla que resuelva el problema. Introducir clases,
  capas o patrones solo si aportan un beneficio concreto al reto.

## Configuración de Ruff

La fuente de verdad es `pyproject.toml`; leerla antes de refactorizar.
Configuración de referencia: Python 3.10+, líneas de hasta 88 caracteres y
complejidad McCabe máxima de 10.

Reglas: pycodestyle (E/W), pyflakes (F), isort (I), nombres PEP 8 (N), bugbear
(B), simplify (SIM), pyupgrade (UP) y McCabe (C90). La carpeta `tests/` está
excluida del linter, pero debe ejecutarse completa con `pytest`.

## Comunicación

Explicar las propuestas y los resultados en español, con lenguaje claro.
Relacionar cada cambio con el problema que resuelve. Distinguir lo verificado
mediante comandos de las conclusiones obtenidas al revisar el código.
