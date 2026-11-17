import json
import threading
import unittest
import urllib.error
import urllib.request

from contoso_paiements import api, historique


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serveur = api.creer_serveur(port=0, connexion=historique.ouvrir())
        cls.base = f"http://127.0.0.1:{cls.serveur.server_address[1]}"
        cls.fil = threading.Thread(target=cls.serveur.serve_forever, daemon=True)
        cls.fil.start()

    @classmethod
    def tearDownClass(cls):
        cls.serveur.shutdown()
        cls.serveur.server_close()

    def appeler(self, methode, chemin, donnees=None):
        corps = json.dumps(donnees).encode("utf-8") if donnees is not None else None
        requete = urllib.request.Request(self.base + chemin, data=corps, method=methode)
        requete.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(requete, timeout=5) as reponse:
                return reponse.status, json.loads(reponse.read())
        except urllib.error.HTTPError as erreur:
            return erreur.code, json.loads(erreur.read())

    def test_sante(self):
        self.assertEqual(self.appeler("GET", "/sante"), (200, {"statut": "ok"}))

    def test_virement_accepte_puis_plafond_atteint(self):
        virement = {"compte": "A001", "montant_centimes": 400_000, "jour": "2026-11-17", "libelle": "Apport"}
        statut, reponse = self.appeler("POST", "/virements", virement)
        self.assertEqual(statut, 201)
        self.assertEqual(reponse["restant_centimes"], 100_000)

        statut, reponse = self.appeler("POST", "/virements", dict(virement, montant_centimes=150_000))
        self.assertEqual(statut, 422)
        self.assertIn("Plafond journalier dépassé", reponse["erreur"])

    def test_virement_invalide(self):
        statut, _ = self.appeler("POST", "/virements", {"compte": "A002"})
        self.assertEqual(statut, 400)

    def test_recherche_des_operations(self):
        virement = {"compte": "A003", "montant_centimes": 1_000, "jour": "2026-11-17", "libelle": "Cotisation"}
        self.appeler("POST", "/virements", virement)
        statut, reponse = self.appeler("GET", "/operations?compte=A003&q=Coti")
        self.assertEqual(statut, 200)
        self.assertEqual(reponse["operations"][0]["libelle"], "Cotisation")


if __name__ == "__main__":
    unittest.main()
