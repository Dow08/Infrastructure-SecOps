# NIST Cybersecurity Framework 2.0 — Référence opérationnelle

## Pourquoi NIST CSF

Framework américain agnostique (NIST = National Institute of Standards and Technology), de facto **standard international** pour exprimer la **maturité cyber** d'une organisation, quel que soit le secteur.

**Avantage majeur** : c'est un cadre de **communication**, pas une norme contraignante. Il s'utilise pour :
- Évaluer la maturité interne
- Communiquer avec le CODIR/CA en termes clairs
- Prioriser les investissements cyber
- Mapper plusieurs cadres (ISO, NIS2, DORA) sur une vue unifiée

**Version 2.0** publiée en février 2024. Évolution majeure : ajout de la **6ème fonction Govern (Gouvernance)**.

## Les 6 fonctions (CSF 2.0)

```
        GOVERN (GV)
        ↓
IDENTIFY → PROTECT → DETECT → RESPOND → RECOVER
   ↑                                          |
   └──────────────── Amélioration continue ──┘
```

| Fonction | Acronyme | Objectif |
|----------|----------|----------|
| **Govern** | GV | Établir et surveiller la stratégie cyber, gestion des risques, attentes |
| **Identify** | ID | Comprendre les risques (actifs, parties prenantes, gouvernance) |
| **Protect** | PR | Mettre en œuvre les protections (accès, formation, données, infra) |
| **Detect** | DE | Détecter les événements cyber (monitoring, anomalies) |
| **Respond** | RS | Agir face aux incidents (réponse, communication, atténuation) |
| **Recover** | RC | Rétablir capacités et services (planification, communication, amélioration) |

### Govern (NOUVEAU en 2.0)

Sous-catégories principales :
- **GV.OC** : Contexte organisationnel
- **GV.RM** : Stratégie de gestion des risques
- **GV.RR** : Rôles, responsabilités et autorités
- **GV.PO** : Politiques
- **GV.OV** : Supervision
- **GV.SC** : Gestion des risques chaîne d'approvisionnement

### Identify

- **ID.AM** : Asset Management — inventaire matériel, logiciel, données
- **ID.RA** : Risk Assessment — identification des vulnérabilités et menaces
- **ID.IM** : Improvement — amélioration continue

### Protect

- **PR.AA** : Identity Management, Authentication, Access Control
- **PR.AT** : Awareness & Training
- **PR.DS** : Data Security
- **PR.PS** : Platform Security
- **PR.IR** : Technology Infrastructure Resilience

### Detect

- **DE.CM** : Continuous Monitoring
- **DE.AE** : Adverse Event Analysis

### Respond

- **RS.MA** : Incident Management
- **RS.AN** : Incident Analysis
- **RS.CO** : Communication
- **RS.MI** : Mitigation

### Recover

- **RC.RP** : Recovery Plan execution
- **RC.CO** : Communication

## Échelle de maturité (Tiers)

CSF propose 4 niveaux de maturité, à appliquer **fonction par fonction** (ou catégorie par catégorie) :

| Tier | Nom | Description |
|------|-----|-------------|
| **1** | Partial | Pratiques ad hoc, réactives, peu de partage d'information |
| **2** | Risk Informed | Conscience du risque, mais pas de processus formel à l'échelle de l'organisation |
| **3** | Repeatable | Politiques formelles, application cohérente, processus de gestion des risques formalisé |
| **4** | Adaptive | Apprend de l'expérience, partage info, adaptation continue |

**À l'usage**, en France on utilise souvent une échelle 0-4 ou 0-5 plus granulaire (voir `scripts/scoring_maturite_nist_csf.py`).

## Profils (Profiles)

Un **profil** est l'alignement des fonctions/catégories avec :
- les exigences business
- la tolérance au risque
- les ressources

On distingue :
- **Profil actuel** (Current) — état des lieux
- **Profil cible** (Target) — où on veut aller

Le **gap** entre les deux = plan d'action.

