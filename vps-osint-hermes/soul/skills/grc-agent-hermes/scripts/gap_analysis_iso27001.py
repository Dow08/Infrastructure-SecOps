#!/usr/bin/env python3
"""
gap_analysis_iso27001.py
------------------------
Outil de gap analysis ISO 27001:2022 (Annexe A - 93 contrôles).

Usage:
    python gap_analysis_iso27001.py [--input fichier.csv] [--output rapport.md]

Format CSV attendu (input):
    code,statut,maturite,commentaire
    A.5.1,Implemente,4,Politique publiee
    A.5.2,Partiel,2,En cours
    ...

Échelle de maturité (CMMI inspiré):
    0 = Inexistant
    1 = Initial / ad hoc
    2 = Reproductible mais informel
    3 = Défini et documenté
    4 = Maîtrisé et mesuré
    5 = Optimisé et amélioré en continu

Sortie: rapport Markdown avec score global, par thème, top écarts.
"""

import csv
import argparse
import sys
from collections import defaultdict
from datetime import datetime

# Référentiel ISO 27001:2022 Annexe A - 93 contrôles regroupés par thème
CONTROLES = {
    "Organisationnels (A.5)": [
        ("A.5.1", "Politiques de sécurité"),
        ("A.5.2", "Rôles et responsabilités"),
        ("A.5.3", "Séparation des tâches"),
        ("A.5.4", "Responsabilités de la direction"),
        ("A.5.5", "Contact avec les autorités"),
        ("A.5.6", "Contact avec des groupes spécialisés"),
        ("A.5.7", "Veille sur les menaces (threat intel)"),
        ("A.5.8", "Sécurité dans la gestion de projet"),
        ("A.5.9", "Inventaire des actifs"),
        ("A.5.10", "Utilisation acceptable des actifs"),
        ("A.5.11", "Restitution des actifs"),
        ("A.5.12", "Classification de l'information"),
        ("A.5.13", "Marquage de l'information"),
        ("A.5.14", "Transfert d'information"),
        ("A.5.15", "Contrôle d'accès"),
        ("A.5.16", "Gestion de l'identité"),
        ("A.5.17", "Informations d'authentification"),
        ("A.5.18", "Droits d'accès"),
        ("A.5.19", "Sécurité dans relations fournisseurs"),
        ("A.5.20", "Sécurité dans accords fournisseurs"),
        ("A.5.21", "Sécurité chaîne approvisionnement TIC"),
        ("A.5.22", "Surveillance des services fournisseurs"),
        ("A.5.23", "Sécurité services Cloud"),
        ("A.5.24", "Planification gestion incidents"),
        ("A.5.25", "Évaluation et décision sur incidents"),
        ("A.5.26", "Réponse aux incidents"),
        ("A.5.27", "Apprentissage suite à incidents"),
        ("A.5.28", "Collecte des preuves"),
        ("A.5.29", "Sécurité pendant perturbations"),
        ("A.5.30", "Préparation TIC à la continuité"),
        ("A.5.31", "Exigences légales et réglementaires"),
        ("A.5.32", "Droits de propriété intellectuelle"),
        ("A.5.33", "Protection des enregistrements"),
        ("A.5.34", "Confidentialité et protection données"),
        ("A.5.35", "Revue indépendante de la sécurité"),
        ("A.5.36", "Conformité avec politiques"),
        ("A.5.37", "Procédures opérationnelles documentées"),
    ],
    "Personnels (A.6)": [
        ("A.6.1", "Vérification des antécédents"),
        ("A.6.2", "Conditions d'embauche"),
        ("A.6.3", "Sensibilisation, formation"),
        ("A.6.4", "Processus disciplinaire"),
        ("A.6.5", "Responsabilités après emploi"),
        ("A.6.6", "Engagements de confidentialité"),
        ("A.6.7", "Travail à distance"),
        ("A.6.8", "Signalement événements sécurité"),
    ],
    "Physiques (A.7)": [
        ("A.7.1", "Périmètres de sécurité physique"),
        ("A.7.2", "Contrôles physiques d'accès"),
        ("A.7.3", "Sécurisation bureaux et salles"),
        ("A.7.4", "Surveillance de la sécurité physique"),
        ("A.7.5", "Protection contre menaces externes"),
        ("A.7.6", "Travail en zones sécurisées"),
        ("A.7.7", "Bureau dégagé et écran verrouillé"),
        ("A.7.8", "Emplacement et protection matériel"),
        ("A.7.9", "Sécurité actifs hors site"),
        ("A.7.10", "Supports de stockage"),
        ("A.7.11", "Services généraux (énergie, clim)"),
        ("A.7.12", "Sécurité du câblage"),
        ("A.7.13", "Maintenance équipements"),
        ("A.7.14", "Élimination ou réutilisation sécurisée"),
    ],
    "Technologiques (A.8)": [
        ("A.8.1", "Terminaux utilisateurs"),
        ("A.8.2", "Privilèges d'accès"),
        ("A.8.3", "Restriction d'accès à l'information"),
        ("A.8.4", "Accès au code source"),
        ("A.8.5", "Authentification sécurisée"),
        ("A.8.6", "Gestion de la capacité"),
        ("A.8.7", "Protection contre les malwares"),
        ("A.8.8", "Gestion des vulnérabilités techniques"),
        ("A.8.9", "Gestion de configuration"),
        ("A.8.10", "Suppression de l'information"),
        ("A.8.11", "Masquage de données"),
        ("A.8.12", "Prévention fuite données (DLP)"),
        ("A.8.13", "Sauvegarde de l'information"),
        ("A.8.14", "Redondance des moyens TIC"),
        ("A.8.15", "Journalisation"),
        ("A.8.16", "Surveillance des activités"),
        ("A.8.17", "Synchronisation horloges"),
        ("A.8.18", "Utilisation utilitaires privilégiés"),
        ("A.8.19", "Installation logiciels systèmes opérationnels"),
        ("A.8.20", "Sécurité des réseaux"),
        ("A.8.21", "Sécurité services réseau"),
        ("A.8.22", "Séparation des réseaux"),
        ("A.8.23", "Filtrage web"),
        ("A.8.24", "Utilisation cryptographie"),
        ("A.8.25", "Cycle vie développement sécurisé"),
        ("A.8.26", "Exigences sécurité applications"),
        ("A.8.27", "Architecture et principes ingénierie"),
        ("A.8.28", "Codage sécurisé"),
        ("A.8.29", "Tests sécurité (SAST/DAST)"),
        ("A.8.30", "Développement externalisé"),
        ("A.8.31", "Séparation environnements (dev/test/prod)"),
        ("A.8.32", "Gestion des changements"),
        ("A.8.33", "Informations de test"),
        ("A.8.34", "Protection des SI pendant audit"),
    ],
}

