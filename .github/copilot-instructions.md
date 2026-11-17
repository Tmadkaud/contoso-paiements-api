# Instructions Copilot : contoso-paiements-api

Service de paiements de Contoso Banque (exemple d'atelier, données synthétiques). Python 3.12, bibliothèque standard uniquement.

## Règles métier
- Les montants sont toujours des **entiers en centimes**. Jamais de `float` pour de l'argent.
- Le plafond journalier de virement est vérifié côté serveur, même si l'interface le vérifie déjà.
- Les messages d'erreur destinés aux clients sont en français.

## Code
- Requêtes SQL toujours paramétrées (`?`), jamais construites par concaténation ou f-string.
- Pas de nouvelle dépendance externe sans validation humaine.
- Aucun secret, jeton ou donnée personnelle réelle dans le code, les tests ou les journaux.

## Tests
- Lancer : `python -m unittest discover -s tests -t . -v`
- Toute évolution de règle métier s'accompagne de tests (cas nominal, limite exacte, refus).

## Pull requests
- Suivre le modèle de PR et remplir la section « Preuves ».
- Lier l'issue (`Closes #N`). Ne jamais contourner les règles de fusion.
