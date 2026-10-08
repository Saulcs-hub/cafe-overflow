from .conexion import obtener_conexion


def listar_productos():
    """
    Devuelve todos los productos registrados.
    """
    with obtener_conexion() as conexion:
        consulta = """
            SELECT id, nombre, precio, stock
            FROM productos
            ORDER BY nombre
        """
        filas = conexion.execute(consulta).fetchall()
        return [dict(fila) for fila in filas]


def obtener_producto(producto_id):
    """
    Devuelve un producto por su identificador.
    """
    with obtener_conexion() as conexion:
        consulta = """
            SELECT id, nombre, precio, stock
            FROM productos
            WHERE id = ?
        """
        fila = conexion.execute(consulta, (producto_id,)).fetchone()
        return dict(fila) if fila else None


def crear_producto(nombre, precio, stock):
    """
    Guarda un nuevo producto y devuelve su identificador.
    """
    with obtener_conexion() as conexion:
        consulta = """
            INSERT INTO productos (nombre, precio, stock)
            VALUES (?, ?, ?)
        """
        cursor = conexion.execute(consulta, (nombre, precio, stock))
        return cursor.lastrowid


def actualizar_stock(producto_id, nuevo_stock):
    """
    Actualiza el stock de un producto.
    """
    with obtener_conexion() as conexion:
        consulta = """
            UPDATE productos
            SET stock = ?
            WHERE id = ?
        """
        cursor = conexion.execute(consulta, (nuevo_stock, producto_id))
        return cursor.rowcount > 0