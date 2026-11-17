import unittest

from contoso_paiements import historique


class TestHistorique(unittest.TestCase):
    def setUp(self):
        self.connexion = historique.ouvrir()
        historique.enregistrer(self.connexion, "C001", "Loyer novembre", 90_000, "2026-11-17")
        historique.enregistrer(self.connexion, "C001", "Courses", 12_550, "2026-11-17")
        historique.enregistrer(self.connexion, "C001", "Loyer octobre", 90_000, "2026-10-17")
        historique.enregistrer(self.connexion, "C002", "Loyer novembre", 70_000, "2026-11-17")

    def tearDown(self):
        self.connexion.close()

    def test_total_du_jour_par_compte(self):
        self.assertEqual(historique.total_du_jour(self.connexion, "C001", "2026-11-17"), 102_550)
        self.assertEqual(historique.total_du_jour(self.connexion, "C003", "2026-11-17"), 0)

    def test_rechercher_par_libelle(self):
        resultats = historique.rechercher(self.connexion, "C001", "Loyer")
        self.assertEqual([libelle for libelle, _, _ in resultats], ["Loyer novembre", "Loyer octobre"])


if __name__ == "__main__":
    unittest.main()
