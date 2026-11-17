"""Frais des virements instantanés : 0,5 % du montant, arrondis au centime le plus proche, plafonnés à 10,00 €."""

TAUX_POUR_MILLE = 5
PLAFOND_FRAIS_CENTIMES = 1_000


def calculer_frais_instantane(montant_centimes):
    if montant_centimes <= 0:
        raise ValueError("Le montant doit être strictement positif.")
    frais = int(montant_centimes * TAUX_POUR_MILLE / 1000)
    return min(frais, PLAFOND_FRAIS_CENTIMES)
