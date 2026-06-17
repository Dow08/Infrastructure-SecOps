#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova Syndicate — Script d'automatisation #1
============================================
Création automatisée de comptes utilisateurs Samba 4 Active Directory
depuis un fichier CSV.

Auteur     : Dorian Poncelet — Nova Syndicate
Date       : Mai 2026
Version    : 1.0
Cible      : DC01-Lyon (Samba 4 AD-DC sur Debian 12)
Référence  : NS-2026-006-script-01

OBJECTIF
--------
Provisionner massivement les 85 comptes collaborateurs Nova Syndicate
dans l'annuaire AD sans intervention manuelle, en respectant la politique
de groupes / mots de passe / unités organisationnelles (OU) définie.

JUSTIFICATION
-------------
La création manuelle de 85 comptes via samba-tool prendrait ~4 heures
et serait sujette aux erreurs de frappe. Ce script industrialise le
processus en 5 minutes, garantit l'idempotence (relance possible sans
duplication), et trace chaque action dans un log auditable.

USAGE
-----
Préparer un fichier CSV `users.csv` avec les colonnes :
    username,firstname,lastname,email,department,manager,site

Exécution :
    sudo python3 create_ad_users.py --csv users.csv [--dry-run]

Options :
    --csv FILE     Chemin du fichier CSV source (obligatoire)
    --dry-run      Simulation sans création (validation)
    --log FILE     Fichier de log personnalisé (par défaut /var/log/nova/create_users.log)
    --domain DOM   Domaine AD (par défaut nova.local)

DÉPENDANCES
-----------
- Python 3.9+
- samba-tool installé et configuré (Samba 4 AD-DC opérationnel)
- Droits root requis (samba-tool appelle des opérations privilégiées)

EXEMPLE DE CSV
--------------
username,firstname,lastname,email,department,manager,site
alice.martin,Alice,MARTIN,alice.martin@nova.local,Commercial,jean.dupont,Lyon
bob.durand,Bob,DURAND,bob.durand@nova.local,Logistique,marie.petit,Marseille
charlie.roy,Charlie,ROY,charlie.roy@nova.local,IT,jean.dupont,Lyon

