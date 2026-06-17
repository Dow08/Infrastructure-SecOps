#!/usr/bin/env python3
"""
calcul_fair.py
--------------
Quantification financière du risque cyber selon le modèle FAIR (Factor Analysis of Information Risk).

Méthode :
- Estimer 3 points (min, likely, max) pour chaque facteur avec PERT-Beta.
- Simulation Monte Carlo (10 000+ itérations).
- Calcul de l'ALE (Annual Loss Expectancy) avec percentiles P50, P90, P95.

Utilise uniquement la stdlib (random + math) pour fonctionner sans dépendances.

Usage:
    python calcul_fair.py [--scenario fichier.json] [--iterations 10000] [--output rapport.md]

JSON attendu (exemple) :
{
  "nom_scenario": "Ransomware sur ERP production",
  "TEF": {"min": 0.1, "likely": 0.3, "max": 1.0},
  "Vuln": {"min": 0.3, "likely": 0.5, "max": 0.7},
  "PLM_par_evenement": {"min": 50000, "likely": 200000, "max": 1500000},
  "SLM_par_evenement": {"min": 100000, "likely": 500000, "max": 5000000}
}

Notation FAIR :
- TEF (Threat Event Frequency) : fréquence des tentatives d'événements menaçants par an.
- Vuln : probabilité qu'un événement réussisse compte tenu des défenses.
- LEF (Loss Event Frequency) = TEF × Vuln : nombre d'événements de perte par an.
- PLM (Primary Loss Magnitude) : pertes directes par événement.
- SLM (Secondary Loss Magnitude) : pertes secondaires (réputation, sanctions, etc.).
- LM (Loss Magnitude) = PLM + SLM.
- ALE (Annual Loss Expectancy) = LEF × LM.
"""

import json
import random
import math
import argparse
import sys
from datetime import datetime


def pert_random(min_v, likely_v, max_v, gamma=4.0):
    """
    Tire une valeur aléatoire selon une distribution PERT-Beta.

    PERT est une variante de Beta qui pondère le mode (likely) avec un paramètre gamma.
    gamma=4 est la valeur standard (Beta-PERT classique).
    """
    if min_v > max_v:
        min_v, max_v = max_v, min_v
    if likely_v < min_v:
        likely_v = min_v
    if likely_v > max_v:
        likely_v = max_v
    if min_v == max_v:
        return min_v

    # Paramètres de la distribution Beta
    range_v = max_v - min_v
    alpha = 1 + gamma * (likely_v - min_v) / range_v
    beta = 1 + gamma * (max_v - likely_v) / range_v

    # Tirer une valeur Beta(alpha, beta) puis remettre à l'échelle
    x = random.betavariate(alpha, beta)
    return min_v + x * range_v


def monte_carlo(scenario, iterations=10000, seed=None):
    """
    Exécute la simulation Monte Carlo pour un scénario FAIR.

    Renvoie la liste des ALE simulés.
    """
    if seed is not None:
        random.seed(seed)

    ale_results = []
    lef_results = []
    lm_results = []

    for _ in range(iterations):
        # Tirer chaque facteur
        tef = pert_random(**scenario["TEF"])
        vuln = pert_random(**scenario["Vuln"])
        plm = pert_random(**scenario["PLM_par_evenement"])
        slm = pert_random(**scenario["SLM_par_evenement"])

        # Calcul FAIR
        lef = tef * vuln           # Loss Event Frequency
        lm = plm + slm              # Loss Magnitude par événement
        ale = lef * lm              # Annual Loss Expectancy

        ale_results.append(ale)
        lef_results.append(lef)
        lm_results.append(lm)

    return ale_results, lef_results, lm_results


def stats(values):
    """Calcule moyenne, médiane, P90, P95, écart-type."""
    if not values:
        return {}
    sorted_v = sorted(values)
    n = len(sorted_v)
    mean = sum(sorted_v) / n
    variance = sum((x - mean) ** 2 for x in sorted_v) / n
    stddev = math.sqrt(variance)

    def percentile(p):
        idx = int(n * p / 100)
        idx = min(idx, n - 1)
        return sorted_v[idx]

    return {
        "min": sorted_v[0],
        "max": sorted_v[-1],
        "mean": mean,
        "median": percentile(50),
        "p75": percentile(75),
        "p90": percentile(90),
        "p95": percentile(95),
        "p99": percentile(99),
        "stddev": stddev,
    }


