from persistencia import cliente_dao
from negocio import reglas_lealtad


def listar_clientes():
    """
    Obtiene todos los clientes registrados.
    """
    return cliente_dao.listar_clientes()


def obtener_cliente(cliente_id):
    """
    Obtiene un cliente por su identificador.
    """
    cliente = cliente_dao.obtener_cliente(cliente_id)

    if cliente is None:
        raise ValueError("El cliente no existe.")

    return cliente


def registrar_cliente(nombre, correo):
    """
    Valida y registra un cliente nuevo.
    """
    nombre = nombre.strip()
    correo = correo.strip().lower()

    if not nombre:
        raise ValueError("El nombre del cliente es obligatorio.")

    if not correo or "@" not in correo:
        raise ValueError("El correo electrónico no es válido.")

    return cliente_dao.crear_cliente(nombre, correo)


def actualizar_lealtad_por_compra(
    cliente_id,
    monto_consumido,
    devpoints_redimidos=0
):
    """
    Actualiza compras, DevPoints y nivel después de completar un pedido.
    """
    cliente = obtener_cliente(cliente_id)

    if monto_consumido < 0:
        raise ValueError("El monto consumido no puede ser negativo.")

    if devpoints_redimidos < 0:
        raise ValueError(
            "Los DevPoints redimidos no pueden ser negativos."
        )

    devpoints_ganados = reglas_lealtad.calcular_devpoints_ganados(
        monto_consumido
    )

    devpoints_actuales = cliente["devpoints"]

    if devpoints_redimidos > devpoints_actuales:
        raise ValueError("El cliente no tiene suficientes DevPoints.")

    nuevos_devpoints = (
        devpoints_actuales
        - devpoints_redimidos
        + devpoints_ganados
    )

    nuevas_compras = (
        cliente["compras_acumuladas"]
        + monto_consumido
    )

    nuevo_nivel = reglas_lealtad.calcular_nivel_por_compras(
        nuevas_compras
    )

    actualizado = cliente_dao.actualizar_lealtad(
        cliente_id=cliente_id,
        nivel=nuevo_nivel,
        devpoints=nuevos_devpoints,
        compras_acumuladas=nuevas_compras,
    )

    if not actualizado:
        raise ValueError(
            "No se pudo actualizar la información de lealtad."
        )

    return cliente_dao.obtener_cliente(cliente_id)