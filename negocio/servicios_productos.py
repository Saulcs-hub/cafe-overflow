from persistencia import producto_dao


def listar_productos():
    """
    Obtiene todos los productos disponibles.
    """
    return producto_dao.listar_productos()


def obtener_producto(producto_id):
    """
    Obtiene un producto por su identificador.
    """
    producto = producto_dao.obtener_producto(producto_id)

    if producto is None:
        raise ValueError("El producto no existe.")

    return producto


def registrar_producto(nombre, precio, stock):
    """
    Valida y registra un producto nuevo.
    """
    nombre = nombre.strip()

    if not nombre:
        raise ValueError("El nombre del producto es obligatorio.")

    if precio < 0:
        raise ValueError("El precio no puede ser negativo.")

    if stock < 0:
        raise ValueError("El stock no puede ser negativo.")

    return producto_dao.crear_producto(nombre, precio, stock)


def cambiar_stock(producto_id, nuevo_stock):
    """
    Valida y actualiza el stock de un producto.
    """
    obtener_producto(producto_id)

    if nuevo_stock < 0:
        raise ValueError("El stock no puede ser negativo.")

    actualizado = producto_dao.actualizar_stock(
        producto_id,
        nuevo_stock
    )

    if not actualizado:
        raise ValueError("No se pudo actualizar el stock.")

    return True