# Bitácora de refactorización

**Nombre:** Evelyne Franco<br>
**Matrícula:**<br>
**Fecha:** 7 de octubre de 2026

Registra aquí **cada refactorización** que realices con Claude Code. Copia el
prompt tal cual lo escribiste (o un resumen fiel si fue una conversación larga),
describe el cambio que se aplicó al código y justifica por qué mejora la calidad.
Después de cada cambio ejecuta `pytest` y anota el resultado.

## Diagnóstico (punto 2 del reto)

**Prompt usado para el análisis del código y la propuesta de refactorización:**

> Eres un programador senio de python, tienes conocimentos sobre best practices y code smells, especialmente en python.
>
> Explora el codigo de este repositorio, necesito como salida un diagnostico detallado sobre code smells, mejores practicas, Vas a ordenar por mas importante a menos importante.
> Una vez identificados y priorizados, necesito que tambien incluyas en reporte porque es importante el cambio, la explicacion debe ser entendible, como si explicaras a un universitario o jr que apenas aprende de este tema.
>
> Por ultimo propon un plan de implementacion y que refactorizacion recomiendas hacer, cuidando que los test sigan pasando.

**Prompt de seguimiento** (para generar el reporte en `reporte/propuesta_de_refactorizacion.md`):

> Olvide mencionar en el prompt genera un archivo md y un folder (reporte/propuesta_de_refactorizavion.md)  agrega esta informacion, tu diagnostico y recomendacion exactamente como me o muetras en el chat pero ahora en el reporte.

## Refactorizaciones

| #  | Prompt usado | Cambio realizado | Justificación | Tests OK |
|----|--------------|------------------|---------------|----------|
| 1  | Sigues siento el Senior programador en python, basado en la propuesta de refatorizacion realizada vas a implementar la refactorizacion que llamamos<br>"R1" Eliminar codigo muerto e imports sin usar<br><br>Despues de los cambios de codigo, los test deben seguir pasando sin actualizar los test.<br>Una vez asegurado que los test pasaron con la refactorizacion haces el commit a la rama R1 Eliminacion de codigo muerto e ipmorts sin usar. | **R1 – Eliminar código muerto e imports sin usar**<br>• `gestor.py`: se eliminaron `calcular_descuento_viejo()`, la función comentada `exportar_txt()` y la variable `MODO_DEBUG`.<br>• `reportes.py`: se eliminaron `reporteViejoCSV()`, el `import os` sin usar y la línea `# -*- coding: utf-8 -*-`.<br>• Antes de borrar se verificó con `grep` que nada los usaba. | El código muerto confunde: obliga a investigar si algo se usa y puede reutilizarse por error. Si algún día se necesita, está en el historial de git.<br>Ruff: 20 → 16 errores. | ✅ 20 passed |
| 2  | Siguiendo trabajando como Senior en python, continuamos con el regactor propuesto en la documentacion propiesta de refactorizacion.md.<br><br>Vas a aplicar la refactorizacion en R2 a R4 que es limpia de terreno, eliminar codigo que estorba.<br>Despues del refactor debes correr los test y deben seguir pasando los 20 test<br>Si los test pasan haz el commit a la rama refactorizavion con el mensaje que indique que cambios lleva este commit. | **R2 – Reemplazar números mágicos por constantes**<br>• `gestor.py`: `TASA_IVA`, `MONTO_DESCUENTO_ALTO`/`TASA_DESCUENTO_ALTO`, `MONTO_DESCUENTO_MEDIO`/`TASA_DESCUENTO_MEDIO`, `PREFIJO_CLIENTE_VIP`, `MONTO_MINIMO_VIP` y `TASA_DESCUENTO_VIP`.<br>• `reportes.py`: `STOCK_MINIMO`, que reemplaza el `5` repetido en dos funciones. | Un número suelto como `0.16` no dice qué significa; una constante con nombre documenta la regla de negocio y se cambia en un solo lugar. El umbral de stock bajo estaba duplicado: cambiar uno y olvidar el otro haría que el reporte y la alerta no coincidieran.<br>Ruff: 16 → 16 (este problema no lo detecta ruff). | ✅ 20 passed |
| 3  | Mismo prompt de la fila 2 (un solo prompt para R2, R3 y R4). | **R3 – Extraer el cálculo de precios duplicado**<br>• `gestor.py`: nuevas funciones `calcular_descuento_por_volumen(subtotal)` y `calcular_iva(base)`.<br>• `registrar_venta` y `cotizar` ahora las usan en lugar de repetir el mismo cálculo.<br>• El descuento VIP sigue solo en `registrar_venta`, igual que antes. | La regla de descuentos e IVA estaba copiada en dos funciones: si cambiaba en una y no en la otra, la cotización dejaba de coincidir con el cobro (principio DRY). Además las cláusulas `if`/`return` eliminan el `else` anidado.<br>Ruff: 16 → 14 (SIM108 y C901 de `registrar_venta`). | ✅ 20 passed |
| 4  | Mismo prompt de la fila 2 (un solo prompt para R2, R3 y R4). | **R4 – Dividir `registrar_venta`**<br>• Validación con cláusulas de guarda en `_validar_venta()`, conservando el orden de los mensajes de error.<br>• Descuento total (volumen + VIP) en `calcular_descuento()`, con `_es_cliente_vip()` en lugar de 3 `if` anidados.<br>• Ticket en `_armar_ticket()`; la venta se arma con un diccionario literal.<br>• `registrar_venta` quedó en ~25 líneas que solo coordinan. | La función hacía de todo (validar, calcular, descontar stock, armar ticket y guardar) y tenía 4 niveles de `if` anidados: era difícil de leer y cualquier cambio arriesgaba el cobro. Ahora cada función tiene una sola responsabilidad.<br>Se comparó la salida antes/después (tickets, cotizaciones, VIP, errores y casos límite) y es idéntica.<br>Ruff: 14 → 11 (3× SIM102). | ✅ 20 passed |
| 5  |              |                  |               |          |

> Agrega más filas si realizas más de 5 refactorizaciones.

## Reflexión final (10-15 líneas)

Responde: ¿Qué tan útil fue Claude Code para detectar y corregir los problemas?
¿Qué propuso la IA que tú no habías notado? ¿En qué casos tuviste que corregir
o rechazar sus sugerencias? ¿Qué aprendiste sobre refactorizar con apoyo de IA?

*(Escribe aquí tu reflexión)*
