"""Reportes de la tienda: inventario, ventas y mas vendidos."""

import gestor

# Por debajo de esta cantidad un producto se considera con stock bajo
STOCK_MINIMO = 5


def formatear_dinero(monto):
    """Da formato de dinero a un monto, redondeado a 2 decimales."""
    return f"${round(monto, 2)}"


def productos_stock_bajo():
    """Regresa la lista de productos con stock por debajo del minimo."""
    return [
        producto
        for producto in gestor.INVENTARIO.values()
        if producto["stock"] < STOCK_MINIMO
    ]


def reporte_inventario():
    """Arma el reporte del inventario, lo imprime y lo regresa como texto."""
    texto = "===== INVENTARIO =====\n"
    valor_total = 0
    for producto in gestor.INVENTARIO.values():
        linea = (
            f"{producto['codigo']} | {producto['nombre']} | "
            f"{formatear_dinero(producto['precio'])} | stock: {producto['stock']}"
        )
        if producto["stock"] < STOCK_MINIMO:
            linea += "  <-- STOCK BAJO"
        texto += linea + "\n"
        valor_total += producto["precio"] * producto["stock"]
    texto += f"Valor total del inventario: {formatear_dinero(valor_total)}\n"
    print(texto)
    return texto


def total_vendido():
    """Suma el total (con IVA) de todas las ventas registradas."""
    return round(sum(venta["total"] for venta in gestor.VENTAS), 2)


def mas_vendidos(n=3):
    """Regresa los n productos mas vendidos como lista de (codigo, unidades)."""
    unidades = {}
    for venta in gestor.VENTAS:
        codigo = venta["codigo"]
        unidades[codigo] = unidades.get(codigo, 0) + venta["cantidad"]
    # sorted es estable: los empates conservan el orden en que aparecieron
    ranking = sorted(unidades.items(), key=lambda par: par[1], reverse=True)
    return ranking[:n]


def resumen_ventas():
    """Arma el resumen de ventas del dia, lo imprime y lo regresa."""
    texto = "===== RESUMEN DE VENTAS =====\n"
    total = 0
    for venta in gestor.VENTAS:
        texto += (
            f"Folio {venta['folio']}: {venta['nombre']} x{venta['cantidad']} = "
            f"{formatear_dinero(venta['total'])}\n"
        )
        total += venta["total"]
    texto += f"Numero de ventas: {len(gestor.VENTAS)}\n"
    texto += f"Total del dia: {formatear_dinero(total)}\n"
    print(texto)
    return texto