def format_euros(v):
    """Formate un montant en euros lisible."""
    if v >= 1_000_000:
        return f"{v/1_000_000:.2f} M€"
    elif v >= 1_000:
        return f"{v/1_000:.1f} k€"
    return f"{v:.0f} €"


def histogram_ascii(values, bins=20, width=50):
    """Histogramme ASCII pour le rapport Markdown."""
    if not values:
        return ""
    sorted_v = sorted(values)
    p99 = sorted_v[int(len(sorted_v) * 0.99)]
    # Limiter à p99 pour éviter les queues très longues
    v_max = p99
    v_min = sorted_v[0]
    bin_size = (v_max - v_min) / bins if v_max > v_min else 1

    buckets = [0] * bins
    for v in values:
        if v > v_max:
            continue
        idx = min(int((v - v_min) / bin_size), bins - 1)
        buckets[idx] += 1

    max_count = max(buckets) if buckets else 1
    lines = []
    for i, count in enumerate(buckets):
        bar_len = int((count / max_count) * width) if max_count else 0
        bar = "█" * bar_len
        low = v_min + i * bin_size
        lines.append(f"  {format_euros(low):>10s} | {bar} {count}")
    return "\n".join(lines)


def scenario_exemple():
    """Renvoie un scénario d'exemple."""
    return {
        "nom_scenario": "Ransomware sur ERP production",
        "description": "Compromission ERP via phishing + exécution ransomware, indisponibilité 5 jours",
        "TEF": {"min_v": 0.1, "likely_v": 0.3, "max_v": 1.0},
        "Vuln": {"min_v": 0.3, "likely_v": 0.5, "max_v": 0.7},
        "PLM_par_evenement": {"min_v": 50000, "likely_v": 200000, "max_v": 1500000},
        "SLM_par_evenement": {"min_v": 100000, "likely_v": 500000, "max_v": 5000000},
    }


def normaliser_scenario(s):
    """Normalise les noms des clés (min/likely/max → min_v/likely_v/max_v)."""
    out = {"nom_scenario": s.get("nom_scenario", "Scénario sans nom"),
           "description": s.get("description", "")}
    for facteur in ("TEF", "Vuln", "PLM_par_evenement", "SLM_par_evenement"):
        if facteur not in s:
            print(f"[!] Facteur manquant: {facteur}", file=sys.stderr)
            sys.exit(1)
        f = s[facteur]
        out[facteur] = {
            "min_v": float(f.get("min", f.get("min_v"))),
            "likely_v": float(f.get("likely", f.get("likely_v"))),
            "max_v": float(f.get("max", f.get("max_v"))),
        }
    return out


