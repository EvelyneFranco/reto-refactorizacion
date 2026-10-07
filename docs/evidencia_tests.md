# Evidencia de tests y linter

Cada refactorización se hizo en su propio commit. Para esta evidencia se hizo
checkout de **cada commit** y se ejecutaron `pytest -v` y `ruff check src` sobre
ese código exacto (Python 3.12.15, entorno virtual del proyecto). Los logs de
abajo son la salida real de esas ejecuciones.

Los tests (`tests/`) y la configuración del linter (`pyproject.toml`) no se
modificaron en ningún commit.

## Resumen por refactorización

| Paso | Commit | Refactorización | `pytest` | Errores de ruff |
|---|---|---|---|---|
| Inicio | `db27683` | Código original (punto de partida) | ✅ 20 passed | **20** |
| R1 | `8783e49` | Eliminar código muerto e imports sin usar | ✅ 20 passed | **16** (20 → 16) |
| R2 | `749d4e7` | Reemplazar números mágicos por constantes | ✅ 20 passed | **16** (sin cambio) |
| R3 | `e17553b` | Extraer el cálculo de descuentos e IVA duplicado | ✅ 20 passed | **14** (16 → 14) |
| R4 | `a0109ae` | Dividir `registrar_venta` | ✅ 20 passed | **11** (14 → 11) |
| R5 | `a3104aa` | Dividir `menu()` en una función por opción | ✅ 20 passed | **8** (11 → 8) |
| R7 | `e954bc4` | Nombres descriptivos y snake_case | ✅ 20 passed | **6** (8 → 6) |
| R6 | `cb018c3` | Manejo seguro de archivos con `with` | ✅ 20 passed | **0** (6 → 0) |
| R8 | `54198ee` | Python idiomático | ✅ 20 passed | **0** (sin cambio) |

El orden es el de los commits: R7 se aplicó antes que R6 (primero los cambios de riesgo medio y después los de riesgo bajo).

## Logs por refactorización

### Código original

Commit `db27683 Código original del reto (punto de partida)`

**pytest:** ✅ 20 passed · **ruff:** 20 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.02s ==============================

$ ruff check src
UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/almacen.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |

SIM115 Use a context manager for opening files
  --> src/almacen.py:16:9
   |
14 |     d["ventas"] = gestor.VENTAS
15 |     d["contador"] = gestor.contadorVentas
16 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
17 |     json.dump(d, f, indent=2, ensure_ascii=False)
18 |     f.close()
   |

SIM115 Use a context manager for opening files
  --> src/almacen.py:30:9
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |         ^^^^
31 |     try:
32 |         d = json.load(f)
   |

UP015 [*] Unnecessary mode argument
  --> src/almacen.py:30:20
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |                    ^^^
31 |     try:
32 |         d = json.load(f)
   |
help: Remove mode argument
   |
29 |         return False
   -     f = open(ruta, "r", encoding="utf-8")
30 +     f = open(ruta, encoding="utf-8")
31 |     try:
   |

N802 Function name `hayArchivo` should be lowercase
  --> src/almacen.py:48:5
   |
48 | def hayArchivo(ruta):
   |     ^^^^^^^^^^
49 |     # checa si ya existe el archivo de datos
50 |     if os.path.exists(ruta):
   |

SIM103 Return the condition `bool(os.path.exists(ruta))` directly
  --> src/almacen.py:50:5
   |
48 |   def hayArchivo(ruta):
49 |       # checa si ya existe el archivo de datos
50 | /     if os.path.exists(ruta):
51 | |         return True
52 | |     else:
53 | |         return False
   | |____________________^
help: Replace with `return bool(os.path.exists(ruta))`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/gestor.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |

N816 Variable `contadorVentas` in global scope should not be mixedCase
  --> src/gestor.py:15:1
   |
13 | INVENTARIO = {}
14 | VENTAS = []
15 | contadorVentas = 0
   | ^^^^^^^^^^^^^^
