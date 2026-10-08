from .conexion import obtener_conexion


def listar_clientes():
    """
    Devuelve todos los clientes registrados.
    """
    with obtener_conexion() as conexion:
        consulta = """
            SELECT
                id,
                nombre,
                correo,
                nivel,
                devpoints,
                compras_acumuladas
            FROM clientes
            ORDER BY nombre
        """
        filas = conexion.execute(consulta).fetchall()
        return [dict(fila) for fila in filas]


def obtener_cliente(cliente_id):
    """
    Devuelve un cliente por su identificador.
    """
    with obtener_conexion() as conexion:
        consulta = """
            SELECT
                id,
                nombre,
                correo,
                nivel,
                devpoints,
                compras_acumuladas
            FROM clientes
            WHERE id = ?
        """
        fila = conexion.execute(consulta, (cliente_id,)).fetchone()
        return dict(fila) if fila else None


def crear_cliente(nombre, correo):
    """
    Crea un cliente nuevo con nivel Junior y cero DevPoints.
    """
    with obtener_conexion() as conexion:
        consulta = """
            INSERT INTO clientes (
                nombre,
                correo,
                nivel,
                devpoints,
                compras_acumuladas
            )
            VALUES (?, ?, 'Junior', 0, 0)
        """
        cursor = conexion.execute(consulta, (nombre, correo))
        return cursor.lastrowid


def actualizar_lealtad(
    cliente_id,
    nivel,
    devpoints,
    compras_acumuladas
):
    """
    Actualiza los datos de lealtad de un cliente.
    """
    with obtener_conexion() as conexion:
        consulta = """
            UPDATE clientes
            SET
                nivel = ?,
                devpoints = ?,
                compras_acumuladas = ?
            WHERE id = ?
        """
        cursor = conexion.execute(
            consulta,
            (
                nivel,
                devpoints,
                compras_acumuladas,
                cliente_id,
            )
        )
        return cursor.rowcount > 0