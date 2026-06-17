# Mapping multi-cadres — Crosswalk de référence

## Pourquoi ce document

Une organisation moderne est rarement soumise à un seul cadre. Une banque française se trouve simultanément face à :
- **ISO 27001** (contrats donneurs d'ordre, exigence client)
- **DORA** (réglementation sectorielle)
- **NIS2** (entité essentielle)
- **RGPD** (toutes données personnelles)
- **NIST CSF** (pilotage interne)
- **SOC 2** (clients US)

L'erreur classique : ouvrir 6 chantiers parallèles. La bonne approche : **un seul SMSI ISO 27001 enrichi**, qui sert de socle commun à tous les autres cadres.

## Principe : ISO 27001 comme socle pivot

ISO 27001:2022 (clauses + Annexe A 93 contrôles) couvre :
- ~80% des exigences NIS2
- ~70% des exigences DORA
- ~75% des exigences RGPD sécurité (art. 32)
- 100% du socle NIST CSF (équivalence directe)
- ~90% des contrôles SOC 2 Trust Service Criteria

Le travail = identifier les **20% de différentiel** par cadre et compléter.

## Tableau de correspondance maître

### Gouvernance et leadership

| Sujet | ISO 27001 | NIST CSF 2.0 | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|---------------|------|------|------|-------|
| Engagement Direction | Clause 5.1 | GV.RR-01 | Art. 20 | Art. 5 | Art. 24 | CC1.1 |
| Politique sécurité | Clause 5.2 + A.5.1 | GV.PO-01 | Mes. 1 | Art. 9 | Art. 24 | CC2.1 |
| Rôles et responsabilités | Clause 5.3 + A.5.2 | GV.RR-02 | Mes. 9 | Art. 6 | Art. 24, 28, 37 | CC1.2 |
| Comité sécurité | Implicite | GV.OV-01 | Implicite | Art. 5.2 | DPO | CC1.4 |

### Gestion des risques

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Identification | Clause 6.1.2 | ID.RA-01/02 | Mes. 1 | Art. 8 | Art. 35 (DPIA) | CC3.1 |
| Analyse | Clause 6.1.2 + ISO 27005/EBIOS | ID.RA-03/05 | Mes. 1 | Art. 6 | Art. 35 | CC3.2 |
| Traitement | Clause 6.1.3 | ID.RA-06 | Mes. 1 | Art. 6 | Art. 24, 32 | CC3.3 |
| Acceptation | Clause 8.3 (validation Direction) | GV.RM-04 | Implicite | Art. 5 | Art. 24 | CC3.4 |

### Inventaire et classification

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Inventaire actifs | A.5.9 | ID.AM-01/02 | Mes. 10 | Art. 8 | Art. 30 (registre) | CC6.1 |
| Classification info | A.5.12-14 | ID.AM-05 | Implicite | Art. 8 | Sensibles (art. 9) | C1.1 |
| Étiquetage | A.5.13 | ID.AM-05 | Implicite | Art. 8 | Implicite | C1.1 |

### Contrôle d'accès et identités

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Politique accès | A.5.15 | PR.AA-01 | Mes. 10 | Art. 9 | Art. 32 | CC6.1 |
| Authentification | A.5.17 + A.8.5 | PR.AA-03/04 | Mes. 11 (MFA) | Art. 9 | Art. 32 | CC6.1 |
| Privilégiés | A.8.2 | PR.AA-05 | Mes. 15 | Art. 9 | Art. 32 | CC6.1 |
| Revue accès | A.5.18 | PR.AA-05 | Mes. 10 | Art. 9 | Art. 32 | CC6.1 |

### Sécurité technique

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Chiffrement | A.8.24 | PR.DS-01/02 | Mes. 8 | Art. 9 | Art. 32 | CC6.7 |
| Configuration | A.8.9 | PR.PS-01 | Implicite | Art. 9 | Implicite | CC6.8 |
| Vulnérabilités | A.8.8 | ID.RA-01 | Mes. 13 | Art. 8 | Art. 32 | CC7.1 |
| Backup | A.8.13 | PR.DS-11 | Mes. 3 | Art. 11 | Implicite | A1.2 |
| Cryptographie clés | A.8.24 | PR.DS-02 | Mes. 8 | Art. 9 | Art. 32 | CC6.7 |

### Détection et surveillance

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Journalisation | A.8.15 | DE.CM-01 | Implicite | Art. 9 | Art. 32 | CC7.2 |
| Surveillance | A.8.16 | DE.CM-01/03 | Implicite | Art. 10 | Art. 32 | CC7.2 |
| Détection anomalies | A.8.16 | DE.AE-01/02 | Implicite | Art. 10 | Implicite | CC7.3 |
| SIEM/SOC | Implicite | DE.CM, DE.AE | Implicite | Art. 10 | Implicite | CC7.2 |

### Gestion des incidents

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Plan IR | A.5.24-25 | RS.MA-01 | Mes. 2 | Art. 17 | Art. 33 | CC7.4 |
| Notification autorité | Implicite | RS.CO-01 | Art. 23 (24h/72h/1m) | Art. 19 (4h/72h/1m) | Art. 33 (72h CNIL) | CC7.4 |
| Notification personnes | Implicite | RS.CO-02 | Implicite | Art. 19 | Art. 34 | CC7.4 |
| Forensic | A.5.28 | RS.AN-03 | Implicite | Art. 17 | Implicite | CC7.5 |
| Leçons apprises | A.5.27 | RS.AN-08 | Implicite | Art. 17 | Implicite | CC7.5 |

### Continuité et résilience

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| BIA | A.5.29 | ID.AM-04 | Mes. 3 | Art. 11 | Implicite | A1.1 |
| Plan continuité | A.5.30 | RC.RP-01 | Mes. 3 | Art. 11 | Art. 32 | A1.2 |
| Tests | A.5.30 | RC.RP-04 | Mes. 3 | Art. 11 + Art. 24-27 (TLPT) | Art. 32 | A1.3 |

### Supply chain / Fournisseurs

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Politique | A.5.19 | GV.SC-01 | Mes. 4 | Art. 28 | Art. 28 | CC9.2 |
| Clauses contractuelles | A.5.20 | GV.SC-02 | Mes. 4 | Art. 30 | Art. 28 | CC9.2 |
| Évaluation | A.5.21 | GV.SC-06 | Mes. 4 | Art. 28 | Art. 32 | CC9.2 |
| Surveillance continue | A.5.22 | GV.SC-07 | Mes. 4 | Art. 28 | Implicite | CC9.2 |
| Stratégie de sortie | Implicite | Implicite | Implicite | Art. 28.8 | Implicite | Implicite |

### RH et sensibilisation

| Sujet | ISO 27001 | NIST CSF | NIS2 | DORA | RGPD | SOC 2 |
|-------|-----------|----------|------|------|------|-------|
| Vérification recrutement | A.6.1 | PR.AT-01 | Mes. 9 | Art. 9 | Implicite | CC1.4 |
| Conditions emploi | A.6.2 | PR.AT-01 | Mes. 9 | Art. 9 | Art. 32 | CC1.4 |
| Sensibilisation | A.6.3 | PR.AT-01/02 | Mes. 7 | Art. 13 | Art. 39 (DPO) | CC1.4 |
| Sanctions | A.6.4 | PR.AT-01 | Mes. 9 | Art. 9 | Implicite | CC1.5 |
| Départ | A.6.5 | PR.AA-04 | Mes. 9 | Art. 9 | Implicite | CC6.2 |

### Spécificités DORA non couvertes par ISO 27001

À traiter en complément si soumis à DORA :

| Exigence DORA | Article | Description |
|---------------|---------|-------------|
| Tests TLPT | Art. 26-27 | Threat-Led Pen Test tous les 3 ans (entités significatives) |
| Registre d'information | Art. 28.3 | Format européen standardisé, annuel |
| Stratégie de sortie | Art. 28.8 | Pour chaque prestataire critique |
| Notification 4h | Art. 19 | Initial alert (plus strict que NIS2) |
| Classification incidents 7 critères | Art. 18 | Méthodologie spécifique DORA |

### Spécificités NIS2 non couvertes par ISO 27001

| Exigence NIS2 | Article | Description |
|---------------|---------|-------------|
| Enregistrement entité | Art. 27 | Auprès du CSIRT national |
| Formation dirigeants | Art. 20 | Spécifique cybersécurité, régulière |
| Notification incident 24h | Art. 23 | Plus strict que ISO |
| Responsabilité personnelle dirigeants | Art. 20 | Concept ISO ne pose pas |

### Spécificités RGPD non couvertes par ISO 27001

| Exigence RGPD | Article | Description |
|---------------|---------|-------------|
| Registre des traitements | Art. 30 | Format spécifique CNIL |
| DPIA / AIPD | Art. 35 | Méthodologie spécifique |
| DPO | Art. 37-39 | Désignation, indépendance, missions |
| Droits des personnes | Art. 15-22 | Procédure de gestion 1 mois |
| Bases légales | Art. 6 | Documentation exigée |
| Transferts hors UE | Art. 44-49 | SCC, BCR, etc. |
| Information transparence | Art. 13-14 | Mentions au moment de la collecte |

## Cas pratiques de mapping

### Cas 1 : ESN soumise NIS2 (entité importante)
**Statut** : ISO 27001 oui, NIS2 nouvelle.
**Travail différentiel** :
- Enregistrement ANSSI (Art. 27 NIS2)
- Formation dirigeants formalisée (Art. 20)
- Procédure notification 24h/72h/1m testée
- Revue contrats fournisseurs avec clauses NIS2
- Évaluation supply chain documentée

### Cas 2 : Banque soumise DORA + NIS2 + ISO 27001 + RGPD
**Statut** : ISO oui, NIS2 oui, DORA neuve.
**Travail différentiel** :
- Registre d'information DORA (Art. 28.3)
- Programme tests résilience formalisé (Art. 24)
- Préparation TLPT (Art. 26-27) si significative
- Notification 4h opérationnelle (Art. 19, plus strict que NIS2)
- Stratégies de sortie pour prestataires critiques (Art. 28.8)

### Cas 3 : SaaS B2B avec clients US + UE
**Statut** : ISO ou SOC 2, RGPD obligatoire.
**Travail différentiel** :
- SOC 2 Type II (audit annuel externe)
- DPF (Data Privacy Framework) ou SCC pour transferts US → UE
- DPO ou point de contact RGPD
- Registre des traitements
- Bases légales documentées par traitement

## Recommandation de séquence

Si une organisation part de zéro et est concernée par plusieurs cadres :

```
1. Définir périmètre et gouvernance (clause 4-5 ISO)
2. Analyse de risques EBIOS RM (compatible ISO 27005)
3. Construire le SMSI ISO 27001 (Annexe A 93 contrôles)
4. Ajouter les compléments NIS2 (notification, formation dirigeants, supply chain)
5. Ajouter les compléments RGPD (registre, AIPD, DPO)
6. Si secteur financier : ajouter compléments DORA (TLPT, registre information)
7. Si maturité internationale visée : mapping NIST CSF pour reporting
8. Si SOC 2 visé : audit externe Type II
```

Une seule politique de sécurité, un seul SMSI, plusieurs déclinaisons documentaires.
