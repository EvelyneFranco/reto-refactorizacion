# Bitácora de refactorización

**Nombre:** Evelyne Franco
**Matrícula:**
**Fecha:** 7 de octubre de 2026

Registra aquí **cada refactorización** que realices con Claude Code. Copia el
prompt tal cual lo escribiste (o un resumen fiel si fue una conversación larga),
describe el cambio que se aplicó al código y justifica por qué mejora la calidad.
Después de cada cambio ejecuta `pytest` y anota el resultado.

1. Prompt usado para punto 2, anàlisis del codigo y propuesta de refactorizacion:
Eres un programador senio de python, tienes conocimentos sobre best practices y code smells, especialmente en python.

Explora el codigo de este repositorio, necesito como salida un diagnostico detallado sobre code smells, mejores practicas, Vas a ordenar por mas importante a menos importante.
Una vez identificados y priorizados, necesito que tambien incluyas en reporte porque es importante el cambio, la explicacion debe ser entendible, como si explicaras a un universitario o jr que apenas aprende de este tema.

Por ultimo propon un plan de implementacion y que refactorizacion recomiendas hacer, cuidando que los test sigan pasando.

Prompt de seguimiento (para generar el reporte en reporte/propuesta_de_refactorizacion.md):
Olvide mencionar en el prompt genera un archivo md y un folder (reporte/propuesta_de_refactorizavion.md)  agrega esta informacion, tu diagnostico y recomendacion exactamente como me o muetras en el chat pero ahora en el reporte.

| #  | Prompt usado | Cambio realizado | Justificación | Tests OK |
|----|--------------|------------------|---------------|----------|
| 1  | Sigues siento el Senior programador en python, basado en la propuesta de refatorizacion realizada vas a implementar la refactorizacion que llamamos<br> "R1" Eliminar codigo muerto e imports sin usar<br><br>Despues de los cambios de codigo, los test deben seguir pasando sin actualizar los test.<br>Una vez asegurado que los test pasaron con la refactorizacion haces el commit a la rama R1 Eliminacion de codigo muerto e ipmorts sin usar. | **R1 – Eliminar código muerto e imports sin usar.** En `gestor.py`: se eliminaron `calcular_descuento_viejo()` (nadie la llamaba), la función comentada `exportar_txt()` y la variable `MODO_DEBUG` (nunca se usaba). En `reportes.py`: se eliminaron `reporteViejoCSV()` (ya no se usaba), el `import os` sin usar y la declaración `# -*- coding: utf-8 -*-`. Antes de borrar se verificó con `grep` que nada en `src/` ni en `tests/` los usaba. | El código muerto confunde: obliga a investigar si algo se usa y puede reutilizarse por error. "Por si acaso" no justifica conservarlo: si se necesita, está en el historial de git. También elimina un archivo abierto sin `with` y un nombre en camelCase que ya no hacía falta corregir. Ruff: 20 → 16 errores (F401, N802, SIM115 y UP009 en `reportes.py`). | ✅ 20 passed |
| 2  |              |                  |               |          |
| 3  |              |                  |               |          |
| 4  |              |                  |               |          |
| 5  |              |                  |               |          |

> Agrega más filas si realizas más de 5 refactorizaciones.

## Reflexión final (10-15 líneas)

Responde: ¿Qué tan útil fue Claude Code para detectar y corregir los problemas?
¿Qué propuso la IA que tú no habías notado? ¿En qué casos tuviste que corregir
o rechazar sus sugerencias? ¿Qué aprendiste sobre refactorizar con apoyo de IA?

*(Escribe aquí tu reflexión)*
