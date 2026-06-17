# Livrables — Nova Syndicate

> Espace de production des **10 livrables officiels** du projet.
> Mis à jour : 14/05/2026.

---

## Vue d'ensemble

| # | Livrable | Statut | Chemin |
|---|----------|--------|--------|
| 1 | **Rapport Phase I** — Analyse besoins | ✅ Écrit | [`01_phase_I_analyse/Rapport_Phase_I_Analyse_Besoins.md`](01_phase_I_analyse/Rapport_Phase_I_Analyse_Besoins.md) |
| 2 | Slides résumé Phase I | ⏳ Vendredi | [`08_presentation_slides/`](08_presentation_slides/) |
| 3 | **Document technique Phase II** — Conception & déploiement | ✅ Écrit | [`02_phase_II_conception/Document_Technique_Phase_II.md`](02_phase_II_conception/Document_Technique_Phase_II.md) |
| 4 | Preuves fonctionnement (25 POC) | 🟡 8/25 | [`../Documents/POC_Screen/`](../Documents/POC_Screen/) |
| 5 | **Rapport amélioration Phase III** | ✅ Écrit | [`03_phase_III_amelioration/Rapport_Amelioration_Phase_III.md`](03_phase_III_amelioration/Rapport_Amelioration_Phase_III.md) |
| 5b | **PCA + PRA** (continuité + reprise sinistre) | ✅ Écrit | [`04_pca_pra/PCA_PRA_Nova_Syndicate.md`](04_pca_pra/PCA_PRA_Nova_Syndicate.md) |
| 6 | **3 scripts d'automatisation** + **5 playbooks Ansible** | ✅ Écrits | [`06_scripts_automation/`](06_scripts_automation/) · [Ansible](06_scripts_automation/ansible/) |
| 7 | **Veille technologique EN** (Wazuh 2025-2026) | ✅ Écrit | [`05_veille_techno_EN/Technology_Watch_Wazuh_SIEM_2025-2026.md`](05_veille_techno_EN/Technology_Watch_Wazuh_SIEM_2025-2026.md) |
| 8 | **Plan self-pentest** + Rapport (post-tests) | 🟡 Plan ✅ / Rapport ⏳ jeudi | [`07_pentest_report/`](07_pentest_report/) |
| 9 | **Gestion projet** (Notion) | ✅ En ligne | [Lien Notion](https://www.notion.so/35ddae11bf0d81b69be1d152bacf14fd) |
| 10 | Slides présentation finale (10-15 min) | ⏳ Vendredi | [`08_presentation_slides/`](08_presentation_slides/) |
| Annexe | **CAPEX/OPEX détaillé** (comparatif 3 solutions) | ✅ Écrit | [`annexes_capex_opex/CAPEX_OPEX_Detaille.md`](annexes_capex_opex/CAPEX_OPEX_Detaille.md) |

---

## Volumétrie produite

| Indicateur | Valeur |
|------------|--------|
| Documents écrits | **8 documents principaux** (lundi nuit) |
| Pages cumulées (estimation) | **~150 pages** |
| Scripts d'automatisation | **3** (Python + 2 Bash) |
| Lignes de code scripts | **~900 lignes commentées** |
| Risques identifiés et cotés | **17** |
| Scénarios d'attaque pentest | **10** |
| POC déjà capturés | **8/25** |

---

## Posture documentaire

Tous les documents sont rédigés en **posture professionnelle** :
- "Nous avons retenu" et non "j'ai choisi"
- "L'analyse initiale a révélé" et non "j'ai vu que"
- "Le ROI mesuré" et non "ça marche"

---

## Conversion finale en PDF (vendredi)

Pour produire les versions PDF imprimables :

```bash
# Installation pandoc
sudo apt install pandoc texlive-xetex

# Conversion Rapport Phase I
pandoc 01_phase_I_analyse/Rapport_Phase_I_Analyse_Besoins.md \
       -o 01_phase_I_analyse/Rapport_Phase_I.pdf \
       --pdf-engine=xelatex \
       --variable=geometry:margin=2cm \
       --variable=mainfont="DejaVu Sans" \
       --toc

# Idem pour les autres documents
```

Alternative : ouvrir le `.md` dans **VS Code + Markdown PDF extension** (clic droit → Export PDF).

---

## Liens utiles

- **Notion projet** : https://www.notion.so/35ddae11bf0d81b69be1d152bacf14fd
- **Kanban Tâches** : (sous-page de la page projet)
- **Budget** : (sous-page de la page projet)
- **GitHub** : Projet_Nova_syndicate_Jedha (branche main)

---

## Note méthodologique

Le périmètre du projet couvre :

1. **Cadrage** (Phase I) : analyse besoins + étude solutions + plan d'exécution.
2. **Conception et déploiement** (Phase II) : architecture cible, déploiement IaC, preuves fonctionnement.
3. **Renforcement** (Phase III) : supervision Wazuh, scripts d'automatisation, PCA/PRA, self-pentest.

Le tout s'inscrit dans un **cadre normatif** : ISO 22301 (continuité), ISO 27001/27031 (sécurité IT), MITRE ATT&CK (cybersécurité), OWASP Top 10 (web), NIST SP 800-207 (Zero Trust), ANSSI (hygiène informatique).
