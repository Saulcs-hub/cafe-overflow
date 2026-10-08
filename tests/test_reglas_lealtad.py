import unittest

from negocio import reglas_lealtad


class TestReglasLealtad(unittest.TestCase):

    def test_descuento_junior(self):
        descuento = reglas_lealtad.calcular_descuento_por_nivel(
            10000,
            "Junior",
        )

        self.assertEqual(descuento, 500)

    def test_descuento_mid(self):
        descuento = reglas_lealtad.calcular_descuento_por_nivel(
            10000,
            "Mid",
        )

        self.assertEqual(descuento, 1000)

    def test_descuento_senior(self):
        descuento = reglas_lealtad.calcular_descuento_por_nivel(
            10000,
            "Senior",
        )

        self.assertEqual(descuento, 1500)

    def test_ascenso_a_mid(self):
        nivel = reglas_lealtad.calcular_nivel_por_compras(
            500000
        )

        self.assertEqual(nivel, "Mid")

    def test_ascenso_a_senior(self):
        nivel = reglas_lealtad.calcular_nivel_por_compras(
            1500000
        )

        self.assertEqual(nivel, "Senior")

    def test_devpoints_ganados(self):
        devpoints = reglas_lealtad.calcular_devpoints_ganados(
            40000
        )

        self.assertEqual(devpoints, 2)

    def test_valor_devpoints(self):
        descuento = reglas_lealtad.calcular_descuento_por_devpoints(
            3
        )

        self.assertEqual(descuento, 600)

    def test_total_no_negativo(self):
        total = reglas_lealtad.calcular_total(
            1000,
            800,
            500,
        )

        self.assertEqual(total, 0)


if __name__ == "__main__":
    unittest.main()