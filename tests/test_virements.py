import unittest

from contoso_paiements import virements


class TestPlafond(unittest.TestCase):
    def test_virement_sous_le_plafond_retourne_le_restant(self):
        self.assertEqual(virements.verifier_plafond(100_000, 50_000), 350_000)

    def test_virement_qui_atteint_exactement_le_plafond_est_accepte(self):
        self.assertEqual(virements.verifier_plafond(200_000, 300_000), 0)

    def test_virement_au_dela_du_plafond_est_refuse(self):
        with self.assertRaises(virements.VirementRefuse) as contexte:
            virements.verifier_plafond(200_000, 400_000)
        self.assertIn("1\u202f000,00\u00a0€", str(contexte.exception))

    def test_montant_non_entier_est_refuse(self):
        for montant in (10.5, "100", True, None):
            with self.subTest(montant=montant):
                with self.assertRaises(virements.VirementRefuse):
                    virements.verifier_plafond(montant, 0)

    def test_montant_nul_ou_negatif_est_refuse(self):
        for montant in (0, -1):
            with self.subTest(montant=montant):
                with self.assertRaises(virements.VirementRefuse):
                    virements.verifier_plafond(montant, 0)


class TestFormatage(unittest.TestCase):
    def test_formater_euros(self):
        self.assertEqual(virements.formater_euros(123_456), "1\u202f234,56\u00a0€")
        self.assertEqual(virements.formater_euros(5), "0,05\u00a0€")
        self.assertEqual(virements.formater_euros(-250), "-2,50\u00a0€")


class TestIban(unittest.TestCase):
    def test_iban_valides(self):
        self.assertTrue(virements.iban_valide("FR76 3000 6000 0112 3456 7890 189"))
        self.assertTrue(virements.iban_valide("DE89370400440532013000"))

    def test_iban_invalides(self):
        for iban in ("FR76 3000 6000 0112 3456 7890 188", "", "FR", "1234567890123456"):
            with self.subTest(iban=iban):
                self.assertFalse(virements.iban_valide(iban))


if __name__ == "__main__":
    unittest.main()