def rapport_markdown(scenario, ale_results, lef_results, lm_results, iterations, output):
    """Génère le rapport Markdown du calcul FAIR."""
    s_ale = stats(ale_results)
    s_lef = stats(lef_results)
    s_lm = stats(lm_results)

    lines = []
    lines.append(f"# Quantification FAIR - {scenario['nom_scenario']}")
    lines.append(f"\n**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Itérations Monte Carlo** : {iterations:,}")
    lines.append(f"**Description** : {scenario.get('description', 'N/A')}\n")

    lines.append("## Hypothèses (PERT 3 points)\n")
    lines.append("| Facteur | Min | Likely | Max |")
    lines.append("|---|---|---|---|")
    for facteur in ("TEF", "Vuln", "PLM_par_evenement", "SLM_par_evenement"):
        f = scenario[facteur]
        if facteur in ("TEF", "Vuln"):
            lines.append(f"| {facteur} | {f['min_v']:.3f} | {f['likely_v']:.3f} | {f['max_v']:.3f} |")
        else:
            lines.append(f"| {facteur} | {format_euros(f['min_v'])} | {format_euros(f['likely_v'])} | {format_euros(f['max_v'])} |")

    lines.append("\n## Résultats - Annual Loss Expectancy (ALE)\n")
    lines.append("| Statistique | Valeur |")
    lines.append("|---|---|")
    lines.append(f"| Moyenne | {format_euros(s_ale['mean'])} |")
    lines.append(f"| Médiane (P50) | {format_euros(s_ale['median'])} |")
    lines.append(f"| P75 | {format_euros(s_ale['p75'])} |")
    lines.append(f"| **P90** | **{format_euros(s_ale['p90'])}** |")
    lines.append(f"| **P95** | **{format_euros(s_ale['p95'])}** |")
    lines.append(f"| P99 | {format_euros(s_ale['p99'])} |")
    lines.append(f"| Maximum simulé | {format_euros(s_ale['max'])} |")
    lines.append(f"| Écart-type | {format_euros(s_ale['stddev'])} |")

    lines.append("\n## Loss Event Frequency (LEF)\n")
    lines.append(f"- Moyenne : {s_lef['mean']:.3f} événements/an")
    lines.append(f"- Médiane : {s_lef['median']:.3f} événements/an")
    lines.append(f"- P90 : {s_lef['p90']:.3f} événements/an")

    lines.append("\n## Loss Magnitude par événement (LM)\n")
    lines.append(f"- Moyenne : {format_euros(s_lm['mean'])}")
    lines.append(f"- Médiane : {format_euros(s_lm['median'])}")
    lines.append(f"- P90 : {format_euros(s_lm['p90'])}")

    lines.append("\n## Distribution ALE (histogramme)\n")
    lines.append("```")
    lines.append(histogram_ascii(ale_results))
    lines.append("```\n")

    lines.append("## Interprétation\n")
    lines.append(f"- **Perte annuelle moyenne attendue** : {format_euros(s_ale['mean'])}")
    lines.append(f"- **Dans 90% des cas**, la perte annuelle sera **inférieure à {format_euros(s_ale['p90'])}**.")
    lines.append(f"- **Pire scénario crédible (P95)** : {format_euros(s_ale['p95'])}")
    lines.append(f"- **Cas extrême (P99)** : {format_euros(s_ale['p99'])}")

    lines.append("\n## Recommandations\n")
    lines.append("- Présenter à la Direction la **valeur P90** comme référence de budget de défense.")
    lines.append("- Comparer le coût d'une mesure de réduction du risque à la **différence d'ALE moyen** avant/après.")
    lines.append("- Une mesure n'est pertinente que si elle réduit l'ALE de plus que son coût total de possession.")
    lines.append("- Réviser le scénario annuellement, ou après un incident significatif modifiant les hypothèses.")
    lines.append("\n## Méthodologie\n")
    lines.append("- Modèle FAIR : ALE = LEF × LM avec LEF = TEF × Vuln et LM = PLM + SLM.")
    lines.append("- Distribution PERT-Beta (gamma=4) sur chaque facteur, échantillonnée en Monte Carlo.")
    lines.append("- Cohérent avec les pratiques The Open Group O-RT (Risk Taxonomy) et O-RA (Risk Analysis).")

    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[+] Rapport généré: {output}")


def main():
    parser = argparse.ArgumentParser(description="Quantification FAIR Monte Carlo")
    parser.add_argument("--scenario", help="JSON décrivant le scénario")
    parser.add_argument("--iterations", type=int, default=10000, help="Nombre d'itérations")
    parser.add_argument("--output", default="rapport_fair.md", help="Rapport Markdown")
    parser.add_argument("--seed", type=int, help="Seed aléatoire (reproductibilité)")
    parser.add_argument("--exemple", action="store_true", help="Lancer avec scénario d'exemple")
    parser.add_argument("--template", action="store_true", help="Générer un JSON modèle")
    args = parser.parse_args()

    if args.template:
        template = {
            "nom_scenario": "Mon scenario",
            "description": "Description du scenario",
            "TEF": {"min": 0.1, "likely": 0.3, "max": 1.0},
            "Vuln": {"min": 0.3, "likely": 0.5, "max": 0.7},
            "PLM_par_evenement": {"min": 50000, "likely": 200000, "max": 1500000},
            "SLM_par_evenement": {"min": 100000, "likely": 500000, "max": 5000000}
        }
        with open("scenario_fair_template.json", "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        print("[+] Template généré: scenario_fair_template.json")
        return

    if args.exemple:
        scenario = scenario_exemple()
    elif args.scenario:
        try:
            with open(args.scenario, "r", encoding="utf-8") as f:
                raw = json.load(f)
            scenario = normaliser_scenario(raw)
        except FileNotFoundError:
            print(f"[!] Fichier non trouvé: {args.scenario}", file=sys.stderr)
            sys.exit(1)
    else:
        print("[i] Utilisez --exemple pour un test rapide, ou --scenario fichier.json")
        return

    print(f"[i] Lancement Monte Carlo {args.iterations:,} itérations sur '{scenario['nom_scenario']}'...")
    ale, lef, lm = monte_carlo(scenario, args.iterations, args.seed)
    rapport_markdown(scenario, ale, lef, lm, args.iterations, args.output)


if __name__ == "__main__":
    main()
