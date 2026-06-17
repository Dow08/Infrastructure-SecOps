#!/usr/bin/env python3
"""
scoring_maturite_nist_csf.py
----------------------------
Évalue la maturité cybersécurité selon NIST CSF 2.0.

6 fonctions (Govern nouveau en 2024) :
- GV : Govern
- ID : Identify
- PR : Protect
- DE : Detect
- RS : Respond
- RC : Recover

4 Tiers de maturité (NIST CSF):
1 = Partial (ad hoc, réactif)
2 = Risk Informed (informé du risque, partiellement formalisé)
3 = Repeatable (répétable, formalisé, mesuré)
4 = Adaptive (adaptatif, amélioration continue)

Usage:
    python scoring_maturite_nist_csf.py [--input fichier.csv] [--template] [--output rapport.md]

CSV attendu:
    fonction,categorie,sous_categorie,score,commentaire
    GV,GV.OC,GV.OC-01,3,Strategie documentee
"""

import csv
import argparse
import sys
from collections import defaultdict
from datetime import datetime

# Modèle NIST CSF 2.0 (extrait des sous-catégories principales - liste non exhaustive mais représentative)
FRAMEWORK = {
    "GV": {
        "nom": "Govern",
        "description": "Stratégie de gestion du risque cyber",
        "categories": {
            "GV.OC": "Contexte organisationnel",
            "GV.RM": "Stratégie de gestion des risques",
            "GV.RR": "Rôles, responsabilités et autorités",
            "GV.PO": "Politique",
            "GV.OV": "Supervision",
            "GV.SC": "Gestion des risques de la chaîne d'approvisionnement",
        },
        "sous_categories": [
            ("GV.OC-01", "Mission organisationnelle comprise"),
            ("GV.OC-02", "Parties prenantes internes/externes comprises"),
            ("GV.OC-03", "Exigences légales/réglementaires comprises"),
            ("GV.OC-04", "Objectifs/capacités/services critiques compris"),
            ("GV.OC-05", "Résultats et dépendances compris"),
            ("GV.RM-01", "Objectifs de gestion des risques convenus"),
            ("GV.RM-02", "Déclarations de tolérance au risque établies"),
            ("GV.RM-03", "Tolérance au risque communiquée"),
            ("GV.RR-01", "Rôles/responsabilités cyber établis"),
            ("GV.RR-02", "Direction responsable de la cybersécurité"),
            ("GV.PO-01", "Politique cyber établie"),
            ("GV.PO-02", "Politique cyber communiquée"),
            ("GV.OV-01", "Performance cyber évaluée"),
            ("GV.OV-02", "Stratégie revue régulièrement"),
            ("GV.SC-01", "Programme de gestion des risques fournisseurs"),
            ("GV.SC-02", "Critères d'évaluation fournisseurs établis"),
        ],
    },
    "ID": {
        "nom": "Identify",
        "description": "Connaissance des actifs, risques et environnement",
        "categories": {
            "ID.AM": "Gestion des actifs",
            "ID.RA": "Évaluation des risques",
            "ID.IM": "Amélioration",
        },
        "sous_categories": [
            ("ID.AM-01", "Inventaire matériel maintenu"),
            ("ID.AM-02", "Inventaire logiciel maintenu"),
            ("ID.AM-03", "Cartographie des flux de données"),
            ("ID.AM-04", "Inventaire des services externes"),
            ("ID.AM-05", "Actifs classifiés et priorisés"),
            ("ID.AM-07", "Données classifiées"),
            ("ID.RA-01", "Vulnérabilités identifiées"),
            ("ID.RA-02", "Renseignement menaces reçu"),
            ("ID.RA-03", "Menaces internes/externes identifiées"),
            ("ID.RA-04", "Impacts business analysés"),
            ("ID.RA-05", "Risques cyber priorisés"),
            ("ID.IM-01", "Leçons apprises intégrées"),
        ],
    },
    "PR": {
        "nom": "Protect",
        "description": "Contrôles de protection des actifs",
        "categories": {
            "PR.AA": "Gestion identités et accès",
            "PR.AT": "Sensibilisation et formation",
            "PR.DS": "Sécurité des données",
            "PR.PS": "Sécurité plateforme",
            "PR.IR": "Résilience infrastructure",
        },
        "sous_categories": [
            ("PR.AA-01", "Identités gérées"),
            ("PR.AA-02", "Authentification appliquée"),
            ("PR.AA-03", "Authentification forte (MFA)"),
            ("PR.AA-05", "Accès géré selon moindre privilège"),
            ("PR.AT-01", "Personnel formé"),
            ("PR.AT-02", "Personnel privilégié formé"),
            ("PR.DS-01", "Données protégées au repos"),
            ("PR.DS-02", "Données protégées en transit"),
            ("PR.DS-10", "Données protégées en utilisation"),
            ("PR.DS-11", "Sauvegardes créées et testées"),
            ("PR.PS-01", "Configurations standards appliquées"),
            ("PR.PS-02", "Logiciels maintenus"),
            ("PR.PS-03", "Matériels maintenus"),
            ("PR.PS-05", "Installation/exécution logiciels non autorisés empêchée"),
            ("PR.PS-06", "Pratiques sécurité du code"),
            ("PR.IR-01", "Réseaux protégés"),
            ("PR.IR-02", "Capacités de résilience établies"),
        ],
    },
    "DE": {
        "nom": "Detect",
        "description": "Détection des événements et anomalies",
        "categories": {
            "DE.CM": "Surveillance continue",
            "DE.AE": "Analyse événements",
        },
        "sous_categories": [
            ("DE.CM-01", "Réseaux surveillés"),
            ("DE.CM-02", "Environnement physique surveillé"),
            ("DE.CM-03", "Personnel surveillé"),
            ("DE.CM-06", "Activités fournisseurs surveillées"),
            ("DE.CM-09", "Logiciels et matériels surveillés"),
            ("DE.AE-02", "Activités suspectes analysées"),
            ("DE.AE-03", "Informations événements corrélées"),
            ("DE.AE-04", "Impact incidents évalué"),
            ("DE.AE-06", "Informations événements communiquées"),
            ("DE.AE-07", "Renseignement cyber intégré"),
            ("DE.AE-08", "Incidents déclarés"),
        ],
    },
    "RS": {
        "nom": "Respond",
        "description": "Réponse aux incidents",
        "categories": {
            "RS.MA": "Gestion incidents",
            "RS.AN": "Analyse incidents",
            "RS.CO": "Communication",
            "RS.MI": "Atténuation",
        },
        "sous_categories": [
            ("RS.MA-01", "Plan de réponse exécuté"),
            ("RS.MA-02", "Incidents triés et validés"),
            ("RS.MA-03", "Incidents catégorisés et priorisés"),
            ("RS.MA-04", "Incidents escaladés"),
            ("RS.MA-05", "Critères d'escalade définis"),
            ("RS.AN-03", "Analyses effectuées"),
            ("RS.AN-06", "Actions documentées"),
            ("RS.AN-07", "Preuves préservées"),
            ("RS.AN-08", "Cause racine déterminée"),
            ("RS.CO-02", "Parties prenantes internes notifiées"),
            ("RS.CO-03", "Information partagée"),
            ("RS.MI-01", "Incidents contenus"),
            ("RS.MI-02", "Incidents éradiqués"),
        ],
    },
    "RC": {
        "nom": "Recover",
        "description": "Reprise après incident",
        "categories": {
            "RC.RP": "Plan de reprise",
            "RC.CO": "Communication reprise",
        },
        "sous_categories": [
            ("RC.RP-01", "Plan de reprise exécuté"),
            ("RC.RP-02", "Actions de reprise sélectionnées"),
            ("RC.RP-03", "Intégrité sauvegardes vérifiée"),
            ("RC.RP-04", "Fonctions critiques restaurées"),
            ("RC.RP-05", "Intégrité systèmes restaurée"),
            ("RC.RP-06", "Fin de la reprise déclarée"),
            ("RC.CO-03", "Activités de reprise communiquées"),
            ("RC.CO-04", "Communication publique gérée"),
        ],
    },
}

