#!/usr/bin/env python3
"""
generateur_registre_risques.py
-------------------------------
Génère un registre de risques pré-rempli adapté à un secteur d'activité.

Permet de démarrer une analyse de risque rapidement avec des scénarios
sectoriels typiques (déjà observés sur le terrain) que l'on adapte ensuite.

Usage:
    python generateur_registre_risques.py --secteur banque [--output registre.csv]

Secteurs supportés:
    banque, sante, industrie, retail, public, esn

Sortie: CSV format identique à templates/registre-risques.csv
"""

import csv
import argparse
import sys
from datetime import datetime


COLONNES = [
    "ID", "Date_identification", "Categorie", "Description", "Source_menace",
    "Actif", "Probabilite_inherente", "Impact_inherent", "Niveau_inherent",
    "Mesures_actuelles", "Probabilite_residuelle", "Impact_residuel", "Niveau_residuel",
    "Strategie_traitement", "Owner", "Date_revue", "Statut", "Commentaires"
]


def _date_today():
    return datetime.now().strftime("%Y-%m-%d")


# Risques transverses (présents dans tous les secteurs)
RISQUES_TRANSVERSES = [
    ("Cyber", "Phishing ciblé sur dirigeants (whaling) menant à compromission email", "Cybercriminels", "Messagerie + données financières", 4, 4, "16", "MFA + sensibilisation + DMARC", 2, 4, "8", "Réduire", "RSSI", "Sensibilisation renforcée Direction"),
    ("Cyber", "Ransomware paralysant la production via chiffrement de fichiers et sauvegardes", "Cybercriminels", "Systèmes production + backups", 4, 4, "16", "EDR + sauvegardes immuables + segmentation", 2, 4, "8", "Réduire", "RSSI", "Test restauration 3-2-1-1-0 trimestriel"),
    ("Cyber", "Compromission de compte privilégié (admin AD/cloud) via credential stuffing", "Cybercriminels", "Active Directory + Cloud", 3, 4, "12", "PAM + MFA + détection comportementale", 1, 4, "4", "Réduire", "DSI", "Tier-0 isolé"),
    ("Tiers", "Défaillance d'un fournisseur critique (SaaS, hébergeur, MSP)", "Externe", "Services dépendants du fournisseur", 3, 4, "12", "Clauses contractuelles + plan de sortie + multi-sourcing", 2, 3, "6", "Réduire", "Achats+RSSI", "Tiering fournisseurs en cours"),
    ("RH", "Départ d'un collaborateur clé sans transfert de connaissance", "Interne", "Compétences critiques", 3, 3, "9", "Documentation + binômage", 2, 2, "4", "Réduire", "RH", "Plan de succession à formaliser"),
    ("Conformité", "Sanction CNIL suite à violation de données personnelles non notifiée à temps", "Régulateur", "Données personnelles + image", 2, 4, "8", "Procédure 72h + DPO + registre", 1, 3, "3", "Réduire", "DPO", "RGPD art.33-34"),
    ("Continuité", "Indisponibilité longue d'un datacenter (incendie, inondation)", "Environnemental", "Production IT", 1, 4, "4", "DR multi-site + tests annuels", 1, 2, "2", "Transférer", "DSI", "Assurance + site de repli"),
    ("Cyber", "Exploitation d'une vulnérabilité zero-day sur application critique", "Cybercriminels", "Applications exposées", 3, 4, "12", "Veille CVE + WAF + virtual patching", 2, 3, "6", "Réduire", "RSSI", "SLA patch critique 30j"),
    ("Cyber", "Attaque sur la supply chain logicielle (dépendances malveillantes)", "Cybercriminels", "Code source + builds", 2, 4, "8", "SBOM + scan dépendances + signature", 1, 3, "3", "Réduire", "RSSI+Dev", "DevSecOps Trivy"),
    ("Cyber", "Vol ou perte de matériel mobile contenant des données sensibles", "Interne/Externe", "Postes mobiles + données", 3, 2, "6", "Chiffrement disque + MDM + revocation distance", 2, 1, "2", "Réduire", "DSI", "BitLocker/FileVault"),
]

