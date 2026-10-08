DESCUENTOS_POR_NIVEL = {
    "Junior": 5,
    "Mid": 10,
    "Senior": 15,
}

UMBRAL_MID = 500_000
UMBRAL_SENIOR = 1_500_000
VALOR_POR_DEVPOINT = 200
CONSUMO_POR_DEVPOINT = 20_000


def obtener_porcentaje_descuento(nivel):
    """
    Devuelve el porcentaje de descuento según el nivel del cliente.
    """
    if nivel not in DESCUENTOS_POR_NIVEL:
        raise ValueError(f"Nivel de cliente no válido: {nivel}")

    return DESCUENTOS_POR_NIVEL[nivel]


def calcular_descuento_por_nivel(subtotal, nivel):
    """
    Calcula el descuento correspondiente al nivel del cliente.
    """
    porcentaje = obtener_porcentaje_descuento(nivel)
    return subtotal * porcentaje // 100


def calcular_descuento_por_devpoints(devpoints_a_redimir):
    """
    Convierte DevPoints redimidos en dinero de descuento.
    """
    if devpoints_a_redimir < 0:
        raise ValueError("No se pueden redimir DevPoints negativos.")

    return devpoints_a_redimir * VALOR_POR_DEVPOINT


def calcular_devpoints_ganados(monto_consumido):
    """
    Calcula los DevPoints ganados por un pedido completado.
    """
    if monto_consumido < 0:
        raise ValueError("El monto consumido no puede ser negativo.")

    return monto_consumido // CONSUMO_POR_DEVPOINT


def calcular_nivel_por_compras(compras_acumuladas):
    """
    Determina el nivel de lealtad según las compras acumuladas.
    """
    if compras_acumuladas < 0:
        raise ValueError(
            "Las compras acumuladas no pueden ser negativas."
        )

    if compras_acumuladas >= UMBRAL_SENIOR:
        return "Senior"

    if compras_acumuladas >= UMBRAL_MID:
        return "Mid"

    return "Junior"


def calcular_total(subtotal, descuento_nivel, descuento_devpoints):
    """
    Calcula el total final sin permitir valores negativos.
    """
    total = subtotal - descuento_nivel - descuento_devpoints
    return max(total, 0)