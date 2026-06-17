# Matrice RACI - Gouvernance, Risque et Conformité

**Objectif** : Clarifier les responsabilités sur l'ensemble des activités GRC pour éviter les zones grises et les responsabilités doubles.
**Référentiels** : ISO 27001 clause 5.3, NIS2 art. 20, DORA art. 5, ISO 38500
**Version** : 1.0
**Date** : [JJ/MM/AAAA]
**Validation** : Direction Générale

---

## Légende RACI

- **R - Responsible** : exécute l'activité (peut être plusieurs).
- **A - Accountable** : rend des comptes, valide, **un seul par activité**.
- **C - Consulted** : consulté avant décision (bidirectionnel).
- **I - Informed** : informé après décision (unidirectionnel).

**Règle d'or** : pour chaque ligne, **un seul A**. Si plusieurs A → conflit garanti.

---

## Rôles types

| Code | Rôle | Description |
|---|---|---|
| DG | Direction Générale / COMEX | Sponsor, décisionnaire stratégique |
| CISO | RSSI | Responsable Sécurité SI |
| DPO | Délégué Protection Données | Conformité RGPD, conseil |
| DSI | Directeur SI | Architecture, exploitation IT |
| LEG | Juridique | Conformité légale, contrats |
| HR | RH | Sécurité ressources humaines |
| OPS | Production / Exploitation | Mise en œuvre opérationnelle |
| DEV | Équipes Développement | Sécurité du code |
| SOC | Security Operations Center | Détection, réponse |
| BU | Directeurs métier | Propriété actifs / risques métier |
| ACH | Achats | Sélection / suivi fournisseurs |
| FIN | Finance / Risk Mgmt | Quantification, assurance |
| AUD | Audit interne | Indépendance, contrôle |

---

## 1. Gouvernance du SMSI

| Activité | DG | CISO | DPO | DSI | LEG | HR | BU | AUD |
|---|---|---|---|---|---|---|---|---|
| Définir la stratégie sécurité (PSSI) | A | R | C | C | C | C | C | I |
| Valider le périmètre SMSI | A | R | C | C | C | I | C | I |
| Présider le Comité de pilotage SMSI | A | R | C | C | I | I | C | I |
| Approuver les budgets sécurité | A | R | I | C | I | I | C | I |
| Définir les indicateurs (KPI/KRI) | I | A,R | C | C | I | I | C | C |
| Valider la cartographie des risques | A | R | C | C | C | C | C | I |
| Revue de Direction annuelle | A | R | C | C | C | C | C | C |
| Communication crise externe | A | C | C | I | C | I | I | I |

---

## 2. Gestion des risques

| Activité | DG | CISO | DPO | DSI | BU | FIN | AUD |
|---|---|---|---|---|---|---|---|
| Définir la méthodologie d'analyse de risques | I | A,R | C | C | C | C | C |
| Identifier les risques | I | R | C | R | R | C | I |
| Évaluer les risques (probabilité, impact) | I | A | C | R | R | C | I |
| Définir les seuils d'acceptation | A | R | C | C | C | C | I |
| Accepter les risques résiduels | A | R | C | C | C | I | I |
| Quantifier financièrement (FAIR) | I | R | C | C | C | A | C |
| Mettre à jour le registre des risques | I | A,R | I | C | C | I | I |
| Souscrire l'assurance cyber | A | C | I | I | I | R | I |

---

## 3. Conformité réglementaire

| Activité | DG | CISO | DPO | LEG | DSI | BU | AUD |
|---|---|---|---|---|---|---|---|
| Veille réglementaire cyber/data | I | C | R | A | I | I | C |
| Conformité ISO 27001 | A | R | C | C | C | C | C |
| Conformité NIS2 | A | R | C | C | C | C | C |
| Conformité DORA (si applicable) | A | R | C | C | R | C | C |
| Conformité RGPD | A | C | R | C | C | C | C |
| Notification CNIL (violation données) | I | C | A,R | C | I | I | I |
| Notification NIS2 (incident significatif) | A | R | I | C | C | I | I |
| AIPD / DPIA | I | C | A,R | C | C | C | I |
| Registre des traitements RGPD | I | I | A,R | C | C | C | I |
| Audits externes / certifications | A | R | C | C | C | I | C |

---

## 4. Sécurité technique

| Activité | DG | CISO | DSI | OPS | DEV | SOC | AUD |
|---|---|---|---|---|---|---|---|
| Architecture sécurité | I | A | R | C | C | C | I |
| Choix solutions sécurité | I | A,R | C | C | C | C | I |
| Gestion des accès et identités | I | A | R | R | I | I | C |
| Revue périodique des habilitations | I | A | R | R | C | I | C |
| Gestion des vulnérabilités | I | A | R | R | C | C | I |
| Patch management | I | C | A | R | C | I | I |
| Chiffrement | I | A | R | R | C | I | C |
| Sauvegardes | I | C | A,R | R | I | I | C |
| Sécurité Cloud | I | A | R | R | C | C | I |
| Sécurité dev (DevSecOps) | I | A | C | C | R | C | I |

---

## 5. Détection et réponse aux incidents

