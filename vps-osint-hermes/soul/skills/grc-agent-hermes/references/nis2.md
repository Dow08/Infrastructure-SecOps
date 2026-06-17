# NIS2 — Directive (UE) 2022/2555 — Référence opérationnelle

## Pourquoi NIS2

NIS2 remplace NIS1 (2016) avec un périmètre **massivement élargi** :
- Avant : ~500 OIV/OSE en France
- Après : **~15 000 entités** concernées
- Transposition en France : loi du **30 octobre 2024** (loi REVOSCYB) + décrets 2025

Si l'utilisateur travaille dans une entreprise de **>50 salariés** ou **>10M€ CA** dans un des secteurs visés, **NIS2 s'applique probablement**.

## Qui est concerné ?

### Deux catégories d'entités

| Type | Critères | Secteurs |
|------|----------|----------|
| **Essentielles (EE)** | >250 salariés OU >50M€ CA / 43M€ bilan | Secteurs Annexe I |
| **Importantes (EI)** | >50 salariés OU >10M€ CA | Secteurs Annexes I + II |

### Secteurs hautement critiques (Annexe I)
1. Énergie (électricité, gaz, pétrole, hydrogène)
2. Transports (aérien, ferroviaire, maritime, routier)
3. Secteur bancaire
4. Infrastructures des marchés financiers
5. Santé (hôpitaux, labos, recherche, dispositifs médicaux)
6. Eau potable
7. Eaux usées
8. Infrastructures numériques (DNS, TLD, IXP, datacenters, cloud, CDN)
9. Gestion services TIC B2B (MSP, MSSP)
10. Administrations publiques
11. Espace

### Secteurs critiques (Annexe II)
1. Services postaux et courriers
2. Gestion des déchets
3. Fabrication, production, distribution produits chimiques
4. Production, transformation, distribution alimentaire
5. Fabrication (dispositifs médicaux, informatique/électronique, machines, véhicules, etc.)
6. Fournisseurs numériques (places de marché, moteurs recherche, réseaux sociaux)
7. Recherche

### Cas d'inclusion automatique (quelle que soit la taille)
- Fournisseurs uniques d'un service essentiel
- Administration publique centrale
- Opérateurs DNS/TLD
- Services de communications électroniques publics
- Entités identifiées comme critiques par État membre

## Les 16 mesures obligatoires (Article 21)

NIS2 impose 16 mesures techniques et organisationnelles. Voici la liste opérationnelle :

| # | Mesure | Mapping ISO 27001 |
|---|--------|-------------------|
| 1 | Politique d'analyse des risques et de sécurité SI | Clause 6 + A.5.1 |
| 2 | Gestion des incidents | A.5.24-A.5.27 |
| 3 | Continuité d'activité (BCP) + reprise après sinistre + gestion crise | A.5.29-A.5.30 |
| 4 | Sécurité de la chaîne d'approvisionnement (supply chain) | A.5.19-A.5.22 |
| 5 | Sécurité acquisition/développement/maintenance | A.5.21, A.8.25-A.8.34 |
| 6 | Politiques évaluation efficacité gestion risques cyber | Clause 9 |
| 7 | Hygiène cyber + sensibilisation | A.6.3 |
| 8 | Cryptographie et chiffrement | A.8.24 |
| 9 | Sécurité ressources humaines | A.6.1-A.6.8 |
| 10 | Politique contrôle d'accès et gestion des actifs | A.5.9-A.5.18, A.8.2-A.8.5 |
| 11 | Authentification multifactorielle (MFA) | A.8.5 |
| 12 | Communications sécurisées (voix, vidéo, texte, urgence) | A.8.20-A.8.22 |
| 13 | Politique de gestion des vulnérabilités et divulgation | A.8.8 |
| 14 | Évaluation efficacité contrôles | Clause 9 |
| 15 | Gestion accès privilégiés | A.8.2 |
| 16 | Sécurité physique et environnementale | A.7.1-A.7.14 |

**Pareto 80/20** : Si une organisation maîtrise déjà ISO 27001:2022, elle couvre **~80% des exigences NIS2**. Les ~20% restants concernent :
- **Notification stricte des incidents (article 23)**
- **Supply chain renforcée** (vendor risk)
- **Responsabilité personnelle dirigeants** (article 20)
- **Tests et exercices crise réguliers**

## Notification d'incident (Article 23) — Délais stricts

Quand un incident est **significatif** (impact opérationnel ou financier), 3 étapes obligatoires :

