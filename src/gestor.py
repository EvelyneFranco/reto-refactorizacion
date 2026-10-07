# -*- coding: utf-8 -*-
"""Modulo principal del gestor de inventario y ventas de "La Esquina".

Aqui vive casi toda la logica del negocio. Historicamente este archivo
lo fueron parchando varias personas, asi que hay de todo un poco.
"""

from datetime import datetime

# ---------------------------------------------------------------
# Reglas de negocio: impuestos y descuentos
# ---------------------------------------------------------------
TASA_IVA = 0.16

# Descuento por volumen segun el subtotal de la compra
MONTO_DESCUENTO_ALTO = 1000
TASA_DESCUENTO_ALTO = 0.10
MONTO_DESCUENTO_MEDIO = 500
TASA_DESCUENTO_MEDIO = 0.05

# Descuento extra para clientes VIP (codigo que empieza con el prefijo)
PREFIJO_CLIENTE_VIP = "VIP"
MONTO_MINIMO_VIP = 200
TASA_DESCUENTO_VIP = 0.02

# ---------------------------------------------------------------
# Estado global de la aplicacion (inventario, ventas y contadores)
# ---------------------------------------------------------------
INVENTARIO = {}
VENTAS = []
contadorVentas = 0
ultimo_error = ""


def reiniciar_sistema():
    """Borra todo el estado del sistema (inventario, ventas y folios)."""
    global contadorVentas, ultimo_error
    INVENTARIO.clear()
    VENTAS.clear()
    contadorVentas = 0
    ultimo_error = ""


def agregarProducto(codigo, nombre, precio, stock):
    # valida los datos y da de alta un producto en el inventario
    global ultimo_error
    if codigo is None or codigo == "":
        ultimo_error = "codigo vacio"
        return False
    if codigo in INVENTARIO:
        ultimo_error = "el producto ya existe"
        return False
    if precio <= 0:
        ultimo_error = "precio invalido"
        return False
    if stock < 0:
        ultimo_error = "stock invalido"
        return False
    x = {}
    x["codigo"] = codigo
    x["nombre"] = nombre
    x["precio"] = precio
    x["stock"] = stock
    INVENTARIO[codigo] = x
    return True


def eliminar_producto(codigo):
    """Quita un producto del inventario. Regresa False si no existe."""
    global ultimo_error
    if codigo in INVENTARIO:
        del INVENTARIO[codigo]
        return True
    ultimo_error = "producto no existe"
    return False


def actualizar_stock(codigo, cantidad):
    """Suma unidades al stock (o resta si la cantidad es negativa)."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return False
    aux = INVENTARIO[codigo]["stock"] + cantidad
    if aux < 0:
        ultimo_error = "el stock no puede quedar negativo"
        return False
    INVENTARIO[codigo]["stock"] = aux
    return True


def buscarProducto(texto):
    # busca productos cuyo nombre contenga el texto (sin importar mayusculas)
    temp2 = []
    for k in INVENTARIO:
        if texto.lower() in INVENTARIO[k]["nombre"].lower():
            temp2.append(INVENTARIO[k])
    return temp2


def calcular_descuento_por_volumen(subtotal):
    """Regresa el descuento que corresponde al subtotal segun su monto."""
    if subtotal >= MONTO_DESCUENTO_ALTO:
        return subtotal * TASA_DESCUENTO_ALTO
    if subtotal >= MONTO_DESCUENTO_MEDIO:
        return subtotal * TASA_DESCUENTO_MEDIO
    return 0


def calcular_iva(base):
    """Regresa el IVA que corresponde a un monto ya con descuentos."""
    return base * TASA_IVA


def _validar_venta(codigo, cantidad):
    """Regresa el producto a vender, o None si la venta no es valida.

    Las validaciones se revisan en orden y la primera que falla deja su
    motivo en ultimo_error.
    """
    global ultimo_error
    if codigo is None or codigo == "":
        ultimo_error = "codigo vacio"
        return None
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return None
    # se usa "not ... >" para conservar el resultado original en casos
    # limite (por ejemplo NaN), donde "<=" no es el opuesto exacto
    if cantidad is None or not cantidad > 0:
        ultimo_error = "cantidad invalida"
        return None
    producto = INVENTARIO[codigo]
    if not producto["stock"] >= cantidad:
        ultimo_error = "stock insuficiente"
        return None
    return producto


def _es_cliente_vip(cliente):
    """Indica si el codigo de cliente empieza con el prefijo VIP."""
    return cliente is not None and cliente.startswith(PREFIJO_CLIENTE_VIP)


def calcular_descuento(subtotal, cliente):
    """Descuento total de una venta: por volumen mas el extra VIP.

    El extra VIP solo aplica si la compra, ya con el descuento por
    volumen, pasa de MONTO_MINIMO_VIP.
    """
    descuento = calcular_descuento_por_volumen(subtotal)
    if _es_cliente_vip(cliente) and subtotal - descuento > MONTO_MINIMO_VIP:
        descuento = descuento + subtotal * TASA_DESCUENTO_VIP
    return descuento


def _armar_ticket(venta, hay_descuento):
    """Arma el ticket de la venta en texto plano."""
    ticket = "TIENDA LA ESQUINA\n"
    ticket += "----------------------------\n"
    ticket += f"Folio: {venta['folio']}\n"
    ticket += f"{venta['nombre']} x{venta['cantidad']}\n"
    ticket += f"Subtotal: ${venta['subtotal']}\n"
    if hay_descuento:
        ticket += f"Descuento: -${venta['descuento']}\n"
    ticket += f"IVA: ${venta['impuesto']}\n"
    ticket += f"TOTAL: ${venta['total']}\n"
    return ticket


def registrar_venta(codigo, cantidad, cliente=""):
    """Registra una venta: calcula importes, descuenta stock y arma el ticket.

    Si algo falla regresa None y deja el motivo en ultimo_error.
    """
    global contadorVentas
    producto = _validar_venta(codigo, cantidad)
    if producto is None:
        return None
    subtotal = producto["precio"] * cantidad
    descuento = calcular_descuento(subtotal, cliente)
    base = subtotal - descuento
    impuesto = calcular_iva(base)
    producto["stock"] = producto["stock"] - cantidad
    contadorVentas = contadorVentas + 1
    venta = {
        "folio": contadorVentas,
        "codigo": codigo,
        "nombre": producto["nombre"],
        "cantidad": cantidad,
        "subtotal": round(subtotal, 2),
        "descuento": round(descuento, 2),
        "impuesto": round(impuesto, 2),
        "total": round(base + impuesto, 2),
        "cliente": cliente,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    venta["ticket"] = _armar_ticket(venta, descuento > 0)
    VENTAS.append(venta)
    return venta


def cotizar(codigo, cantidad):
    """Calcula cuanto costaria una compra sin registrar la venta."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return None
    if cantidad is None or cantidad <= 0:
        ultimo_error = "cantidad invalida"
        return None
    aux = INVENTARIO[codigo]["precio"] * cantidad
    desc = calcular_descuento_por_volumen(aux)
    base = aux - desc
    total = base + calcular_iva(base)
    return round(total, 2)
