"""API HTTP du service de paiements (bibliothèque standard uniquement)."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import historique, virements


class GestionnaireApi(BaseHTTPRequestHandler):
    connexion = None

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/sante":
            return self._json(200, {"statut": "ok"})
        if url.path == "/operations":
            parametres = parse_qs(url.query)
            compte = parametres.get("compte", [""])[0]
            terme = parametres.get("q", [""])[0]
            lignes = historique.rechercher(self.connexion, compte, terme)
            operations = [
                {"libelle": libelle, "montant_centimes": montant, "jour": jour}
                for libelle, montant, jour in lignes
            ]
            return self._json(200, {"operations": operations})
        return self._json(404, {"erreur": "Ressource inconnue."})

    def do_POST(self):
        if urlparse(self.path).path != "/virements":
            return self._json(404, {"erreur": "Ressource inconnue."})
        try:
            longueur = int(self.headers.get("Content-Length", "0"))
            corps = json.loads(self.rfile.read(longueur) or b"{}")
            compte = str(corps["compte"])
            montant = corps["montant_centimes"]
            jour = str(corps["jour"])
            deja_vire = historique.total_du_jour(self.connexion, compte, jour)
            restant = virements.verifier_plafond(montant, deja_vire)
        except virements.VirementRefuse as refus:
            return self._json(422, {"erreur": str(refus)})
        except (KeyError, TypeError, ValueError):
            return self._json(400, {"erreur": "Requête invalide."})
        libelle = str(corps.get("libelle", "Virement"))
        historique.enregistrer(self.connexion, compte, libelle, montant, jour)
        return self._json(201, {"statut": "accepté", "restant_centimes": restant})

    def _json(self, statut, donnees):
        corps = json.dumps(donnees, ensure_ascii=False).encode("utf-8")
        self.send_response(statut)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)

    def log_message(self, format, *args):
        pass


def creer_serveur(port=8000, connexion=None):
    GestionnaireApi.connexion = connexion or historique.ouvrir()
    return ThreadingHTTPServer(("127.0.0.1", port), GestionnaireApi)


if __name__ == "__main__":
    serveur = creer_serveur()
    print("API Contoso Paiements : http://127.0.0.1:8000/sante")
    serveur.serve_forever()
