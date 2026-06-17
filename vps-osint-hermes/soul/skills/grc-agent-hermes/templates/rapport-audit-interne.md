# Rapport d'Audit Interne du SMSI

**Référentiel** : ISO 27001:2022 clause 9.2, ISO 19011:2018 (lignes directrices audit)
**Périmètre audité** : [À préciser - ex : Direction des Systèmes d'Information]
**Période d'audit** : du [JJ/MM/AAAA] au [JJ/MM/AAAA]
**Auditeur(s)** : [Nom + qualification ISO 27001 Lead Auditor / interne]
**Audité(s)** : [Représentants des entités auditées]
**Date du rapport** : [JJ/MM/AAAA]
**Version** : 1.0
**Diffusion** : Direction, RSSI, Comité de pilotage SMSI

---

## 1. Synthèse exécutive

### 1.1 Objectif de l'audit

Vérifier la conformité et l'efficacité du Système de Management de la Sécurité de l'Information (SMSI) par rapport à :
- la norme ISO/IEC 27001:2022,
- les politiques et procédures internes,
- les exigences réglementaires applicables (RGPD, NIS2, DORA selon le cas),
- les exigences contractuelles clients.

### 1.2 Conclusion globale

**[Conforme / Conforme avec remarques / Non conforme]**

Le SMSI est dans l'ensemble [opérationnel et maîtrisé / partiellement conforme / présentant des écarts significatifs]. Les principaux points forts sont [...]. Les principales zones d'amélioration concernent [...].

### 1.3 Résultats chiffrés

| Indicateur | Valeur |
|---|---|
| Nombre de contrôles audités | XX / 93 (Annexe A) |
| Conformités | XX (XX%) |
| Non-conformités majeures (NC) | X |
| Non-conformités mineures (nc) | X |
| Observations / opportunités d'amélioration (OA) | XX |
| Bonnes pratiques relevées | X |

### 1.4 Top 5 actions prioritaires

| # | Action | Échéance | Owner |
|---|---|---|---|
| 1 | ... | T+30j | ... |
| 2 | ... | T+60j | ... |
| 3 | ... | T+90j | ... |
| 4 | ... | T+120j | ... |
| 5 | ... | T+180j | ... |

---

## 2. Périmètre et méthodologie

### 2.1 Périmètre

- **Organisationnel** : entités, sites, processus métier inclus
- **Technique** : infrastructures, applications, données dans le scope ISMS
- **Géographique** : pays, sites
- **Hors périmètre** : éléments explicitement exclus + justification

### 2.2 Documents audités

- Politique de sécurité (PSSI v[X])
- Déclaration d'Applicabilité (SoA) du [date]
- Plan de traitement des risques
- Registre des risques
- Procédures opérationnelles
- Comptes-rendus des comités de pilotage
- Indicateurs et tableaux de bord

### 2.3 Personnes rencontrées

| Date | Personne | Fonction | Sujet |
|---|---|---|---|
| | RSSI | | Gouvernance, gestion risques |
| | DSI | | Architecture, exploitation |
| | DPO | | Conformité RGPD |
| | Responsable RH | | Sécurité ressources humaines |
| | Responsable Achats | | Sécurité fournisseurs |
| | Lead Dev | | Sécurité dev (DevSecOps) |
| | Utilisateurs | | Sensibilisation, vécu |

### 2.4 Méthodologie

- Revue documentaire
- Entretiens semi-directifs
- Échantillonnage et tests :
  - Échantillon de [N] habilitations utilisateurs vérifiées
  - Échantillon de [N] modifications de configuration analysées
  - Échantillon de [N] incidents traités
  - Test de restauration d'une sauvegarde
  - Vérification physique de [N] sites
- Observation directe (badges, surveillance, déchets sensibles, écrans non verrouillés...)

---

## 3. Évaluation des clauses ISO 27001:2022

### 3.1 Clause 4 - Contexte de l'organisation

| Critère | Constat | Conformité |
|---|---|---|
| 4.1 Enjeux internes/externes identifiés | Document à jour, dernière revue [date] | Conforme |
| 4.2 Parties intéressées | Cartographie partielle, attentes clients à formaliser | Observation |
| 4.3 Périmètre du SMSI | Documenté, mais 2 sites manquants | nc |
| 4.4 SMSI établi | Processus définis | Conforme |

### 3.2 Clause 5 - Leadership

| Critère | Constat | Conformité |
|---|---|---|
| 5.1 Engagement Direction | PSSI signée Direction Générale 2025, revues trimestrielles | Conforme |
| 5.2 Politique sécurité | Diffusée, accessible intranet | Conforme |
| 5.3 Rôles et responsabilités | RSSI nommé, RACI à compléter pour 3 processus | Observation |

### 3.3 Clause 6 - Planification

| Critère | Constat | Conformité |
|---|---|---|
| 6.1.2 Appréciation des risques | Méthode EBIOS RM appliquée, 47 risques identifiés | Conforme |
| 6.1.3 Traitement des risques | Plan documenté, SoA à jour | Conforme |
| 6.2 Objectifs sécurité mesurables | 5 objectifs définis, 2 sans indicateur quantitatif | nc |
| 6.3 Planification des changements | Processus formel manquant | NC |

### 3.4 Clause 7 - Support

| Critère | Constat | Conformité |
|---|---|---|
| 7.1 Ressources | Budget validé, équipe RSSI 2 ETP | Conforme |
| 7.2 Compétences | Plan de formation existe, suivi partiel | Observation |
| 7.3 Sensibilisation | Campagne annuelle effectuée, 87% taux complétion | Conforme |
| 7.4 Communication | Plan communication interne formalisé | Conforme |
| 7.5 Informations documentées | Maîtrise documentaire, GED à jour | Conforme |

### 3.5 Clause 8 - Fonctionnement

| Critère | Constat | Conformité |
|---|---|---|
| 8.1 Planification et maîtrise | Procédures opérationnelles existent | Conforme |
| 8.2 Appréciation périodique des risques | Effectuée annuellement, dernier en [date] | Conforme |
| 8.3 Traitement des risques | Plan exécuté à 78% | Observation |

### 3.6 Clause 9 - Évaluation des performances

| Critère | Constat | Conformité |
|---|---|---|
| 9.1 Surveillance, mesure, analyse, évaluation | Tableau de bord mensuel produit | Conforme |
| 9.2 Audit interne | Programme audit annuel, présent audit | Conforme |
| 9.3 Revue de direction | Effectuée [date], décisions documentées | Conforme |

### 3.7 Clause 10 - Amélioration

| Critère | Constat | Conformité |
|---|---|---|
| 10.1 Amélioration continue | Boucle PDCA active | Conforme |
| 10.2 Non-conformités et actions correctives | 12 NC ouvertes sur année, 9 closes, 3 en cours | Conforme |

---

## 4. Évaluation des contrôles Annexe A (extrait)

> Détail complet en annexe. Focus ici sur les écarts significatifs.

### 4.1 Contrôles organisationnels (A.5)

| Contrôle | Constat | Niveau |
|---|---|---|
| A.5.1 Politiques | PSSI complète, 12 politiques satellites | Conforme |
| A.5.7 Threat intelligence | Pas de processus formalisé, abonnement CERT-FR uniquement | nc |
| A.5.15 Contrôle d'accès | Politique à jour, revues semestrielles | Conforme |
| A.5.23 Sécurité services Cloud | 3 fournisseurs Cloud, 1 sans clauses sécurité contractuelles | NC |
| A.5.30 Préparation TIC PCA | PCA existant, dernier test > 18 mois | NC |

### 4.2 Contrôles personnels (A.6)

| Contrôle | Constat | Niveau |
|---|---|---|
| A.6.3 Sensibilisation | 87% complétion, objectif 100% | Observation |
| A.6.7 Télétravail | Charte télétravail signée par tous | Conforme |
| A.6.8 Signalement incidents | Procédure connue, 14 signalements 2025 | Conforme |

### 4.3 Contrôles physiques (A.7)

| Contrôle | Constat | Niveau |
|---|---|---|
| A.7.1 Périmètres physiques | Badges + sas, contrôle satisfaisant | Conforme |
| A.7.4 Surveillance physique | CCTV opérationnelle, registre RGPD à actualiser | nc |
| A.7.7 Bureau et écran clairs | 4 postes observés non verrouillés sur 30 | nc |

### 4.4 Contrôles technologiques (A.8)

| Contrôle | Constat | Niveau |
|---|---|---|
| A.8.5 Authentification sécurisée | MFA déployé à 95%, comptes service exclus = risque | nc |
| A.8.7 Protection malware | EDR sur 100% endpoints | Conforme |
| A.8.8 Gestion vulnérabilités | Scans mensuels, SLA patch critique 30j non respecté | NC |
| A.8.9 Gestion configurations | CMDB partielle, écart 12% avec inventaire réel | nc |
| A.8.12 DLP | Solution déployée Q4 2025, monitoring en cours | Conforme |
| A.8.15 Logs | Centralisation Splunk, conservation 13 mois | Conforme |
| A.8.16 Surveillance activités | UEBA partiel, 5 cas faux positifs | Observation |
| A.8.23 Filtrage web | Proxy + DNS filtering | Conforme |
| A.8.28 Codage sécurisé | Lignes directrices publiées, formation dev 60% | Observation |

---

## 5. Détail des non-conformités

### NC-2026-001 - Plan de traitement DR non testé

- **Contrôle** : A.5.30, A.8.14, ISO 27001 clause 8.1
- **Constat** : Le dernier test de bascule du Plan de Reprise d'Activité date de 19 mois. La politique exige un test annuel.
- **Risque** : En cas de sinistre majeur, l'organisation n'a pas de garantie sur le RTO de 4h annoncé.
- **Preuve** : Rapport de test daté du [date], aucun test postérieur.
- **Cause racine** : Absence de planification opérationnelle, équipe sous-dimensionnée Q1-Q2 2025.
- **Action corrective demandée** : Planifier et exécuter un test PRA complet d'ici 90 jours, formaliser un calendrier triennal des tests.
- **Échéance** : 90 jours
- **Owner** : RSSI + DSI

### NC-2026-002 - Fournisseur Cloud sans clauses sécurité

- **Contrôle** : A.5.23, A.5.19, A.5.20
- **Constat** : Le contrat avec [Prestataire X] (hébergement application Z) ne contient pas de clauses sécurité minimales (chiffrement, journalisation, notification incident, droit d'audit).
- **Risque** : Pas de recours contractuel en cas d'incident, non-conformité RGPD art. 28.
- **Preuve** : Contrat consulté, annexe sécurité absente.
- **Cause racine** : Procédure d'achat de 2022 ne couvrait pas ce volet.
- **Action corrective demandée** : Avenant au contrat sous 60 jours intégrant les clauses standard de l'organisation. Mettre à jour la procédure d'achat pour rendre obligatoire la revue sécurité avant signature.
- **Échéance** : 60 jours
- **Owner** : Achats + RSSI + Juridique

### NC-2026-003 - SLA patch critique non respecté

- **Contrôle** : A.8.8
- **Constat** : Le SLA de 30 jours pour les patchs CVSS ≥ 9 n'est pas respecté. Sur 24 vulnérabilités critiques identifiées en 2025, 9 ont été corrigées avec un délai > 30 jours, dont 3 > 60 jours.
- **Risque** : Fenêtre d'exploitation prolongée, exposition à des attaques opportunistes.
- **Preuve** : Rapport mensuel scan Qualys, extraction 2025.
- **Cause racine** : Coordination Patch Management / Métier, fenêtres de maintenance restreintes.
- **Action corrective demandée** : Mettre en place un processus d'exception documenté pour les patchs critiques (compensating controls + escalade Direction). Cibler 95% de patchs critiques dans le SLA d'ici Q4.
- **Échéance** : 90 jours
- **Owner** : DSI + RSSI

### NC-2026-004 - Processus formel de planification des changements

- **Contrôle** : ISO 27001 clause 6.3
- **Constat** : Les changements impactant le SMSI ne font pas l'objet d'une planification formelle (analyse impact, ressources, communication).
- **Risque** : Changements non maîtrisés, perte de cohérence du SMSI.
- **Action corrective demandée** : Formaliser une procédure de gestion des changements SMSI, l'inclure dans le périmètre des comités trimestriels.
- **Échéance** : 60 jours
- **Owner** : RSSI

---

## 6. Détail des non-conformités mineures

> Liste synthétique, détails en annexe.

| ID | Contrôle | Constat résumé | Échéance |
|---|---|---|---|
| nc-2026-001 | 4.3 | Périmètre SMSI omet 2 sites annexes | 30j |
| nc-2026-002 | 6.2 | 2 objectifs sans indicateur mesurable | 30j |
| nc-2026-003 | A.5.7 | Pas de processus threat intel formalisé | 90j |
| nc-2026-004 | A.6.3 | Sensibilisation 87% au lieu de 100% | 60j |
| nc-2026-005 | A.7.4 | Registre RGPD CCTV à actualiser | 30j |
| nc-2026-006 | A.7.7 | 13% postes observés non verrouillés | 60j (campagne) |
| nc-2026-007 | A.8.5 | Comptes service exclus de la MFA | 90j |
| nc-2026-008 | A.8.9 | CMDB partielle (écart 12%) | 90j |

---

## 7. Observations et opportunités d'amélioration

1. Industrialiser la **threat intelligence** en intégrant un flux MISP automatisé.
2. Étendre la **revue d'accès** aux comptes de service (souvent oubliés).
3. Étendre les **tests de phishing** à des scénarios sectoriels (banque, supply chain).
4. Évaluer un **outil GRC** pour automatiser SoA, registre risques, KPI.
5. Mettre en place un **comité dédié IA et données** anticipant l'AI Act.
6. Renforcer la **chaîne tierce** (formaliser tiering fournisseurs, audits annuels Top 10).
7. Élargir le **DevSecOps** : SAST/DAST sur 100% pipelines, SBOM systématique.
8. Documenter formellement la **stratégie de sortie** pour les 3 services Cloud critiques.

---

## 8. Bonnes pratiques relevées

- Sponsorship Direction Générale fort, présence aux comités SMSI.
- Plateforme GRC partiellement automatisée (registre risques, SoA).
- Programme de sensibilisation engageant (gamification, escape game cyber).
- Tableaux de bord mensuels lisibles, partagés au CODIR.
- Maturité élevée sur la gestion des incidents (procédure, RETEX systématique).

---

## 9. Plan d'action consolidé

| ID | Action | Priorité | Owner | Échéance | Indicateur de clôture |
|---|---|---|---|---|---|
| NC-001 | Test PRA complet | Haute | RSSI/DSI | 90j | Rapport test validé |
| NC-002 | Avenant contrat fournisseur | Haute | Achats | 60j | Contrat signé |
| NC-003 | Plan patch critique | Haute | DSI | 90j | 95% SLA respecté |
| NC-004 | Procédure changements SMSI | Moyenne | RSSI | 60j | Procédure publiée |
| nc-* | Corrections mineures | Moyenne | Divers | 30-90j | Selon détail |
| OA-1 | Threat intel automatisée | Moyenne | RSSI | 6 mois | Flux MISP opérationnel |
| OA-* | Autres opportunités | Variable | Divers | 6-12 mois | À définir par owner |

---

## 10. Conclusion et recommandations à la Direction

Le SMSI démontre un niveau de maturité satisfaisant, ancré dans une démarche d'amélioration continue. Les non-conformités identifiées sont **traitables sans investissement majeur** (estimation 80-120 k€) et **n'empêchent pas l'organisation de soutenir un audit de certification ISO 27001 externe** à condition que les 4 NC majeures soient closes avant la visite de certification.

**Recommandations stratégiques** :
1. Maintenir le sponsorship Direction et la dynamique PDCA.
2. Lancer le plan d'action selon échéances proposées.
3. Programmer le prochain audit interne dans 12 mois.
4. Envisager la certification externe ISO 27001:2022 d'ici 18 mois.

---

## Annexes

- Annexe 1 : Programme d'audit détaillé
- Annexe 2 : Liste des documents consultés
- Annexe 3 : Échantillons audités (anonymisés)
- Annexe 4 : Détail des constats par contrôle Annexe A (93 lignes)
- Annexe 5 : Pièces jointes et preuves

---

| Signature | Nom | Fonction | Date |
|---|---|---|---|
| Auditeur principal | | | |
| Audités (visa) | | | |
| RSSI | | | |
| Direction | | | |