LICENCE
-------
Usage interne Nova Syndicate uniquement. Diffusion soumise à autorisation.
"""

import argparse
import csv
import logging
import os
import secrets
import string
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────────────────────
# Configuration globale
# ─────────────────────────────────────────────────────────────
DEFAULT_DOMAIN = "nova.local"
DEFAULT_LOG_FILE = "/var/log/nova/create_users.log"
PASSWORD_LENGTH = 16            # Longueur des mots de passe initiaux
PASSWORD_MUST_CHANGE = True     # Force le changement à la première connexion

# Mapping département → Organizational Unit AD
# Permet la structuration logique de l'annuaire (utile pour les GPO)
DEPARTMENT_TO_OU = {
    "Commercial": "OU=Commercial,OU=NovaUsers,DC=nova,DC=local",
    "Logistique": "OU=Logistique,OU=NovaUsers,DC=nova,DC=local",
    "IT":         "OU=IT,OU=NovaUsers,DC=nova,DC=local",
    "Direction":  "OU=Direction,OU=NovaUsers,DC=nova,DC=local",
    "R&D":        "OU=R&D,OU=NovaUsers,DC=nova,DC=local",
}

# Mapping département → groupe AD principal
DEPARTMENT_TO_GROUP = {
    "Commercial": "Commerciaux",
    "Logistique": "Logistique",
    "IT":         "IT-Admins",
    "Direction":  "Direction",
    "R&D":        "R&D",
}


# ─────────────────────────────────────────────────────────────
# Fonctions utilitaires
# ─────────────────────────────────────────────────────────────

def setup_logging(log_path: str) -> logging.Logger:
    """
    Initialise le système de log avec rotation simple (timestamp à chaque ligne).
    Le log est essentiel pour la traçabilité et l'audit RGPD.
    """
    # Création du dossier de log si nécessaire
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("nova_create_users")
    logger.setLevel(logging.INFO)

    # Handler fichier
    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )

    # Handler console (stdout) pour suivi interactif
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("[%(levelname)s] %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def generate_password(length: int = PASSWORD_LENGTH) -> str:
    """
    Génère un mot de passe initial cryptographiquement sûr.

    Le module `secrets` est utilisé plutôt que `random` car il utilise
    le générateur d'aléa du système d'exploitation (urandom) et est
    explicitement conçu pour les usages sécuritaires (PEP 506).

    Caractéristiques garantissant la conformité aux politiques AD :
    - 1 majuscule minimum
    - 1 minuscule minimum
    - 1 chiffre minimum
    - 1 caractère spécial minimum
    - 16 caractères au total
    """
    while True:
        alphabet = string.ascii_letters + string.digits + "!@#$%&*+-="
        password = "".join(secrets.choice(alphabet) for _ in range(length))

        # Vérification des prérequis de complexité AD
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%&*+-=" for c in password)
        ):
            return password


def check_prerequisites(logger: logging.Logger) -> bool:
    """
    Vérifie que les prérequis sont remplis avant exécution.

    - Droits root (sudo)
    - samba-tool installé et dans le PATH
    - Le domaine Samba est joignable
    """
    if os.geteuid() != 0:
        logger.error("Ce script doit être exécuté en root (sudo).")
        return False

    # Vérification présence samba-tool
    try:
        subprocess.run(
            ["samba-tool", "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        logger.error("samba-tool n'est pas installé ou inaccessible.")
        return False

    # Vérification accessibilité du domaine
    try:
        result = subprocess.run(
            ["samba-tool", "domain", "info", DEFAULT_DOMAIN],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        logger.info(f"Domaine AD opérationnel : {DEFAULT_DOMAIN}")
    except subprocess.CalledProcessError:
        logger.error(f"Impossible d'interroger le domaine {DEFAULT_DOMAIN}.")
        return False

    return True


def user_exists(username: str, logger: logging.Logger) -> bool:
    """
    Vérifie si un utilisateur existe déjà dans l'AD.
    Permet l'idempotence du script (relance possible sans erreur).
    """
    try:
        result = subprocess.run(
            ["samba-tool", "user", "show", username],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout lors de la vérification d'existence de {username}.")
        return False


def create_user(
    username: str,
    firstname: str,
    lastname: str,
    email: str,
    department: str,
    site: str,
    password: str,
    logger: logging.Logger,
    dry_run: bool = False,
) -> bool:
    """
    Crée un utilisateur Samba AD.

    Retourne True si succès, False sinon.
    """
    # Construction de la commande samba-tool
    cmd = [
        "samba-tool", "user", "create",
        username, password,
        f"--given-name={firstname}",
        f"--surname={lastname}",
        f"--mail-address={email}",
        f"--department={department}",
        f"--description=Site {site} - Créé automatiquement le "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    # Ajout de l'OU si le département est mappé
    if department in DEPARTMENT_TO_OU:
        cmd.append(f"--userou={DEPARTMENT_TO_OU[department]}")

    # Force le changement de mot de passe à la première connexion
    if PASSWORD_MUST_CHANGE:
        cmd.append("--must-change-at-next-login")

    if dry_run:
        logger.info(f"[DRY-RUN] Aurait créé : {username} ({firstname} {lastname})")
        return True

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            logger.info(f"Utilisateur créé : {username}")
            return True
        else:
            logger.error(
                f"Échec création {username} : {result.stderr.strip()}"
            )
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout lors de la création de {username}.")
        return False


def add_user_to_group(
    username: str,
    group: str,
    logger: logging.Logger,
    dry_run: bool = False,
) -> bool:
    """
    Ajoute un utilisateur à un groupe AD.
    Si le groupe n'existe pas, il est créé automatiquement.
    """
    if dry_run:
        logger.info(f"[DRY-RUN] Aurait ajouté {username} au groupe {group}")
        return True

    # Vérifier si le groupe existe, sinon le créer
    check = subprocess.run(
        ["samba-tool", "group", "show", group],
        capture_output=True,
        text=True,
        timeout=5,
    )
    if check.returncode != 0:
        logger.info(f"Création du groupe {group} (n'existait pas)")
        subprocess.run(
            ["samba-tool", "group", "add", group],
            capture_output=True,
            text=True,
            timeout=5,
        )

    # Ajout de l'utilisateur au groupe
    cmd = ["samba-tool", "group", "addmembers", group, username]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info(f"{username} ajouté au groupe {group}")
            return True
        else:
            logger.warning(
                f"Impossible d'ajouter {username} à {group} : "
                f"{result.stderr.strip()}"
            )
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout lors de l'ajout de {username} au groupe {group}.")
        return False


def write_password_file(
    passwords: dict,
    output_path: str = "/root/nova_initial_passwords.csv",
) -> None:
    """
    Enregistre les mots de passe initiaux dans un fichier sécurisé.

    Ce fichier doit être :
    - Chiffré (option : gpg --encrypt après génération).
    - Distribué aux utilisateurs par canal sécurisé (email signé, en main propre).
    - Supprimé après distribution (force change at next login = vérifié).
    """
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "initial_password"])
        for user, pwd in passwords.items():
            writer.writerow([user, pwd])

    # Permissions restrictives (root uniquement)
    os.chmod(output_path, 0o600)


# ─────────────────────────────────────────────────────────────
# Programme principal
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Création batch utilisateurs AD Nova Syndicate"
    )
    parser.add_argument("--csv", required=True, help="Fichier CSV des utilisateurs")
    parser.add_argument("--dry-run", action="store_true", help="Simulation")
    parser.add_argument("--log", default=DEFAULT_LOG_FILE, help="Fichier de log")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help="Domaine AD")
    args = parser.parse_args()

    logger = setup_logging(args.log)
    logger.info("=" * 60)
    logger.info(f"Démarrage script create_ad_users — mode {'DRY-RUN' if args.dry_run else 'PRODUCTION'}")
    logger.info("=" * 60)

    # Vérification des prérequis
    if not check_prerequisites(logger):
        logger.error("Prérequis non remplis. Arrêt.")
        sys.exit(1)

    # Lecture du fichier CSV
    if not Path(args.csv).is_file():
        logger.error(f"Fichier CSV introuvable : {args.csv}")
        sys.exit(1)

    # Compteurs pour rapport final
    stats = {"créés": 0, "ignorés": 0, "échoués": 0}
    generated_passwords = {}

    with open(args.csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row["username"].strip()
            firstname = row["firstname"].strip()
            lastname = row["lastname"].strip()
            email = row["email"].strip()
            department = row["department"].strip()
            site = row["site"].strip()

            # Vérification idempotence
            if user_exists(username, logger):
                logger.info(f"Utilisateur {username} existe déjà — ignoré.")
                stats["ignorés"] += 1
                continue

            # Génération du mot de passe initial
            password = generate_password()
            generated_passwords[username] = password

            # Création de l'utilisateur
            if create_user(
                username, firstname, lastname, email, department, site,
                password, logger, args.dry_run
            ):
                stats["créés"] += 1

                # Ajout au groupe correspondant au département
                if department in DEPARTMENT_TO_GROUP:
                    add_user_to_group(
                        username,
                        DEPARTMENT_TO_GROUP[department],
                        logger,
                        args.dry_run,
                    )
            else:
                stats["échoués"] += 1

    # Sauvegarde des mots de passe (uniquement en mode production)
    if not args.dry_run and generated_passwords:
        write_password_file(generated_passwords)
        logger.info(
            "Mots de passe initiaux enregistrés dans "
            "/root/nova_initial_passwords.csv (mode 600)."
        )
        logger.warning(
            "ACTION REQUISE : distribuer ces mots de passe par canal sécurisé "
            "et supprimer le fichier après distribution."
        )

    # Rapport final
    logger.info("=" * 60)
    logger.info(
        f"FIN — Créés: {stats['créés']} | "
        f"Ignorés: {stats['ignorés']} | "
        f"Échoués: {stats['échoués']}"
    )
    logger.info("=" * 60)

    # Code de sortie selon le résultat
    sys.exit(0 if stats["échoués"] == 0 else 2)


if __name__ == "__main__":
    main()