16 | ultimo_error = ""
17 | MODO_DEBUG = False
   |

C901 `registrar_venta` is too complex (12 > 10)
  --> src/gestor.py:86:5
   |
86 | def registrar_venta(codigo, cantidad, cliente=""):
   |     ^^^^^^^^^^^^^^^
87 |     """Registra una venta completa.
   |

SIM108 Use ternary operator `desc = aux * 0.05 if aux >= 500 else 0` instead of `if`-`else`-block
   --> src/gestor.py:120:9
    |
118 |           desc = aux * 0.10
119 |       else:
120 | /         if aux >= 500:
121 | |             desc = aux * 0.05
122 | |         else:
123 | |             desc = 0
    | |____________________^
124 |       # los clientes cuyo codigo empieza con VIP tienen un extra,
125 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
    |
help: Replace `if`-`else`-block with `desc = aux * 0.05 if aux >= 500 else 0`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:126:5
    |
124 |       # los clientes cuyo codigo empieza con VIP tienen un extra,
125 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
126 | /     if cliente != "" and cliente is not None:
127 | |         if len(cliente) >= 3:
128 | |             if cliente[0:3] == "VIP":
129 | |                 if aux - desc > 200:
    | |____________________________________^
130 |                       desc = desc + aux * 0.02
131 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:127:9
    |
125 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
126 |       if cliente != "" and cliente is not None:
127 | /         if len(cliente) >= 3:
128 | |             if cliente[0:3] == "VIP":
129 | |                 if aux - desc > 200:
    | |____________________________________^
130 |                       desc = desc + aux * 0.02
131 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:128:13
    |
126 |       if cliente != "" and cliente is not None:
127 |           if len(cliente) >= 3:
128 | /             if cliente[0:3] == "VIP":
129 | |                 if aux - desc > 200:
    | |____________________________________^
130 |                       desc = desc + aux * 0.02
131 |       base = aux - desc
    |
help: Combine `if` statements using `and`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/main.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |

I001 [*] Import block is un-sorted or un-formatted
 --> src/main.py:4:1
  |
2 |   """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
3 |
4 | / import gestor
5 | | import almacen
6 | | import reportes
  | |_______________^
7 |
8 |   ARCHIVO = "datos_ejemplo.json"
  |
help: Organize imports
  |
3 |
4 + import almacen
5 | import gestor
  - import almacen
6 | import reportes
  |

C901 `menu` is too complex (17 > 10)
  --> src/main.py:21:5
   |
21 | def menu():
   |     ^^^^
22 |     print("Bienvenido al gestor de la tienda La Esquina")
23 |     if almacen.hayArchivo(ARCHIVO):
   |

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/reportes.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Reportes de la tienda: inventario, ventas y mas vendidos."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Reportes de la tienda: inventario, ventas y mas vendidos."""
  |

F401 [*] `os` imported but unused
 --> src/reportes.py:4:8
  |
2 | """Reportes de la tienda: inventario, ventas y mas vendidos."""
3 |
4 | import os
  |        ^^
5 |
6 | import gestor
  |
help: Remove unused import: `os`
  |
3 |
  - import os
4 |
  |

N802 Function name `reporteViejoCSV` should be lowercase
  --> src/reportes.py:83:5
   |
83 | def reporteViejoCSV(ruta):
   |     ^^^^^^^^^^^^^^^
84 |     # version vieja del reporte que pedia contabilidad, ya no se usa
85 |     # desde que cambiaron de sistema, pero por si las dudas aqui sigue
   |

SIM115 Use a context manager for opening files
  --> src/reportes.py:86:9
   |
84 |     # version vieja del reporte que pedia contabilidad, ya no se usa
85 |     # desde que cambiaron de sistema, pero por si las dudas aqui sigue
86 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
87 |     f.write("codigo,nombre,stock\n")
88 |     for k in gestor.INVENTARIO:
   |