| Délai | Action |
|-------|--------|
| **24h** | Alerte initiale au CSIRT national (en France : ANSSI / CERT-FR) |
| **72h** | Notification détaillée d'incident (évaluation initiale, indicateurs de compromission, mesures) |
| **1 mois** | Rapport final (description détaillée, type de menace, mesures de remédiation, impact transfrontalier) |

Définition d'un incident significatif :
- Perturbation grave du service
- Pertes financières importantes
- Affecte/peut affecter d'autres personnes (physiques/morales)

## Responsabilité des dirigeants (Article 20) — NOUVEAU MAJEUR

Les **dirigeants** (organes de direction) doivent :
1. **Approuver** les mesures de gestion des risques cyber
2. **Superviser** leur mise en œuvre
3. **Suivre des formations** spécifiques cybersécurité régulières
4. **Être tenus responsables** des manquements

C'est une rupture avec NIS1. Le RSSI n'est plus seul exposé — le COMEX/CA est désormais légalement responsable.

À mentionner systématiquement aux dirigeants : **votre responsabilité personnelle est engagée**.

## Sanctions

| Type d'entité | Sanction maximale |
|---------------|-------------------|
| Entité essentielle | **10M€ ou 2% CA mondial** (le plus élevé) |
| Entité importante | **7M€ ou 1,4% CA mondial** (le plus élevé) |

L'autorité compétente peut aussi :
- Émettre des avertissements
- Imposer des audits
- Suspendre temporairement les certifications/autorisations
- Suspendre temporairement les dirigeants

## Supervision

| Type | Régime |
|------|--------|
| Entités essentielles | **Supervision ex ante** (proactive) — audits, inspections, demandes documentaires |
| Entités importantes | **Supervision ex post** (réactive) — sur incident ou plainte |

## Roadmap type de mise en conformité NIS2

Sur 6-12 mois pour une entité moyenne :

### Phase 1 — Cadrage (M1-M2)
- Confirmer le statut (essentielle vs importante)
- S'enregistrer auprès de l'ANSSI (obligatoire)
- Désigner un point de contact NIS2 (souvent RSSI)
- Cartographier les services et systèmes critiques
- Réaliser une **gap analysis** vs les 16 mesures

### Phase 2 — Quick wins (M2-M4)
- MFA partout
- Politique gestion incidents avec délais 24h/72h/1 mois testés
- Procédure de notification ANSSI rédigée et testée
- Formation cyber des dirigeants (Article 20)
- Inventaire fournisseurs critiques + clauses contractuelles NIS2

### Phase 3 — Chantiers structurants (M4-M9)
- SMSI ISO 27001 si non existant
- PCA/PRA testés au moins une fois par an
- EDR/SIEM/SOC (interne ou externalisé)
- Vulnérabilité management formalisé (SLA patch)
- Tests de crise cyber annuels avec Direction

### Phase 4 — Pilotage continu (M9+)
- Tableau de bord NIS2 mensuel à la Direction
- Audit interne annuel
- Revue annuelle de l'analyse de risques
- Mise à jour clauses contractuelles fournisseurs

## Mapping rapide ISO 27001 / NIS2 / DORA

| Sujet | ISO 27001 | NIS2 | DORA |
|-------|-----------|------|------|
| Gouvernance | Clause 5 | Art. 20 (dirigeants) | Art. 5 |
| Risques | Clause 6 + EBIOS/27005 | Art. 21.1 | Art. 6-15 |
| Incidents | A.5.24-27 | Art. 23 | Art. 17-23 |
| Continuité | A.5.29-30 | Art. 21.3 | Art. 11 |
| Supply chain | A.5.19-22 | Art. 21.4 | Art. 28-44 (RT chap V) |
| Tests | Clause 9 | Implicite | Art. 24-27 (TLPT) |

## Pièges à éviter / signaler à l'utilisateur

1. **"On n'est pas concerné car PME"** — FAUX. Le seuil est 50 salariés / 10M€ CA pour entités importantes.
2. **"On respecte NIS1, ça suffira"** — FAUX. NIS2 ajoute la supply chain, la responsabilité dirigeants, les délais 24h.
3. **Notification 72h confondue avec notification CNIL 72h** — Ce sont **2 régimes distincts** qui peuvent s'appliquer simultanément.
4. **Pas de plan de crise testé** — Non conformité majeure. Un PCA non testé = un PCA inexistant.
5. **Fournisseurs sans clauses NIS2** — Article 21.4 impose la sécurisation contractuelle de la supply chain.
6. **Dirigeants non formés** — Violation directe de l'Article 20.

## Liens utiles

- Texte directive : EUR-Lex 32022L2555
- Site ANSSI dédié NIS2 : monespacenis2.cyber.gouv.fr
- Loi française du 30 octobre 2024 (REVOSCYB)