| Activité | DG | CISO | DSI | OPS | SOC | DPO | LEG |
|---|---|---|---|---|---|---|---|
| Définir la stratégie SIEM/EDR | I | A,R | C | C | C | I | I |
| Surveillance 24/7 | I | A | I | I | R | I | I |
| Détection alertes | I | A | I | I | R | I | I |
| Qualification incidents | I | A | C | C | R | C | I |
| Coordination réponse incident majeur | A | R | C | R | R | C | C |
| Investigation forensique | I | A | C | C | R | C | C |
| Communication crise externe | A | C | C | I | I | C | R |
| RETEX et amélioration | I | A,R | C | C | R | C | I |

---

## 6. Continuité d'activité (PCA/PRA)

| Activité | DG | CISO | DSI | OPS | BU | RH |
|---|---|---|---|---|---|---|
| Stratégie de continuité | A | C | R | C | C | I |
| Bilan d'Impact Activité (BIA) | I | C | C | C | A,R | C |
| Plan de Reprise (PRA) | I | A | R | R | C | I |
| Plan de Continuité (PCA) | A | C | C | R | R | C |
| Tests PCA/PRA | I | A | R | R | C | I |
| Cellule de crise | A | R | C | C | C | C |
| Communication de crise | A | C | I | I | C | C |

---

## 7. Sécurité ressources humaines

| Activité | DG | CISO | HR | LEG | BU |
|---|---|---|---|---|---|
| Charte SI | A | R | R | C | I |
| Clauses sécurité dans contrats | I | C | R | A | I |
| Vérification antécédents (background check) | I | C | A,R | C | I |
| Sensibilisation / formation cyber | I | A | R | I | C |
| Tests de phishing | I | A,R | C | C | I |
| Processus offboarding | I | C | A,R | I | C |
| Discipline / sanctions | A | C | R | C | C |

---

## 8. Gestion des tiers (fournisseurs)

| Activité | DG | CISO | DSI | ACH | LEG | DPO |
|---|---|---|---|---|---|---|
| Politique fournisseurs critiques | A | R | C | C | C | C |
| Tiering / classification fournisseurs | I | A,R | C | R | C | C |
| Due diligence sécurité | I | A,R | C | R | C | C |
| Clauses contractuelles sécurité | I | C | C | R | A | C |
| Audit fournisseurs critiques | I | A,R | C | C | C | C |
| Surveillance continue (SLA, incidents) | I | A | R | R | C | I |
| Registre information (DORA art. 28.3) | I | C | R | R | C | I |
| Stratégie de sortie | A | R | C | C | C | I |

---

## 9. Audit et amélioration continue

| Activité | DG | CISO | AUD | DSI | DPO |
|---|---|---|---|---|---|
| Programme d'audit annuel | A | C | R | I | C |
| Audit interne SMSI | I | C | A,R | C | C |
| Audit RGPD | I | C | R | I | A |
| Audit fournisseurs | I | A | R | C | C |
| Suivi des non-conformités | I | A,R | C | C | C |
| Plan d'action correctif | A | R | C | C | C |
| Indicateurs et tableaux de bord | I | A,R | C | C | C |
| Revue de Direction | A | R | C | C | C |

---

## 10. Cas particuliers - Crise majeure cyber

| Activité | DG | CISO | DSI | LEG | DPO | DIR-COM | RH |
|---|---|---|---|---|---|---|---|
| Activation cellule de crise | A | R | C | C | C | C | I |
| Décision déconnexion systèmes critiques | A | R | R | C | I | I | I |
| Communication interne | A | C | I | C | I | R | C |
| Communication clients/partenaires | A | C | I | C | I | R | I |
| Communication presse / réseaux sociaux | A | C | I | C | I | R | I |
| Notification autorités (ANSSI/CNIL) | A | R | I | C | R | I | I |
| Plainte pénale | A | C | I | R | C | I | I |
| Activation assurance cyber | A | C | I | C | I | I | I |
| RETEX post-crise | A | R | C | C | C | C | C |

---

## 11. Règles de cohérence

1. **Un seul A par ligne** : si plusieurs personnes "valident", c'est qu'il n'y a pas de décisionnaire clair.
2. **R = à au moins une personne** : si personne n'exécute, l'activité ne se fait pas.
3. **A peut être R** : un même rôle peut être Accountable et Responsible (ex : RSSI sur la cartographie des risques).
4. **C ≠ I** : Consulted implique un dialogue, Informed une notification.
5. **Limiter les C** : trop de Consulted = paralysie décisionnelle.
6. **Limiter les R** : trop de Responsible = dilution.

---

## 12. Adaptation à la structure

Selon la taille de l'organisation :

- **PME (< 250 personnes)** : DSI + RSSI souvent fusionnés. DPO externalisé. Pas de SOC interne → MSSP.
- **ETI (250-5000)** : RSSI séparé, équipe sécurité 3-5 personnes. SOC externalisé. DPO temps plein.
- **Grand groupe** : Filière RSSI multi-niveaux (Groupe, BU, pays). SOC interne. DPO + équipe.

Mettre à jour la matrice en cas de :
- réorganisation,
- nouveau poste créé,
- externalisation d'un service,
- M&A,
- changement de stratégie sécurité.

---

## 13. Validation

| Signature | Nom | Date |
|---|---|---|
| Direction Générale | | |
| RSSI | | |
| DPO | | |
| DSI | | |
| RH | | |
| Direction Juridique | | |
