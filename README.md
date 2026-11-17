# contoso-paiements-api

Service de paiements de **Contoso Banque**, dépôt d'exemple de l'atelier [« Usine logicielle agentique »](https://github.com/Tmadkaud/atelier-usine-agentique). Données et entreprise fictives.

> Ce dépôt contient volontairement des défauts pour l'atelier : une faille de sécurité à trouver avec le code scanning, et (sur la branche `demo/ci-cassee`) un test en échec à réparer avec Agent Merge.

## Lancer

```shell
python -m unittest discover -s tests -t . -v   # tests
python -m contoso_paiements.api                # API sur http://127.0.0.1:8000
```

Python 3.12, bibliothèque standard uniquement.

## API

| Méthode | Chemin | Rôle |
| --- | --- | --- |
| `GET` | `/sante` | État du service |
| `POST` | `/virements` | Virement `{compte, montant_centimes, jour, libelle}` ; refusé (422) au-delà du plafond journalier |
| `GET` | `/operations?compte=…&q=…` | Recherche dans l'historique |

## Garde-fous des agents

`.github/hooks/garde-fous.json` déclenche `.github/hooks/garde-fous.mjs` avant chaque outil utilisé par un agent Copilot (Copilot app et Copilot CLI) : actions destructrices refusées, zones sensibles soumises à validation humaine. Node.js 20 ou plus est requis.