# Risques sectoriels spécifiques
RISQUES_SECTEUR = {
    "banque": [
        ("Cyber", "Attaque sur le système SWIFT/paiements interbancaires", "Cybercriminels organisés", "Système de paiement", 2, 4, "8", "Ségrégation + 4-yeux + monitoring transactions", 1, 4, "4", "Réduire", "RSSI", "Conformité SWIFT CSP"),
        ("Cyber", "Fraude par ingénierie sociale (faux virement Président)", "Cybercriminels", "Trésorerie", 3, 4, "12", "Double validation virements > seuil + sensibilisation", 2, 3, "6", "Réduire", "DAF", "FIDA 2023"),
        ("Conformité", "Non-respect DORA - défaut tests TLPT triennaux", "Régulateur (ESA)", "Conformité réglementaire", 2, 3, "6", "Programme TLPT 2026 planifié + budget", 1, 2, "2", "Réduire", "RSSI", "DORA art.27"),
        ("Conformité", "Sanction ACPR pour défaut résilience opérationnelle", "Régulateur (ACPR)", "Licence bancaire", 2, 4, "8", "Programme DORA + reporting", 1, 3, "3", "Réduire", "Compliance", "Sanction jusqu'à 10% CA"),
        ("Cyber", "DDoS sur la banque en ligne durant période critique (paye, fêtes)", "Activistes/Cybercriminels", "Plateforme banque en ligne", 3, 3, "9", "Anti-DDoS Cloud + CDN + dimensionnement", 2, 2, "4", "Transférer", "DSI", "SLA opérateur"),
        ("Tiers", "Défaillance d'un prestataire TIC critique (cloud, paiement)", "Externe", "Services TIC critiques", 3, 4, "12", "Registre information DORA + stratégie sortie", 2, 3, "6", "Réduire", "Achats+RSSI", "DORA art.28-44"),
        ("Cyber", "Manipulation d'algorithmes de scoring (IA Act, biais discriminatoire)", "Régulateur + clients", "Modèles IA crédit", 2, 3, "6", "Gouvernance IA + audit modèles + explicabilité", 1, 3, "3", "Réduire", "RSSI+CTO", "AI Act EU"),
    ],
    "sante": [
        ("Cyber", "Ransomware paralysant le SIH (système d'information hospitalier)", "Cybercriminels", "Production hospitalière", 4, 4, "16", "EDR + segmentation + plan dégradé papier", 2, 4, "8", "Réduire", "RSSI", "Cible majeure 2024-2026"),
        ("Conformité", "Hébergement de données de santé sans certification HDS", "Régulateur (ANS)", "Conformité", 2, 4, "8", "Hébergeur HDS certifié + audit annuel", 1, 3, "3", "Réduire", "DPO+RSSI", "Décret 2018-137"),
        ("Cyber", "Compromission d'objets médicaux connectés (IoMT)", "Cybercriminels", "Dispositifs médicaux", 3, 4, "12", "VLAN dédié IoMT + inventaire + MAJ", 2, 3, "6", "Réduire", "Biomed+RSSI", "NIS2 secteur santé"),
        ("Conformité", "Sanction CNIL fuite massive de données de santé (art.9 RGPD)", "Régulateur (CNIL)", "Données patients", 3, 4, "12", "Chiffrement + DLP + traçabilité accès", 2, 3, "6", "Réduire", "DPO", "Données sensibles art.9"),
        ("Continuité", "Indisponibilité du SIH > 4h impactant les soins urgents", "Multiple", "Soins", 2, 4, "8", "DRP + procédure dégradée + tests semestriels", 1, 3, "3", "Réduire", "DSI", "Continuité soins"),
        ("Tiers", "Compromission via éditeur logiciel médical (supply chain)", "Cybercriminels", "Logiciels métier", 3, 4, "12", "Veille éditeurs + WAF + sécurité contractuelle", 2, 3, "6", "Réduire", "RSSI", "Type Solarwinds santé"),
    ],
    "industrie": [
        ("Cyber", "Compromission OT/ICS impactant la production (arrêt usine)", "Cybercriminels/État", "Systèmes industriels", 3, 4, "12", "Segmentation IT/OT + Purdue model + monitoring OT", 2, 3, "6", "Réduire", "RSSI+OT", "IEC 62443"),
        ("Cyber", "Espionnage industriel - vol de propriété intellectuelle", "Cyberespionnage", "R&D + brevets", 3, 4, "12", "Classification + DLP + accès strict + audit", 2, 3, "6", "Réduire", "RSSI+R&D", "État sponsorisé possible"),
        ("Continuité", "Indisponibilité fournisseur unique de composant critique", "Externe", "Production", 2, 4, "8", "Stock tampon + qualification 2ème source", 1, 3, "3", "Réduire", "Achats", "Single sourcing"),
        ("Cyber", "Sabotage interne par employé en fin de contrat", "Interne malveillant", "Production/données", 1, 4, "4", "Surveillance départs + revocation J+0", 1, 2, "2", "Réduire", "RH+RSSI", "Insider threat"),
        ("Conformité", "Non-conformité NIS2 - amende et atteinte image", "Régulateur (ANSSI)", "Conformité + image", 2, 3, "6", "Programme NIS2 en cours + désignation DPO/RSSI", 1, 2, "2", "Réduire", "RSSI", "Loi REVOSCYB 2024"),
        ("Cyber", "Falsification de paramètres procédé via PLC compromis", "Cybercriminels/État", "Sécurité industrielle", 1, 4, "4", "Hardening PLC + monitoring intégrité + 4-yeux", 1, 3, "3", "Réduire", "OT+RSSI", "Stuxnet-like"),
    ],
    "retail": [
        ("Cyber", "Vol de données bancaires clients via skimming front-end", "Cybercriminels", "Données paiement", 3, 4, "12", "PCI-DSS + WAF + tokenisation + monitoring", 2, 3, "6", "Réduire", "RSSI", "Magecart"),
        ("Cyber", "Compromission caisses (POS) via malware spécialisé", "Cybercriminels", "Terminaux POS", 3, 3, "9", "PCI-DSS + EDR + segmentation + AppLocker", 2, 2, "4", "Réduire", "RSSI", "BlackPOS, TrickBot"),
        ("Continuité", "Indisponibilité e-commerce durant Black Friday", "Multiple", "CA e-commerce", 3, 4, "12", "CDN + auto-scaling + tests charge + DR", 2, 3, "6", "Réduire", "DSI", "CA critique"),
        ("Conformité", "Sanction CNIL pour cookies publicitaires sans consentement", "Régulateur (CNIL)", "Conformité + image", 3, 3, "9", "CMP + audit cookies trimestriel", 2, 2, "4", "Réduire", "DPO", "100M€ Google 2021"),
        ("Cyber", "Fraude par création de faux comptes / abus promo (carding)", "Cybercriminels", "Marge commerciale", 4, 2, "8", "Anti-fraude + captcha + détection patterns", 2, 2, "4", "Accepter", "Métier+RSSI", "Coût acceptable"),
        ("Tiers", "Compromission d'un prestataire fidélité/CRM avec PII clients", "Externe", "Données clients", 3, 4, "12", "Due diligence + clauses art.28 + audit", 2, 3, "6", "Réduire", "DPO", "Image marque"),
    ],
    "public": [
        ("Cyber", "Cyberattaque ciblée État-nation sur services publics", "État adverse", "Services aux citoyens", 3, 4, "12", "ANSSI + segmentation + SOC + plan crise", 2, 3, "6", "Réduire", "RSSI", "Cible géopolitique"),
        ("Conformité", "Violation données fiscales/sociales (RGPD art.9)", "Multiple", "Données citoyens", 2, 4, "8", "Chiffrement + DLP + accès strict + revues", 1, 3, "3", "Réduire", "DPO", "Catégories spéciales"),
        ("Cyber", "Hacktivisme - défacement site institutionnel", "Activistes", "Image institutionnelle", 4, 2, "8", "WAF + bastion + monitoring", 2, 2, "4", "Réduire", "RSSI", "Image + désinformation"),
        ("Conformité", "Non-conformité RGS / référentiel sécurité État", "Régulateur (ANSSI)", "Homologation SI", 2, 3, "6", "Programme homologation + audit annuel", 1, 2, "2", "Réduire", "RSSI", "Décret RGS"),
        ("Continuité", "Indisponibilité service public critique > 24h", "Multiple", "Continuité service citoyen", 2, 4, "8", "DRP + procédure dégradée papier + tests", 1, 3, "3", "Réduire", "DSI", "Image publique"),
    ],
    "esn": [
        ("Tiers", "Fuite données client suite compromission interne", "Interne/Externe", "Données clients + image + contrats", 2, 4, "8", "Cloisonnement projets + traçabilité + clauses pénales", 1, 4, "4", "Réduire", "RSSI", "Réputation = survie"),
        ("Conformité", "Sanction client / résiliation pour défaut sécurité contractuel", "Client", "CA + image", 2, 4, "8", "ISO 27001 + audit clients + reporting", 1, 3, "3", "Réduire", "Commerce+RSSI", "B2B"),
        ("RH", "Départ d'un consultant clé avec data client sensible", "Interne", "Confidentialité client", 3, 3, "9", "NDA + offboarding strict + revocation J+0", 2, 2, "4", "Réduire", "RH+RSSI", "Tournover ESN élevé"),
        ("Cyber", "Attaque sur outils collaboration (Teams, Slack, Confluence) avec data multi-clients", "Cybercriminels", "Données clients", 3, 4, "12", "MFA + DLP + classification + audit accès", 2, 3, "6", "Réduire", "RSSI", "Cross-contamination"),
        ("Conformité", "Non-conformité NIS2 en tant qu'entité importante (fournisseur services TIC)", "Régulateur", "Continuité activité", 2, 3, "6", "Programme NIS2 + RSSI désigné", 1, 2, "2", "Réduire", "RSSI", "REVOSCYB"),
        ("Cyber", "Compromission d'un environnement de dev client (vol code source)", "Cybercriminels", "Code source clients", 2, 4, "8", "Environnements isolés + accès JIT + audit", 1, 3, "3", "Réduire", "DSI+RSSI", "Confidentialité client"),
    ],
}

