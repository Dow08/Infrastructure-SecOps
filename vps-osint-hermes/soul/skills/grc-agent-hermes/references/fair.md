# FAIR — Factor Analysis of Information Risk — Référence opérationnelle

## Pourquoi FAIR

FAIR est **la méthode de référence pour quantifier financièrement le risque cyber**. Standard **Open FAIR** maintenu par The Open Group.

**Différence fondamentale** vs EBIOS / ISO 27005 :
- EBIOS/ISO : qualitatif (faible/moyen/élevé)
- FAIR : **chiffré en euros par an** (pertes annuelles attendues, exposition)

**Pourquoi c'est puissant** : c'est le seul langage que le **CFO et le COMEX** comprennent. "On a un risque élevé de fuite RGPD" ≠ "On a une exposition annuelle estimée entre 280k€ et 1.2M€ pour fuite RGPD". La deuxième phrase débloque un budget.

## Le modèle FAIR

```
        Risque
          │
   ┌──────┴───────┐
   │              │
  LEF        Loss Magnitude
(Loss Event   (Magnitude
 Frequency)    des pertes)
   │              │
┌──┴──┐        ┌──┴───┐
TEF    Vuln    PLM    SLM
       │
    Threat
    Capability
       vs
    Resistance
    Strength
```

### Définitions

| Terme | Définition |
|-------|------------|
| **Risk** | Probabilité × Magnitude des pertes |
| **LEF** (Loss Event Frequency) | Combien de fois par an l'événement de perte se produit |
| **TEF** (Threat Event Frequency) | Combien de fois la menace tente d'attaquer |
| **Vuln** | Probabilité de réussite d'une tentative |
| **TCap** | Capacité de la menace |
| **RS** | Force de résistance du contrôle |
| **PLM** (Primary Loss Magnitude) | Pertes primaires directes |
| **SLM** (Secondary Loss Magnitude) | Pertes secondaires (réputation, sanctions, contentieux) |

### Formule simplifiée

```
ALE (Annual Loss Expectancy) = LEF × LM
```

Où :
- LEF est exprimé en événements/an
- LM est exprimé en € par événement

## Méthode opérationnelle (5 étapes)

### Étape 1 — Identifier le scénario de risque

Un scénario FAIR est précis : **acteur → action → actif → effet**.

**Exemple** :
- Acteur : Cybercriminel externe
- Action : Exfiltration BDD
- Actif : Base clients (100k enregistrements avec emails + données paiement)
- Effet : Fuite de données RGPD

### Étape 2 — Estimer LEF (fréquence)

Utiliser une **distribution PERT à 3 points** (min/likely/max) plutôt qu'un chiffre unique.

**Sources d'estimation** :
- Historique interne (incidents passés sur 5 ans)
- Benchmarks sectoriels (Verizon DBIR, ENISA Threat Landscape, Marsh, Allianz)
- Avis d'experts (RSSI, CERT, prestataire SOC)

**Exemple** : pour notre scénario
- Min : 0.05 / an (1 fois tous les 20 ans)
- Likely : 0.2 / an (1 fois tous les 5 ans)
- Max : 0.5 / an (1 fois tous les 2 ans)

### Étape 3 — Estimer LM (magnitude par événement)

Décomposer en **Primary Loss** et **Secondary Loss**.

#### Primary Loss (pertes directes)
- Coût de réponse à incident (forensic, expertise)
- Coût de remédiation technique
- Pertes de productivité
- Perte de chiffre d'affaires durant indisponibilité
- Vol/détournement direct

