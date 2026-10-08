from .conexion import obtener_conexion


def contar_pedidos_por_cliente_y_estado(cliente_id, estado):
    """
    Cuenta los pedidos de un cliente que tienen un estado específico.
    """
    with obtener_conexion() as conexion:
        consulta = """
            SELECT COUNT(*) AS cantidad
            FROM pedidos
            WHERE cliente_id = ?
              AND estado = ?
        """
        fila = conexion.execute(
            consulta,
            (cliente_id, estado)
        ).fetchone()

        return fila["cantidad"]


def crear_pedido(
    cliente_id,
    estado,
    subtotal,
    descuento_nivel,
    descuento_devpoints,
    total,
    fecha
):
    """
    Guarda un pedido con sus valores ya calculados por la capa de negocio.
    """
    with obtener_conexion() as conexion:
        consulta = """
            INSERT INTO pedidos (
                cliente_id,
                estado,
                subtotal,
                descuento_nivel,
                descuento_devpoints,
                total,
                fecha
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor = conexion.execute(
            consulta,
            (
                cliente_id,
                estado,
                subtotal,
                descuento_nivel,
                descuento_devpoints,
                total,
                fecha,
            )
        )

        return cursor.lastrowid


def crear_item_pedido(
    pedido_id,
    producto_id,
    cantidad,
    precio_unitario
):
    """
    Guarda un producto dentro de un pedido.
    """
    with obtener_conexion() as conexion:
        consulta = """
            INSERT INTO pedido_items (
                pedido_id,
                producto_id,
                cantidad,
                precio_unitario
            )
            VALUES (?, ?, ?, ?)
        """

        cursor = conexion.execute(
            consulta,
            (
                pedido_id,
                producto_id,
                cantidad,
                precio_unitario,
            )
        )

        return cursor.lastrowid


def listar_pedidos():
    """
    Devuelve todos los pedidos registrados.
    """
    with obtener_conexion() as conexion:
        consulta = """
            SELECT
                p.id,
                p.cliente_id,
                c.nombre AS cliente_nombre,
                p.estado,
                p.subtotal,
                p.descuento_nivel,
                p.descuento_devpoints,
                p.total,
                p.fecha
            FROM pedidos AS p
            INNER JOIN clientes AS c
                ON c.id = p.cliente_id
            ORDER BY p.fecha DESC, p.id DESC
        """

        filas = conexion.execute(consulta).fetchall()
        return [dict(fila) for fila in filas]


def obtener_pedido(pedido_id):
    """
    Devuelve un pedido junto con sus productos.
    """
    with obtener_conexion() as conexion:
        consulta_pedido = """
            SELECT
                p.id,
                p.cliente_id,
                c.nombre AS cliente_nombre,
                p.estado,
                p.subtotal,
                p.descuento_nivel,
                p.descuento_devpoints,
                p.total,
                p.fecha
            FROM pedidos AS p
            INNER JOIN clientes AS c
                ON c.id = p.cliente_id
            WHERE p.id = ?
        """

        pedido = conexion.execute(
            consulta_pedido,
            (pedido_id,)
        ).fetchone()

        if pedido is None:
            return None

        consulta_items = """
            SELECT
                pi.id,
                pi.producto_id,
                pr.nombre AS producto_nombre,
                pi.cantidad,
                pi.precio_unitario
            FROM pedido_items AS pi
            INNER JOIN productos AS pr
                ON pr.id = pi.producto_id
            WHERE pi.pedido_id = ?
        """

        items = conexion.execute(
            consulta_items,
            (pedido_id,)
        ).fetchall()

        resultado = dict(pedido)
        resultado["items"] = [dict(item) for item in items]

        return resultado


def actualizar_estado(pedido_id, nuevo_estado):
    """
    Actualiza el estado de un pedido.
    """
    with obtener_conexion() as conexion:
        consulta = """
            UPDATE pedidos
            SET estado = ?
            WHERE id = ?
        """

        cursor = conexion.execute(
            consulta,
            (nuevo_estado, pedido_id)
        )

        return cursor.rowcount > 0