Found 20 errors.
[*] 7 fixable with the `--fix` option (5 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

</details>

### R1: Eliminar código muerto e imports sin usar

Commit `8783e49 R1: Eliminación de código muerto e imports sin usar`

**pytest:** ✅ 20 passed · **ruff:** 16 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/almacen.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |

SIM115 Use a context manager for opening files
  --> src/almacen.py:16:9
   |
14 |     d["ventas"] = gestor.VENTAS
15 |     d["contador"] = gestor.contadorVentas
16 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
17 |     json.dump(d, f, indent=2, ensure_ascii=False)
18 |     f.close()
   |

SIM115 Use a context manager for opening files
  --> src/almacen.py:30:9
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |         ^^^^
31 |     try:
32 |         d = json.load(f)
   |

UP015 [*] Unnecessary mode argument
  --> src/almacen.py:30:20
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |                    ^^^
31 |     try:
32 |         d = json.load(f)
   |
help: Remove mode argument
   |
29 |         return False
   -     f = open(ruta, "r", encoding="utf-8")
30 +     f = open(ruta, encoding="utf-8")
31 |     try:
   |

N802 Function name `hayArchivo` should be lowercase
  --> src/almacen.py:48:5
   |
48 | def hayArchivo(ruta):
   |     ^^^^^^^^^^
49 |     # checa si ya existe el archivo de datos
50 |     if os.path.exists(ruta):
   |

SIM103 Return the condition `bool(os.path.exists(ruta))` directly
  --> src/almacen.py:50:5
   |
48 |   def hayArchivo(ruta):
49 |       # checa si ya existe el archivo de datos
50 | /     if os.path.exists(ruta):
51 | |         return True
52 | |     else:
53 | |         return False
   | |____________________^
help: Replace with `return bool(os.path.exists(ruta))`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/gestor.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |

N816 Variable `contadorVentas` in global scope should not be mixedCase
  --> src/gestor.py:15:1
   |
13 | INVENTARIO = {}
14 | VENTAS = []
15 | contadorVentas = 0
   | ^^^^^^^^^^^^^^
16 | ultimo_error = ""
   |

C901 `registrar_venta` is too complex (12 > 10)
  --> src/gestor.py:85:5
   |
85 | def registrar_venta(codigo, cantidad, cliente=""):
   |     ^^^^^^^^^^^^^^^
86 |     """Registra una venta completa.
   |

SIM108 Use ternary operator `desc = aux * 0.05 if aux >= 500 else 0` instead of `if`-`else`-block
   --> src/gestor.py:119:9
    |
117 |           desc = aux * 0.10
118 |       else:
119 | /         if aux >= 500:
120 | |             desc = aux * 0.05
121 | |         else:
122 | |             desc = 0
    | |____________________^
123 |       # los clientes cuyo codigo empieza con VIP tienen un extra,
124 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
    |
help: Replace `if`-`else`-block with `desc = aux * 0.05 if aux >= 500 else 0`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:125:5
    |
123 |       # los clientes cuyo codigo empieza con VIP tienen un extra,
124 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
125 | /     if cliente != "" and cliente is not None:
126 | |         if len(cliente) >= 3:
127 | |             if cliente[0:3] == "VIP":
128 | |                 if aux - desc > 200:
    | |____________________________________^
129 |                       desc = desc + aux * 0.02
130 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:126:9
    |
124 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
125 |       if cliente != "" and cliente is not None:
126 | /         if len(cliente) >= 3:
127 | |             if cliente[0:3] == "VIP":
128 | |                 if aux - desc > 200:
    | |____________________________________^
129 |                       desc = desc + aux * 0.02
130 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:127:13
    |
125 |       if cliente != "" and cliente is not None:
126 |           if len(cliente) >= 3:
127 | /             if cliente[0:3] == "VIP":
128 | |                 if aux - desc > 200:
    | |____________________________________^
129 |                       desc = desc + aux * 0.02
130 |       base = aux - desc
    |
help: Combine `if` statements using `and`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/main.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |

I001 [*] Import block is un-sorted or un-formatted
 --> src/main.py:4:1
  |
2 |   """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
3 |
4 | / import gestor
5 | | import almacen
6 | | import reportes
  | |_______________^
7 |
8 |   ARCHIVO = "datos_ejemplo.json"
  |
help: Organize imports
  |
3 |
4 + import almacen
5 | import gestor
  - import almacen
6 | import reportes
  |

C901 `menu` is too complex (17 > 10)
  --> src/main.py:21:5
   |
21 | def menu():
   |     ^^^^
22 |     print("Bienvenido al gestor de la tienda La Esquina")
23 |     if almacen.hayArchivo(ARCHIVO):
   |

Found 16 errors.
[*] 5 fixable with the `--fix` option (5 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

</details>

### R2: Reemplazar números mágicos por constantes

Commit `749d4e7 R2: Reemplazo de números mágicos por constantes`

**pytest:** ✅ 20 passed · **ruff:** 16 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/almacen.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |

SIM115 Use a context manager for opening files
  --> src/almacen.py:16:9
   |
14 |     d["ventas"] = gestor.VENTAS
15 |     d["contador"] = gestor.contadorVentas
16 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
17 |     json.dump(d, f, indent=2, ensure_ascii=False)
18 |     f.close()
   |

SIM115 Use a context manager for opening files
  --> src/almacen.py:30:9
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |         ^^^^
31 |     try:
32 |         d = json.load(f)
   |

UP015 [*] Unnecessary mode argument
  --> src/almacen.py:30:20
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |                    ^^^
31 |     try:
32 |         d = json.load(f)
   |
help: Remove mode argument
   |
29 |         return False
   -     f = open(ruta, "r", encoding="utf-8")
30 +     f = open(ruta, encoding="utf-8")
31 |     try:
   |

N802 Function name `hayArchivo` should be lowercase
  --> src/almacen.py:48:5
   |
48 | def hayArchivo(ruta):
   |     ^^^^^^^^^^
49 |     # checa si ya existe el archivo de datos
50 |     if os.path.exists(ruta):
   |

SIM103 Return the condition `bool(os.path.exists(ruta))` directly
  --> src/almacen.py:50:5
   |
48 |   def hayArchivo(ruta):
49 |       # checa si ya existe el archivo de datos
50 | /     if os.path.exists(ruta):
51 | |         return True
52 | |     else:
53 | |         return False
   | |____________________^
help: Replace with `return bool(os.path.exists(ruta))`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/gestor.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |

N816 Variable `contadorVentas` in global scope should not be mixedCase
  --> src/gestor.py:31:1
   |
29 | INVENTARIO = {}
30 | VENTAS = []
31 | contadorVentas = 0
   | ^^^^^^^^^^^^^^
32 | ultimo_error = ""
   |

C901 `registrar_venta` is too complex (12 > 10)
   --> src/gestor.py:101:5
    |
101 | def registrar_venta(codigo, cantidad, cliente=""):
    |     ^^^^^^^^^^^^^^^
102 |     """Registra una venta completa.
    |

SIM108 Use ternary operator `desc = aux * TASA_DESCUENTO_MEDIO if aux >= MONTO_DESCUENTO_MEDIO else 0` instead of `if`-`else`-block
   --> src/gestor.py:135:9
    |
133 |           desc = aux * TASA_DESCUENTO_ALTO
134 |       else:
135 | /         if aux >= MONTO_DESCUENTO_MEDIO:
136 | |             desc = aux * TASA_DESCUENTO_MEDIO
137 | |         else:
138 | |             desc = 0
    | |____________________^
139 |       # los clientes cuyo codigo empieza con VIP tienen un extra,
140 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
    |
help: Replace `if`-`else`-block with `desc = aux * TASA_DESCUENTO_MEDIO if aux >= MONTO_DESCUENTO_MEDIO else 0`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:141:5
    |
139 |       # los clientes cuyo codigo empieza con VIP tienen un extra,
140 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
141 | /     if cliente != "" and cliente is not None:
142 | |         if len(cliente) >= len(PREFIJO_CLIENTE_VIP):
143 | |             if cliente[0:len(PREFIJO_CLIENTE_VIP)] == PREFIJO_CLIENTE_VIP:
144 | |                 if aux - desc > MONTO_MINIMO_VIP:
    | |_________________________________________________^
145 |                       desc = desc + aux * TASA_DESCUENTO_VIP
146 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:142:9
    |
140 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
141 |       if cliente != "" and cliente is not None:
142 | /         if len(cliente) >= len(PREFIJO_CLIENTE_VIP):
143 | |             if cliente[0:len(PREFIJO_CLIENTE_VIP)] == PREFIJO_CLIENTE_VIP:
144 | |                 if aux - desc > MONTO_MINIMO_VIP:
    | |_________________________________________________^
145 |                       desc = desc + aux * TASA_DESCUENTO_VIP
146 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:143:13
    |
141 |       if cliente != "" and cliente is not None:
142 |           if len(cliente) >= len(PREFIJO_CLIENTE_VIP):
143 | /             if cliente[0:len(PREFIJO_CLIENTE_VIP)] == PREFIJO_CLIENTE_VIP:
144 | |                 if aux - desc > MONTO_MINIMO_VIP:
    | |_________________________________________________^
145 |                       desc = desc + aux * TASA_DESCUENTO_VIP
146 |       base = aux - desc
    |
help: Combine `if` statements using `and`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/main.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |

I001 [*] Import block is un-sorted or un-formatted
 --> src/main.py:4:1
  |
2 |   """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
3 |
4 | / import gestor
5 | | import almacen
6 | | import reportes
  | |_______________^
7 |
8 |   ARCHIVO = "datos_ejemplo.json"
  |
help: Organize imports
  |
3 |
4 + import almacen
5 | import gestor
  - import almacen
6 | import reportes
  |

C901 `menu` is too complex (17 > 10)
  --> src/main.py:21:5
   |
21 | def menu():
   |     ^^^^
22 |     print("Bienvenido al gestor de la tienda La Esquina")
23 |     if almacen.hayArchivo(ARCHIVO):
   |

Found 16 errors.
[*] 5 fixable with the `--fix` option (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

</details>

### R3: Extraer el cálculo de descuentos e IVA duplicado

Commit `e17553b R3: Extracción del cálculo de descuentos e IVA duplicado`

**pytest:** ✅ 20 passed · **ruff:** 14 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/almacen.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |

SIM115 Use a context manager for opening files
  --> src/almacen.py:16:9
   |
14 |     d["ventas"] = gestor.VENTAS
15 |     d["contador"] = gestor.contadorVentas
16 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
17 |     json.dump(d, f, indent=2, ensure_ascii=False)
18 |     f.close()
   |

SIM115 Use a context manager for opening files
  --> src/almacen.py:30:9
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |         ^^^^
31 |     try:
32 |         d = json.load(f)
   |

UP015 [*] Unnecessary mode argument
  --> src/almacen.py:30:20
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |                    ^^^
31 |     try:
32 |         d = json.load(f)
   |
help: Remove mode argument
   |
29 |         return False
   -     f = open(ruta, "r", encoding="utf-8")
30 +     f = open(ruta, encoding="utf-8")
31 |     try:
   |

N802 Function name `hayArchivo` should be lowercase
  --> src/almacen.py:48:5
   |
48 | def hayArchivo(ruta):
   |     ^^^^^^^^^^
49 |     # checa si ya existe el archivo de datos
50 |     if os.path.exists(ruta):
   |

SIM103 Return the condition `bool(os.path.exists(ruta))` directly
  --> src/almacen.py:50:5
   |
48 |   def hayArchivo(ruta):
49 |       # checa si ya existe el archivo de datos
50 | /     if os.path.exists(ruta):
51 | |         return True
52 | |     else:
53 | |         return False
   | |____________________^
help: Replace with `return bool(os.path.exists(ruta))`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/gestor.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |

N816 Variable `contadorVentas` in global scope should not be mixedCase
  --> src/gestor.py:31:1
   |
29 | INVENTARIO = {}
30 | VENTAS = []
31 | contadorVentas = 0
   | ^^^^^^^^^^^^^^
32 | ultimo_error = ""
   |

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:147:5
    |
145 |       # los clientes cuyo codigo empieza con VIP tienen un extra,
146 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
147 | /     if cliente != "" and cliente is not None:
148 | |         if len(cliente) >= len(PREFIJO_CLIENTE_VIP):
149 | |             if cliente[0:len(PREFIJO_CLIENTE_VIP)] == PREFIJO_CLIENTE_VIP:
150 | |                 if aux - desc > MONTO_MINIMO_VIP:
    | |_________________________________________________^
151 |                       desc = desc + aux * TASA_DESCUENTO_VIP
152 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:148:9
    |
146 |       # pero solo si su compra (ya con descuento) pasa de cierto monto
147 |       if cliente != "" and cliente is not None:
148 | /         if len(cliente) >= len(PREFIJO_CLIENTE_VIP):
149 | |             if cliente[0:len(PREFIJO_CLIENTE_VIP)] == PREFIJO_CLIENTE_VIP:
150 | |                 if aux - desc > MONTO_MINIMO_VIP:
    | |_________________________________________________^
151 |                       desc = desc + aux * TASA_DESCUENTO_VIP
152 |       base = aux - desc
    |
help: Combine `if` statements using `and`

SIM102 Use a single `if` statement instead of nested `if` statements
   --> src/gestor.py:149:13
    |
147 |       if cliente != "" and cliente is not None:
148 |           if len(cliente) >= len(PREFIJO_CLIENTE_VIP):
149 | /             if cliente[0:len(PREFIJO_CLIENTE_VIP)] == PREFIJO_CLIENTE_VIP:
150 | |                 if aux - desc > MONTO_MINIMO_VIP:
    | |_________________________________________________^
151 |                       desc = desc + aux * TASA_DESCUENTO_VIP
152 |       base = aux - desc
    |
help: Combine `if` statements using `and`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/main.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |

I001 [*] Import block is un-sorted or un-formatted
 --> src/main.py:4:1
  |
2 |   """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
3 |
4 | / import gestor
5 | | import almacen
6 | | import reportes
  | |_______________^
7 |
8 |   ARCHIVO = "datos_ejemplo.json"
  |
help: Organize imports
  |
3 |
4 + import almacen
5 | import gestor
  - import almacen
6 | import reportes
  |

C901 `menu` is too complex (17 > 10)
  --> src/main.py:21:5
   |
21 | def menu():
   |     ^^^^
22 |     print("Bienvenido al gestor de la tienda La Esquina")
23 |     if almacen.hayArchivo(ARCHIVO):
   |

Found 14 errors.
[*] 5 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```

</details>

### R4: Dividir `registrar_venta`

Commit `a0109ae R4: División de registrar_venta en funciones con una responsabilidad`

**pytest:** ✅ 20 passed · **ruff:** 11 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/almacen.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |

SIM115 Use a context manager for opening files
  --> src/almacen.py:16:9
   |
14 |     d["ventas"] = gestor.VENTAS
15 |     d["contador"] = gestor.contadorVentas
16 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
17 |     json.dump(d, f, indent=2, ensure_ascii=False)
18 |     f.close()
   |

SIM115 Use a context manager for opening files
  --> src/almacen.py:30:9
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |         ^^^^
31 |     try:
32 |         d = json.load(f)
   |

UP015 [*] Unnecessary mode argument
  --> src/almacen.py:30:20
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |                    ^^^
31 |     try:
32 |         d = json.load(f)
   |
help: Remove mode argument
   |
29 |         return False
   -     f = open(ruta, "r", encoding="utf-8")
30 +     f = open(ruta, encoding="utf-8")
31 |     try:
   |

N802 Function name `hayArchivo` should be lowercase
  --> src/almacen.py:48:5
   |
48 | def hayArchivo(ruta):
   |     ^^^^^^^^^^
49 |     # checa si ya existe el archivo de datos
50 |     if os.path.exists(ruta):
   |

SIM103 Return the condition `bool(os.path.exists(ruta))` directly
  --> src/almacen.py:50:5
   |
48 |   def hayArchivo(ruta):
49 |       # checa si ya existe el archivo de datos
50 | /     if os.path.exists(ruta):
51 | |         return True
52 | |     else:
53 | |         return False
   | |____________________^
help: Replace with `return bool(os.path.exists(ruta))`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/gestor.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |

N816 Variable `contadorVentas` in global scope should not be mixedCase
  --> src/gestor.py:31:1
   |
29 | INVENTARIO = {}
30 | VENTAS = []
31 | contadorVentas = 0
   | ^^^^^^^^^^^^^^
32 | ultimo_error = ""
   |

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/main.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
  |

I001 [*] Import block is un-sorted or un-formatted
 --> src/main.py:4:1
  |
2 |   """Punto de entrada del gestor de tienda (menu interactivo en consola)."""
3 |
4 | / import gestor
5 | | import almacen
6 | | import reportes
  | |_______________^
7 |
8 |   ARCHIVO = "datos_ejemplo.json"
  |
help: Organize imports
  |
3 |
4 + import almacen
5 | import gestor
  - import almacen
6 | import reportes
  |

C901 `menu` is too complex (17 > 10)
  --> src/main.py:21:5
   |
21 | def menu():
   |     ^^^^
22 |     print("Bienvenido al gestor de la tienda La Esquina")
23 |     if almacen.hayArchivo(ARCHIVO):
   |

Found 11 errors.
[*] 5 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```

</details>

### R5: Dividir `menu()` en una función por opción

Commit `a3104aa R5: División de menu() en una función por opción`

**pytest:** ✅ 20 passed · **ruff:** 8 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/almacen.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |

SIM115 Use a context manager for opening files
  --> src/almacen.py:16:9
   |
14 |     d["ventas"] = gestor.VENTAS
15 |     d["contador"] = gestor.contadorVentas
16 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
17 |     json.dump(d, f, indent=2, ensure_ascii=False)
18 |     f.close()
   |

SIM115 Use a context manager for opening files
  --> src/almacen.py:30:9
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |         ^^^^
31 |     try:
32 |         d = json.load(f)
   |

UP015 [*] Unnecessary mode argument
  --> src/almacen.py:30:20
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |                    ^^^
31 |     try:
32 |         d = json.load(f)
   |
help: Remove mode argument
   |
29 |         return False
   -     f = open(ruta, "r", encoding="utf-8")
30 +     f = open(ruta, encoding="utf-8")
31 |     try:
   |

N802 Function name `hayArchivo` should be lowercase
  --> src/almacen.py:48:5
   |
48 | def hayArchivo(ruta):
   |     ^^^^^^^^^^
49 |     # checa si ya existe el archivo de datos
50 |     if os.path.exists(ruta):
   |

SIM103 Return the condition `bool(os.path.exists(ruta))` directly
  --> src/almacen.py:50:5
   |
48 |   def hayArchivo(ruta):
49 |       # checa si ya existe el archivo de datos
50 | /     if os.path.exists(ruta):
51 | |         return True
52 | |     else:
53 | |         return False
   | |____________________^
help: Replace with `return bool(os.path.exists(ruta))`

UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/gestor.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Modulo principal del gestor de inventario y ventas de "La Esquina".
  |

N816 Variable `contadorVentas` in global scope should not be mixedCase
  --> src/gestor.py:31:1
   |
29 | INVENTARIO = {}
30 | VENTAS = []
31 | contadorVentas = 0
   | ^^^^^^^^^^^^^^
32 | ultimo_error = ""
   |

Found 8 errors.
[*] 3 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```

</details>

### R7: Nombres descriptivos y snake_case

Commit `e954bc4 R7: Nombres descriptivos y estilo snake_case consistente`

**pytest:** ✅ 20 passed · **ruff:** 6 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
UP009 [*] UTF-8 encoding declaration is unnecessary
 --> src/almacen.py:1:1
  |
1 | # -*- coding: utf-8 -*-
  | ^^^^^^^^^^^^^^^^^^^^^^^
2 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |
help: Remove unnecessary coding comment
  |
  - # -*- coding: utf-8 -*-
1 | """Persistencia del gestor: carga y guardado de datos en JSON."""
  |

SIM115 Use a context manager for opening files
  --> src/almacen.py:16:9
   |
14 |     datos["ventas"] = gestor.VENTAS
15 |     datos["contador"] = gestor.contador_ventas
16 |     f = open(ruta, "w", encoding="utf-8")
   |         ^^^^
17 |     json.dump(datos, f, indent=2, ensure_ascii=False)
18 |     f.close()
   |

SIM115 Use a context manager for opening files
  --> src/almacen.py:30:9
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |         ^^^^
31 |     try:
32 |         datos = json.load(f)
   |

UP015 [*] Unnecessary mode argument
  --> src/almacen.py:30:20
   |
28 |         gestor.ultimo_error = "el archivo no existe"
29 |         return False
30 |     f = open(ruta, "r", encoding="utf-8")
   |                    ^^^
31 |     try:
32 |         datos = json.load(f)
   |
help: Remove mode argument
   |
29 |         return False
   -     f = open(ruta, "r", encoding="utf-8")
30 +     f = open(ruta, encoding="utf-8")
31 |     try:
   |

N802 Function name `hayArchivo` should be lowercase
  --> src/almacen.py:48:5
   |
48 | def hayArchivo(ruta):
   |     ^^^^^^^^^^
49 |     # checa si ya existe el archivo de datos
50 |     if os.path.exists(ruta):
   |

SIM103 Return the condition `bool(os.path.exists(ruta))` directly
  --> src/almacen.py:50:5
   |
48 |   def hayArchivo(ruta):
49 |       # checa si ya existe el archivo de datos
50 | /     if os.path.exists(ruta):
51 | |         return True
52 | |     else:
53 | |         return False
   | |____________________^
help: Replace with `return bool(os.path.exists(ruta))`

Found 6 errors.
[*] 2 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```

</details>

### R6: Manejo seguro de archivos con `with`

Commit `cb018c3 R6: Manejo seguro de archivos y existe_archivo() en almacen`

**pytest:** ✅ 20 passed · **ruff:** 0 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
All checks passed!
```

</details>

### R8: Python idiomático

Commit `54198ee R8: Python idiomático en reportes, gestor y almacen`

**pytest:** ✅ 20 passed · **ruff:** 0 errores

<details>
<summary>Ver log</summary>

```text
$ pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.6.0 -- /Users/evelynefranco/Downloads/reto-refactorizacion/.venv/bin/python3.12
rootdir: .
configfile: pyproject.toml
testpaths: tests
collecting ... collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.01s ==============================

$ ruff check src
All checks passed!
```

</details>

## Validación adicional

Los 20 tests no cubren el texto del ticket, los reportes impresos ni el menú
interactivo. Por eso, durante el reto se compararon contra el código original,
con scripts temporales fuera del repositorio:

- Tickets, cotizaciones, descuentos VIP y mensajes de error de cientos de
  combinaciones de ventas (desde R2).
- Casos límite como `NaN` y cliente `None` (desde R4).
- Sesiones simuladas del menú (`main.py`) que recorren todas las opciones (desde R5).
- Carga de archivos corruptos, vacíos, con codificación inválida o inexistentes (desde R6).
- 300 casos aleatorios de empates en "más vendidos" (R8).

En todos los casos la salida fue idéntica a la del código original.
