import unittest

from contoso_paiements.frais import calculer_frais_instantane


class TestFraisInstantane(unittest.TestCase):
    def test_frais_simples(self):
        self.assertEqual(calculer_frais_instantane(10_000), 50)

    def test_arrondi_au_centime_le_plus_proche(self):
        self.assertEqual(calculer_frais_instantane(1_999), 10)
        self.assertEqual(calculer_frais_instantane(100), 1)
        self.assertEqual(calculer_frais_instantane(80), 0)

    def test_frais_plafonnes(self):
        self.assertEqual(calculer_frais_instantane(1_000_000), 1_000)

    def test_montant_invalide(self):
        with self.assertRaises(ValueError):
            calculer_frais_instantane(0)


if __name__ == "__main__":
    unittest.main()
