"""Historique des opérations (SQLite)."""

import sqlite3


def ouvrir(chemin=":memory:"):
    connexion = sqlite3.connect(chemin, check_same_thread=False)
    connexion.execute(
        "CREATE TABLE IF NOT EXISTS operations ("
        "id INTEGER PRIMARY KEY, compte TEXT NOT NULL, libelle TEXT NOT NULL, "
        "montant_centimes INTEGER NOT NULL, jour TEXT NOT NULL)"
    )
    return connexion


def enregistrer(connexion, compte, libelle, montant_centimes, jour):
    connexion.execute(
        "INSERT INTO operations (compte, libelle, montant_centimes, jour) VALUES (?, ?, ?, ?)",
        (compte, libelle, montant_centimes, jour),
    )
    connexion.commit()


def total_du_jour(connexion, compte, jour):
    ligne = connexion.execute(
        "SELECT COALESCE(SUM(montant_centimes), 0) FROM operations WHERE compte = ? AND jour = ?",
        (compte, jour),
    ).fetchone()
    return ligne[0]


def rechercher(connexion, compte, terme):
    requete = (
        "SELECT libelle, montant_centimes, jour FROM operations "
        f"WHERE compte = '{compte}' AND libelle LIKE '%{terme}%' ORDER BY id"
    )
    return connexion.execute(requete).fetchall()
