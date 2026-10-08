from datetime import datetime

from negocio import reglas_lealtad
from negocio import servicios_clientes
from persistencia import cliente_dao
from persistencia import pedido_dao
from persistencia import producto_dao


ESTADOS_PEDIDO = (
    "Pendiente de pago",
    "En preparación",
    "Listo",
    "Entregado",
)

TRANSICIONES_VALIDAS = {
    "Pendiente de pago": ("En preparación",),
    "En preparación": ("Listo",),
    "Listo": ("Entregado",),
    "Entregado": (),
}


def crear_pedido(
    cliente_id,
    items,
    devpoints_a_redimir=0,
):
    """
    Valida, calcula y registra un pedido nuevo.

    Cada item debe tener este formato:
    {
        "producto_id": 1,
        "cantidad": 2
    }
    """
    cliente = cliente_dao.obtener_cliente(cliente_id)

    if cliente is None:
        raise ValueError("El cliente no existe.")

    if not items:
        raise ValueError("El pedido debe tener al menos un producto.")

    pedidos_pendientes = (
        pedido_dao.contar_pedidos_por_cliente_y_estado(
            cliente_id,
            "Pendiente de pago",
        )
    )

    if pedidos_pendientes > 0:
        raise ValueError(
            "El cliente ya tiene un pedido pendiente de pago."
        )

    if devpoints_a_redimir < 0:
        raise ValueError(
            "Los DevPoints a redimir no pueden ser negativos."
        )

    if devpoints_a_redimir > cliente["devpoints"]:
        raise ValueError(
            "El cliente no tiene suficientes DevPoints."
        )

    items_validados = []
    subtotal = 0

    for item in items:
        producto_id = item.get("producto_id")
        cantidad = item.get("cantidad")

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser un número entero positivo."
            )

        producto = producto_dao.obtener_producto(producto_id)

        if producto is None:
            raise ValueError(
                f"El producto {producto_id} no existe."
            )

        if cantidad > producto["stock"]:
            raise ValueError(
                f"No hay suficiente stock de "
                f"{producto['nombre']}."
            )

        subtotal_item = producto["precio"] * cantidad
        subtotal += subtotal_item

        items_validados.append(
            {
                "producto_id": producto["id"],
                "cantidad": cantidad,
                "precio_unitario": producto["precio"],
                "stock_actual": producto["stock"],
            }
        )

    descuento_nivel = reglas_lealtad.calcular_descuento_por_nivel(
        subtotal,
        cliente["nivel"],
    )

    maximo_descuento_devpoints = max(
        subtotal - descuento_nivel,
        0,
    )

    descuento_devpoints = min(
        reglas_lealtad.calcular_descuento_por_devpoints(
            devpoints_a_redimir
        ),
        maximo_descuento_devpoints,
    )

    total = reglas_lealtad.calcular_total(
        subtotal,
        descuento_nivel,
        descuento_devpoints,
    )

    fecha = datetime.now().isoformat(timespec="seconds")

    pedido_id = pedido_dao.crear_pedido(
        cliente_id=cliente_id,
        estado="Pendiente de pago",
        subtotal=subtotal,
        descuento_nivel=descuento_nivel,
        descuento_devpoints=descuento_devpoints,
        total=total,
        fecha=fecha,
    )

    for item in items_validados:
        pedido_dao.crear_item_pedido(
            pedido_id=pedido_id,
            producto_id=item["producto_id"],
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"],
        )

        nuevo_stock = item["stock_actual"] - item["cantidad"]

        producto_dao.actualizar_stock(
            producto_id=item["producto_id"],
            nuevo_stock=nuevo_stock,
        )

    return pedido_dao.obtener_pedido(pedido_id)


def listar_pedidos():
    """
    Devuelve todos los pedidos.
    """
    return pedido_dao.listar_pedidos()


def obtener_pedido(pedido_id):
    """
    Devuelve un pedido con sus productos.
    """
    pedido = pedido_dao.obtener_pedido(pedido_id)

    if pedido is None:
        raise ValueError("El pedido no existe.")

    return pedido


def cambiar_estado(pedido_id, nuevo_estado):
    """
    Cambia el estado de un pedido respetando el flujo permitido.
    """
    if nuevo_estado not in ESTADOS_PEDIDO:
        raise ValueError("El estado del pedido no es válido.")

    pedido = obtener_pedido(pedido_id)
    estado_actual = pedido["estado"]

    estados_siguientes = TRANSICIONES_VALIDAS[estado_actual]

    if nuevo_estado not in estados_siguientes:
        raise ValueError(
            f"No se puede pasar de '{estado_actual}' "
            f"a '{nuevo_estado}'."
        )

    actualizado = pedido_dao.actualizar_estado(
        pedido_id,
        nuevo_estado,
    )

    if not actualizado:
        raise ValueError("No se pudo actualizar el estado.")

    if nuevo_estado == "Entregado":
        devpoints_redimidos = (
            pedido["descuento_devpoints"]
            // reglas_lealtad.VALOR_POR_DEVPOINT
        )

        servicios_clientes.actualizar_lealtad_por_compra(
            cliente_id=pedido["cliente_id"],
            monto_consumido=pedido["total"],
            devpoints_redimidos=devpoints_redimidos,
        )

    return obtener_pedido(pedido_id)