# Aplatir en index code -> (thème, nom)
INDEX = {}
for theme, ctrls in CONTROLES.items():
    for code, name in ctrls:
        INDEX[code] = (theme, name)


def load_csv(path):
    """Charge un CSV avec les colonnes: code, statut, maturite, commentaire."""
    data = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row.get("code", "").strip()
                if not code:
                    continue
                data[code] = {
                    "statut": row.get("statut", "Non evalue").strip(),
                    "maturite": int(row.get("maturite", "0") or "0"),
                    "commentaire": row.get("commentaire", "").strip(),
                }
    except FileNotFoundError:
        print(f"[!] Fichier non trouvé: {path}", file=sys.stderr)
        sys.exit(1)
    return data


def template_csv(output_path="iso27001_template.csv"):
    """Génère un CSV vierge à compléter."""
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["code", "nom", "theme", "statut", "maturite", "commentaire"])
        for theme, ctrls in CONTROLES.items():
            for code, name in ctrls:
                writer.writerow([code, name, theme, "Non evalue", 0, ""])
    print(f"[+] Template généré: {output_path}")


def analyse(data):
    """Calcule les scores et identifie les écarts."""
    par_theme = defaultdict(lambda: {"count": 0, "score_sum": 0, "implementes": 0})
    ecarts = []
    non_evalues = []

    for code, (theme, name) in INDEX.items():
        info = data.get(code)
        if not info or info["statut"] == "Non evalue":
            non_evalues.append((code, name, theme))
            continue

        par_theme[theme]["count"] += 1
        par_theme[theme]["score_sum"] += info["maturite"]
        if info["statut"] == "Implemente" and info["maturite"] >= 3:
            par_theme[theme]["implementes"] += 1

        if info["maturite"] < 3 or info["statut"] in ("Partiel", "Non implemente"):
            ecarts.append({
                "code": code,
                "nom": name,
                "theme": theme,
                "statut": info["statut"],
                "maturite": info["maturite"],
                "commentaire": info["commentaire"],
            })

    return par_theme, ecarts, non_evalues