INDEX = {}
for fcode, fdata in FRAMEWORK.items():
    for sc_code, sc_nom in fdata["sous_categories"]:
        INDEX[sc_code] = (fcode, fdata["nom"], sc_nom)


def template_csv(path="nist_csf_template.csv"):
    """Génère un CSV vierge à compléter."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fonction", "categorie", "sous_categorie", "nom", "score", "commentaire"])
        for fcode, fdata in FRAMEWORK.items():
            for sc_code, sc_nom in fdata["sous_categories"]:
                cat = sc_code.rsplit("-", 1)[0]
                writer.writerow([fcode, cat, sc_code, sc_nom, 0, ""])
    print(f"[+] Template généré: {path}")


def load_csv(path):
    """Charge les évaluations depuis un CSV."""
    data = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sc = row.get("sous_categorie", "").strip()
                if not sc:
                    continue
                try:
                    score = int(row.get("score", "0") or "0")
                except ValueError:
                    score = 0
                data[sc] = {
                    "score": max(0, min(4, score)),
                    "commentaire": row.get("commentaire", "").strip(),
                }
    except FileNotFoundError:
        print(f"[!] Fichier non trouvé: {path}", file=sys.stderr)
        sys.exit(1)
    return data


def tier_label(score):
    """Convertit le score moyen en Tier NIST CSF."""
    if score >= 3.5:
        return "Tier 4 - Adaptive"
    elif score >= 2.5:
        return "Tier 3 - Repeatable"
    elif score >= 1.5:
        return "Tier 2 - Risk Informed"
    elif score >= 0.5:
        return "Tier 1 - Partial"
    return "Non évalué"


def analyse(data):
    """Calcule scores par fonction et identifie les écarts."""
    par_fonction = defaultdict(lambda: {"count": 0, "score_sum": 0, "scores": []})
    ecarts = []

    for sc_code, (fcode, fnom, sc_nom) in INDEX.items():
        info = data.get(sc_code)
        score = info["score"] if info else 0
        par_fonction[fcode]["count"] += 1
        par_fonction[fcode]["score_sum"] += score
        par_fonction[fcode]["scores"].append(score)

        if score < 2:
            ecarts.append({
                "code": sc_code,
                "nom": sc_nom,
                "fonction": fnom,
                "score": score,
                "commentaire": info["commentaire"] if info else "",
            })

    return par_fonction, ecarts


def rapport_markdown(data, par_fonction, ecarts, output="rapport_nist_csf.md"):
    """Génère le rapport."""
    total_count = sum(p["count"] for p in par_fonction.values())
    total_sum = sum(p["score_sum"] for p in par_fonction.values())
    score_global = total_sum / total_count if total_count else 0

    lines = []
    lines.append("# Rapport de maturité NIST CSF 2.0")
    lines.append(f"\n**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Sous-catégories évaluées** : {total_count}")
    lines.append(f"**Score moyen global** : {score_global:.2f} / 4")
    lines.append(f"**Niveau global** : {tier_label(score_global)}\n")

    lines.append("## Score par fonction\n")
    lines.append("| Fonction | Description | Score moyen | Tier |")
    lines.append("|---|---|---|---|")
    for fcode, fdata in FRAMEWORK.items():
        p = par_fonction.get(fcode, {"count": 0, "score_sum": 0})
        moy = p["score_sum"] / p["count"] if p["count"] else 0
        lines.append(f"| {fcode} - {fdata['nom']} | {fdata['description']} | {moy:.2f} | {tier_label(moy)} |")

    # Heat map ASCII
    lines.append("\n## Heat map (visualisation)\n")
    lines.append("```")
    for fcode, fdata in FRAMEWORK.items():
        p = par_fonction.get(fcode, {"count": 0, "score_sum": 0})
        moy = p["score_sum"] / p["count"] if p["count"] else 0
        # Échelle visuelle 0-4
        n_blocks = int(round(moy * 5))
        bar = "█" * n_blocks + "░" * (20 - n_blocks)
        lines.append(f"{fcode} {fdata['nom']:10s} [{bar}] {moy:.2f}")
    lines.append("```\n")

    # Écarts
    lines.append(f"## Écarts à traiter en priorité ({len(ecarts)})\n")
    if not ecarts:
        lines.append("Aucun écart majeur (score < 2) identifié.\n")
    else:
        ecarts.sort(key=lambda e: (e["score"], e["code"]))
        lines.append("| Code | Sous-catégorie | Fonction | Score | Commentaire |")
        lines.append("|---|---|---|---|---|")
        for e in ecarts[:30]:
            lines.append(
                f"| {e['code']} | {e['nom']} | {e['fonction']} | {e['score']} | "
                f"{e['commentaire'][:60]} |"
            )
        if len(ecarts) > 30:
            lines.append(f"\n*... et {len(ecarts) - 30} autres écarts*\n")

    # Recommandations
    lines.append("\n## Recommandations stratégiques\n")
    # Identifier les 2 fonctions les plus faibles
    moyennes = []
    for fcode, fdata in FRAMEWORK.items():
        p = par_fonction.get(fcode)
        if p and p["count"]:
            moyennes.append((p["score_sum"] / p["count"], fcode, fdata["nom"]))
    moyennes.sort()

    if moyennes:
        lines.append("**Priorités d'amélioration** (fonctions les plus faibles) :\n")
        for moy, fcode, fnom in moyennes[:2]:
            lines.append(f"- **{fcode} ({fnom})** : score {moy:.2f} - investir prioritairement.")

    lines.append("\n## Méthodologie\n")
    lines.append("- Échelle NIST CSF 2.0 : 0 (non évalué) → 4 (adaptatif).")
    lines.append("- Le Tier global cible est généralement 3 (répétable) pour les organisations matures.")
    lines.append("- Le Tier 4 (adaptatif) est l'objectif des grands groupes et secteurs régulés.")
    lines.append("- Revue annuelle minimum + après changement majeur.")
    lines.append("- La fonction **Govern (GV)** est NOUVELLE dans CSF 2.0 (2024) et souvent la moins mature dans les évaluations initiales.\n")

    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[+] Rapport généré: {output}")


def main():
    parser = argparse.ArgumentParser(description="Scoring maturité NIST CSF 2.0")
    parser.add_argument("--input", help="CSV d'évaluation")
    parser.add_argument("--output", default="rapport_nist_csf.md", help="Rapport Markdown")
    parser.add_argument("--template", action="store_true", help="Générer un CSV vierge")
    args = parser.parse_args()

    if args.template:
        template_csv()
        return

    if not args.input:
        print("[i] Utiliser --template pour générer un CSV vierge, puis --input.")
        return

    data = load_csv(args.input)
    par_fonction, ecarts = analyse(data)
    rapport_markdown(data, par_fonction, ecarts, args.output)


if __name__ == "__main__":
    main()