OWNERS_DEFAUT = {
    "Cyber": "RSSI",
    "Tiers": "Achats+RSSI",
    "RH": "RH",
    "Conformité": "DPO",
    "Continuité": "DSI",
    "Métier": "Direction métier",
}


def generer_registre(secteur, output):
    """Génère le registre pour un secteur donné."""
    if secteur not in RISQUES_SECTEUR:
        print(f"[!] Secteur inconnu: {secteur}", file=sys.stderr)
        print(f"    Secteurs disponibles : {', '.join(RISQUES_SECTEUR.keys())}", file=sys.stderr)
        sys.exit(1)

    risques = RISQUES_TRANSVERSES + RISQUES_SECTEUR[secteur]
    date_id = _date_today()
    # Date de revue à 6 mois
    from datetime import timedelta
    date_revue = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")

    with open(output, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(COLONNES)
        for i, r in enumerate(risques, 1):
            rid = f"R-{i:03d}"
            (categorie, description, source, actif, prob_inh, imp_inh, niv_inh,
             mesures, prob_res, imp_res, niv_res, strategie, owner, commentaire) = r
            writer.writerow([
                rid, date_id, categorie, description, source, actif,
                prob_inh, imp_inh, niv_inh,
                mesures, prob_res, imp_res, niv_res,
                strategie, owner, date_revue, "Actif", commentaire,
            ])

    print(f"[+] Registre généré : {output}")
    print(f"    Secteur : {secteur}")
    print(f"    Nombre de risques : {len(risques)} ({len(RISQUES_TRANSVERSES)} transverses + {len(RISQUES_SECTEUR[secteur])} sectoriels)")
    print(f"    Prochaine revue : {date_revue}")


def main():
    parser = argparse.ArgumentParser(description="Générateur de registre des risques par secteur")
    parser.add_argument("--secteur", required=False,
                        choices=list(RISQUES_SECTEUR.keys()),
                        help="Secteur d'activité")
    parser.add_argument("--output", default=None, help="Fichier CSV de sortie")
    parser.add_argument("--list", action="store_true", help="Lister les secteurs disponibles")
    args = parser.parse_args()

    if args.list:
        print("Secteurs disponibles :")
        for s in RISQUES_SECTEUR.keys():
            n_risques = len(RISQUES_TRANSVERSES) + len(RISQUES_SECTEUR[s])
            print(f"  - {s} ({n_risques} risques)")
        return

    if not args.secteur:
        print("[i] Spécifier --secteur (banque|sante|industrie|retail|public|esn) ou --list")
        return

    output = args.output or f"registre_risques_{args.secteur}.csv"
    generer_registre(args.secteur, output)


if __name__ == "__main__":
    main()
