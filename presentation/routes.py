from negocio import servicios_clientes
from negocio import servicios_pedidos
from negocio import servicios_productos


def obtener_recursos(ruta):
    """
    Atiende las solicitudes GET.
    """
    if ruta == "/api/productos":
        return 200, servicios_productos.listar_productos()

    if ruta == "/api/clientes":
        return 200, servicios_clientes.listar_clientes()

    if ruta == "/api/pedidos":
        return 200, servicios_pedidos.listar_pedidos()

    raise ValueError("La ruta solicitada no existe.")


def crear_recurso(ruta, datos):
    """
    Atiende las solicitudes POST.
    """
    if ruta == "/api/productos":
        producto_id = servicios_productos.registrar_producto(
            nombre=datos.get("nombre", ""),
            precio=datos.get("precio", 0),
            stock=datos.get("stock", 0),
        )

        return 201, {
            "mensaje": "Producto creado correctamente.",
            "id": producto_id,
        }

    if ruta == "/api/clientes":
        cliente_id = servicios_clientes.registrar_cliente(
            nombre=datos.get("nombre", ""),
            correo=datos.get("correo", ""),
        )

        return 201, {
            "mensaje": "Cliente creado correctamente.",
            "id": cliente_id,
        }

    if ruta == "/api/pedidos":
        pedido = servicios_pedidos.crear_pedido(
            cliente_id=datos.get("cliente_id"),
            items=datos.get("items", []),
            devpoints_a_redimir=datos.get(
                "devpoints_a_redimir",
                0,
            ),
        )

        return 201, pedido

    raise ValueError("La ruta solicitada no existe.")


def actualizar_recurso(ruta, datos):
    """
    Atiende las solicitudes PATCH.
    """
    partes = ruta.strip("/").split("/")

    if (
        len(partes) == 4
        and partes[0] == "api"
        and partes[1] == "pedidos"
        and partes[3] == "estado"
    ):
        pedido_id = int(partes[2])

        pedido = servicios_pedidos.cambiar_estado(
            pedido_id=pedido_id,
            nuevo_estado=datos.get("estado", ""),
        )

        return 200, pedido

    raise ValueError("La ruta solicitada no existe.")