#### Secondary Loss (pertes secondaires)
- Sanctions réglementaires (CNIL/RGPD jusqu'à 4% CA mondial)
- Notification clients (forfait + frais)
- Compensation clients
- Contentieux (class actions)
- Perte de clients (churn)
- Perte de contrats prospects (cycle de vente impacté)
- Coût d'opportunité (croissance freinée)
- Coût de communication de crise / RP
- Augmentation prime assurance cyber

**Exemple** : pour fuite 100k clients
- Min : 200 000 €
- Likely : 850 000 €
- Max : 3 500 000 €

### Étape 4 — Calculer ALE avec simulation Monte Carlo

Pourquoi Monte Carlo : la multiplication de deux distributions PERT donne une distribution non-triviale qu'on ne peut pas estimer mentalement.

**Méthode** :
1. Échantillonner LEF selon distribution PERT (10 000 tirages)
2. Échantillonner LM selon distribution PERT (10 000 tirages)
3. Calculer ALE = LEF × LM pour chaque tirage
4. Sortir : médiane, P90, P95 (intervalles de confiance)

**Sortie type** :
- ALE médian : 170 000 € / an
- ALE P90 : 580 000 € / an
- ALE P95 : 850 000 € / an

→ Interprétation : "On peut s'attendre à perdre **170k€/an en moyenne**. Dans 5% des futurs possibles, la perte dépasse **850k€/an**."

(Le script `scripts/calcul_fair.py` automatise ces calculs.)

### Étape 5 — Évaluer les contrôles

Pour chaque contrôle envisagé, estimer la réduction qu'il apporte sur LEF ou LM, et son coût.

**Exemple — DLP + chiffrement BDD** :
- Réduit LEF likely de 0.2 à 0.08 (mesure 1 : DLP empêche exfiltration aisée)
- Réduit LM likely de 850k€ à 350k€ (mesure 2 : chiffrement réduit l'utilité des données volées)
- Nouveau ALE médian : 28 000 € / an
- **Gain annuel attendu** : 142 000 €
- Coût du contrôle (CAPEX+OPEX annualisé) : 80 000 €/an
- **ROI estimé** : +62 000 €/an → contrôle rentable

C'est cette analyse qui permet de **prioriser les investissements** par ROI.

## Distribution PERT — Notion clé

PERT = Beta-PERT. Distribution asymétrique définie par 3 points : min, likely (mode), max.

**Pourquoi PERT** : reflète mieux la réalité que :
- Distribution uniforme (équiprobable, irréaliste)
- Distribution normale (pas de bornes, peut donner du négatif)

**Calcul rapide moyenne PERT** :
```
moyenne ≈ (min + 4×likely + max) / 6
```

Permet une estimation rapide sans Monte Carlo, mais perd l'intervalle de confiance.

## Tableau de bord FAIR

Pour communiquer en Direction :

| Scénario | ALE médian | ALE P95 | Tier de risque |
|----------|-----------:|--------:|----------------|
| Fuite BDD clients (RGPD) | 170 k€/an | 850 k€/an | Élevé |
| Ransomware production | 320 k€/an | 1.2 M€/an | **Critique** |
| Compromission compte admin | 45 k€/an | 280 k€/an | Modéré |
| Indispo site e-commerce >24h | 90 k€/an | 320 k€/an | Modéré |
| **Total exposition cyber** | **625 k€/an** | **2.65 M€/an** | — |

Le total se calcule par sommation des tirages Monte Carlo (pas par addition des médianes — biais).

## Pièges classiques

1. **Estimer un chiffre unique au lieu de PERT** : perte d'information sur l'incertitude.
2. **Confondre TEF et LEF** : TEF = tentatives, LEF = succès. LEF = TEF × Vuln.
3. **Oublier les Secondary Losses** : souvent supérieures aux Primary (réputation, churn).
4. **Estimations sans benchmarks** : trop sensibles au biais. Toujours référencer un rapport public (DBIR, ENISA, IBM Cost of Data Breach).
5. **FAIR en remplacement d'EBIOS** : non, complémentaires. EBIOS identifie les scénarios, FAIR les quantifie.
6. **Communiquer la médiane uniquement** : risque sous-estimé. Toujours afficher P90/P95.

## Mapping FAIR / ISO 27005 / EBIOS

| EBIOS RM | ISO 27005 | FAIR |
|----------|-----------|------|
| Atelier 1-2 (sources, cibles) | Identification | Définition scénario (Acteur/Action/Actif/Effet) |
| Atelier 3-4 (scénarios) | Estimation | LEF + LM (3 points) |
| Atelier 5 (traitement) | Évaluation | Monte Carlo + ROI contrôles |

**Bonne pratique** : EBIOS RM pour identifier les top scénarios (qualitatif), puis FAIR pour quantifier les 5-10 plus critiques.

## Sources de données quantitatives 2024-2025

- **Verizon DBIR** (Data Breach Investigations Report) — annuel, gratuit
- **IBM Cost of a Data Breach Report** — coût moyen par incident par secteur/pays
- **ENISA Threat Landscape** — Europe, gratuit
- **Marsh / Aon / Allianz Cyber Reports** — données issues des claims assurance
- **CNIL — sanctions publiées** — pour calibrer les sanctions RGPD
- **Ponemon Institute** — études coût et fréquence

## Outils

- **Excel + Monte Carlo** : suffisant pour 10-20 scénarios
- **RiskLens** : outil commercial leader FAIR
- **Open FAIR Risk Analysis Tool** : gratuit, basique
- **Python (numpy/scipy)** : pour custom (voir `scripts/calcul_fair.py`)