def rapport_markdown(data, par_theme, ecarts, non_evalues, output="rapport_gap_iso27001.md"):
    """Génère le rapport au format Markdown."""
    total_evalues = sum(t["count"] for t in par_theme.values())
    total_implementes = sum(t["implementes"] for t in par_theme.values())
    total_score = sum(t["score_sum"] for t in par_theme.values())
    score_global = (total_score / total_evalues) if total_evalues else 0

    lines = []
    lines.append(f"# Rapport Gap Analysis ISO 27001:2022")
    lines.append(f"\n**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Contrôles évalués** : {total_evalues} / 93")
    lines.append(f"**Contrôles implémentés (maturité ≥ 3)** : {total_implementes}")
    lines.append(f"**Score moyen de maturité** : {score_global:.2f} / 5")
    lines.append(f"**Taux de couverture** : {(total_evalues/93)*100:.1f}%")
    lines.append(f"**Taux d'implémentation effective** : {(total_implementes/93)*100:.1f}%")

    # Évaluation globale
    if score_global >= 4:
        verdict = "🟢 Maturité élevée - candidat à la certification"
    elif score_global >= 3:
        verdict = "🟠 Maturité acceptable - écarts à traiter avant certification"
    elif score_global >= 2:
        verdict = "🔴 Maturité partielle - travail significatif requis (6-12 mois)"
    else:
        verdict = "🔴 Maturité faible - programme de mise en conformité de 12-18 mois"
    lines.append(f"\n**Verdict global** : {verdict}\n")

    # Score par thème
    lines.append("## Score par thème\n")
    lines.append("| Thème | Contrôles évalués | Score moyen | % maturité ≥ 3 |")
    lines.append("|---|---|---|---|")
    for theme in CONTROLES.keys():
        t = par_theme.get(theme, {"count": 0, "score_sum": 0, "implementes": 0})
        if t["count"] == 0:
            lines.append(f"| {theme} | 0 | N/A | N/A |")
        else:
            moy = t["score_sum"] / t["count"]
            taux = (t["implementes"] / t["count"]) * 100
            lines.append(f"| {theme} | {t['count']} | {moy:.2f} | {taux:.1f}% |")

    # Top écarts
    lines.append("\n## Écarts identifiés (à traiter en priorité)\n")
    if not ecarts:
        lines.append("Aucun écart majeur détecté sur les contrôles évalués.\n")
    else:
        # Trier par maturité croissante puis par code
        ecarts.sort(key=lambda x: (x["maturite"], x["code"]))
        lines.append("| Code | Nom | Statut | Maturité | Thème | Commentaire |")
        lines.append("|---|---|---|---|---|---|")
        for e in ecarts[:30]:
            lines.append(
                f"| {e['code']} | {e['nom']} | {e['statut']} | {e['maturite']} | "
                f"{e['theme']} | {e['commentaire'][:60]} |"
            )
        if len(ecarts) > 30:
            lines.append(f"\n*... et {len(ecarts) - 30} autres écarts (voir CSV complet)*\n")

    # Non évalués
    if non_evalues:
        lines.append(f"\n## Contrôles non évalués ({len(non_evalues)})\n")
        lines.append("À compléter pour avoir une vue complète :\n")
        lines.append("| Code | Nom | Thème |")
        lines.append("|---|---|---|")
        for code, name, theme in non_evalues[:20]:
            lines.append(f"| {code} | {name} | {theme} |")
        if len(non_evalues) > 20:
            lines.append(f"\n*... et {len(non_evalues) - 20} autres*\n")

    # Plan d'action recommandé
    lines.append("\n## Plan d'action recommandé\n")
    lines.append("1. **Traiter les contrôles de maturité 0 ou 1** : ce sont les écarts majeurs.")
    lines.append("2. **Consolider les contrôles de maturité 2** : formaliser et documenter.")
    lines.append("3. **Optimiser les contrôles de maturité 3** : mesurer et améliorer.")
    lines.append("4. **Compléter les contrôles non évalués** sous 30 jours.")
    lines.append("5. **Revue dans 3 mois** après plan d'action initial.")
    lines.append("\n## Méthodologie\n")
    lines.append("- Échelle CMMI : 0 (inexistant) → 5 (optimisé)")
    lines.append("- Seuil de conformité visé : maturité ≥ 3 sur 90% des contrôles applicables")
    lines.append("- Réévaluation : annuelle minimum, ou après changement majeur du périmètre.\n")

    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[+] Rapport généré: {output}")


def main():
    parser = argparse.ArgumentParser(description="Gap analysis ISO 27001:2022")
    parser.add_argument("--input", help="Fichier CSV d'évaluation")
    parser.add_argument("--output", default="rapport_gap_iso27001.md", help="Rapport Markdown")
    parser.add_argument("--template", action="store_true", help="Générer un CSV vierge")
    args = parser.parse_args()

    if args.template:
        template_csv()
        return

    if not args.input:
        print("[i] Aucun fichier fourni. Utilisez --template pour générer un CSV vierge,")
        print("    puis --input fichier.csv pour analyser vos données.")
        return

    data = load_csv(args.input)
    par_theme, ecarts, non_evalues = analyse(data)
    rapport_markdown(data, par_theme, ecarts, non_evalues, args.output)


if __name__ == "__main__":
    main()
