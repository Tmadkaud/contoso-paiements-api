"""Règles métier des virements. Tous les montants sont des entiers en centimes."""

PLAFOND_JOURNALIER_CENTIMES = 500_000  # 5 000,00 €


class VirementRefuse(Exception):
    """Le virement ne respecte pas une règle métier."""


def valider_montant(montant_centimes):
    if not isinstance(montant_centimes, int) or isinstance(montant_centimes, bool):
        raise VirementRefuse("Le montant doit être un entier en centimes.")
    if montant_centimes <= 0:
        raise VirementRefuse("Le montant doit être strictement positif.")
    return montant_centimes


def verifier_plafond(montant_centimes, deja_vire_aujourdhui_centimes):
    """Retourne le montant encore disponible aujourd'hui après ce virement."""
    valider_montant(montant_centimes)
    total = deja_vire_aujourdhui_centimes + montant_centimes
    if total > PLAFOND_JOURNALIER_CENTIMES:
        restant = max(PLAFOND_JOURNALIER_CENTIMES - deja_vire_aujourdhui_centimes, 0)
        raise VirementRefuse(
            f"Plafond journalier dépassé : il reste {formater_euros(restant)} aujourd'hui."
        )
    return PLAFOND_JOURNALIER_CENTIMES - total


def formater_euros(centimes):
    euros, reste = divmod(abs(centimes), 100)
    signe = "-" if centimes < 0 else ""
    milliers = f"{euros:,}".replace(",", "\u202f")
    return f"{signe}{milliers},{reste:02d}\u00a0€"


def iban_valide(iban):
    """Contrôle de clé IBAN (ISO 13616, modulo 97)."""
    compact = "".join(iban.split()).upper()
    if len(compact) < 15 or len(compact) > 34 or not compact.isalnum():
        return False
    if not compact[:2].isalpha() or not compact[2:4].isdigit():
        return False
    reordonne = compact[4:] + compact[:4]
    chiffres = "".join(str(int(c, 36)) for c in reordonne)
    return int(chiffres) % 97 == 1