## Méthode d'évaluation rapide (4-6 semaines)

### Semaine 1-2 : Cadrage
- Périmètre (entité, BU, services)
- Interlocuteurs identifiés (RSSI, DSI, métiers)
- Liste des documents à demander

### Semaine 2-4 : Évaluation
- Entretiens (CISO/RSSI, DSI, Risk, métiers critiques)
- Revue documentaire (politiques, procédures, preuves)
- Scoring par sous-catégorie sur échelle 0-4

### Semaine 4-5 : Synthèse
- Heat map maturité par fonction
- Identification des "low hangers" (low effort / high impact)
- Définition profil cible

### Semaine 5-6 : Roadmap
- Plan d'action prioritisé
- KPI de suivi
- Présentation Direction

## Sortie type — Heat map par fonction

| Fonction | Score actuel | Score cible | Gap | Priorité |
|----------|-------------:|------------:|----:|----------|
| Govern | 1.8 | 3.0 | 1.2 | Haute |
| Identify | 2.5 | 3.0 | 0.5 | Moyenne |
| Protect | 2.2 | 3.5 | 1.3 | Haute |
| Detect | 1.5 | 3.0 | 1.5 | **Critique** |
| Respond | 2.0 | 3.0 | 1.0 | Moyenne |
| Recover | 1.2 | 3.0 | 1.8 | **Critique** |

→ Le gap le plus large = priorité d'investissement.

## Mapping NIST CSF / ISO 27001 / NIS2

NIST publie des "Informative References" qui mappent CSF aux principaux cadres :

| NIST CSF | ISO 27001:2022 | NIS2 Art. 21 |
|----------|----------------|--------------|
| GV.OC | Clause 4 | Implicite |
| GV.RM | Clause 6.1 | Mesure 1 |
| GV.RR | Clause 5.3 | Mesure 9 |
| GV.PO | Clause 5.2 + A.5.1 | Mesure 1 |
| GV.SC | A.5.19-22 | Mesure 4 |
| ID.AM | A.5.9-11 | Mesure 10 |
| PR.AA | A.5.15-18 | Mesures 10, 11, 15 |
| PR.AT | A.6.3 | Mesure 7 |
| PR.DS | A.8.10-12, A.8.24 | Mesure 8 |
| DE.CM | A.8.16 | Implicite |
| RS.MA | A.5.24-27 | Mesure 2 |
| RC.RP | A.5.29-30 | Mesure 3 |

## Quand utiliser NIST CSF plutôt qu'ISO 27001 ?

| Besoin | Utilise |
|--------|---------|
| Certification commerciale | ISO 27001 |
| Évaluation maturité interne (sans certif) | NIST CSF |
| Conformité réglementaire EU | NIS2/DORA + ISO 27001 |
| Communication CODIR/CA | NIST CSF (plus accessible) |
| Mapping multi-cadres | NIST CSF (rôle de pivot) |
| Marché US ou international | NIST CSF (langage commun) |

**Bonne pratique** : utiliser NIST CSF pour le **pilotage**, ISO 27001 pour la **structuration formelle**, EBIOS RM pour l'**analyse de risques détaillée**.

## Pièges à éviter

1. **Coter sans preuves** : un score 3 doit être justifié par un document/processus, pas par une déclaration verbale.
2. **Ne pas coter Govern** (la nouvelle fonction) : c'est souvent là que les gaps sont les plus visibles.
3. **Profile cible 4 partout** : irréaliste. Une maturité 3 partout est déjà très solide.
4. **Pas de revue annuelle** : le profil change. À réévaluer chaque année.
5. **Confondre maturité et conformité** : on peut être conforme ISO 27001 avec une maturité CSF de 2 sur certains domaines.

## Pour aller plus loin

- NIST CSF 2.0 (PDF) : nist.gov/cyberframework
- Implementation Examples : exemples concrets par sous-catégorie
- Quick Start Guides : par type d'organisation (PME, secteur public, etc.)
