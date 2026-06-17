# DORA — Digital Operational Resilience Act — Référence opérationnelle

## Pourquoi DORA

Règlement **(UE) 2022/2554**, applicable depuis le **17 janvier 2025**. Vise la **résilience opérationnelle numérique** du secteur financier européen.

**Caractéristique** : c'est un **règlement**, pas une directive — donc directement applicable, sans transposition nationale.

## Qui est concerné ?

~22 000 entités financières dans l'UE :
- Banques (établissements de crédit)
- Entreprises d'investissement
- Établissements de paiement et de monnaie électronique
- Assurances et réassurances
- Sociétés de gestion (OPCVM, FIA)
- Marchés organisés (bourses)
- Dépositaires centraux et contreparties centrales
- Prestataires de services sur crypto-actifs (MiCA)
- Plus : **prestataires TIC critiques** désignés par les ESA

Proportionnalité : la rigueur d'application varie selon la taille et la criticité (cf. art. 4).

## Les 5 piliers DORA

```
1. Gouvernance & gestion des risques TIC
2. Gestion des incidents TIC
3. Tests de résilience opérationnelle numérique
4. Gestion des risques fournisseurs TIC tiers
5. Partage d'informations sur les cybermenaces
```

### Pilier 1 — Gouvernance & gestion des risques TIC (Art. 5-15)

**Organe de direction** = ultime responsable du cadre de gestion des risques TIC.

Exigences principales :
- Cadre de gestion des risques TIC documenté, approuvé annuellement
- Politique de sécurité de l'information
- Inventaire des actifs TIC à jour
- Classification fonctions et actifs par criticité
- Identification, protection, détection, réponse et restauration (mapping NIST CSF direct)
- Politiques RH, accès, gestion changements, sauvegarde, chiffrement

### Pilier 2 — Gestion des incidents TIC (Art. 17-23)

#### Classification

Un incident TIC doit être classifié selon **7 critères** (art. 18) :
1. Nombre clients/contreparties affectés
2. Réputation
3. Durée
4. Étendue géographique
5. Pertes de données
6. Criticité des services affectés
7. Impact économique

#### Notification (art. 19)

| Délai max | Type de rapport |
|-----------|-----------------|
| **4h** après classification | **Notification initiale** à l'autorité compétente |
| **72h** | **Rapport intermédiaire** |
| **1 mois** | **Rapport final** |

**Plus strict que NIS2** (qui est à 24h/72h/1 mois). Si une entité est soumise aux deux, c'est le délai DORA qui prime pour les TIC.

### Pilier 3 — Tests de résilience (Art. 24-27)

Tous les acteurs doivent réaliser **annuellement** :
- Tests de vulnérabilité
- Open source scans
- Tests réseau
- Analyse de gaps
- Tests de performance
- Tests de scénarios
- Tests de compatibilité
- Tests de pénétration

#### Tests TLPT — Threat-Led Penetration Tests (Art. 26-27)

Pour les entités **significatives**, obligation tous les **3 ans** d'un **TLPT** (basé sur TIBER-EU) :
- Test d'intrusion piloté par la menace (red team)
- Scénarios construits à partir de threat intelligence
- Durée : 12 semaines minimum
- Supervisé par autorité compétente
- Couvre les fonctions critiques en production

Le TLPT est l'exigence la plus lourde de DORA. Budget typique : 200k-500k€ par campagne.

### Pilier 4 — Risques fournisseurs TIC tiers (Art. 28-44)

C'est **le pilier le plus disruptif** pour les acteurs financiers.

#### Registre d'information (Art. 28.3) — OBLIGATOIRE

Format standardisé européen (RTS ESA) à fournir annuellement à l'autorité. Contient :
- Tous les prestataires TIC
- Type de service fourni
- Localisation traitement et stockage des données
- Fonction critique ou importante supportée
- Évaluation de risques
- Conditions contractuelles

#### Clauses contractuelles obligatoires (Art. 30)

Tout contrat TIC doit comporter :
- Description précise des services
- Lieu de prestation
- Niveau de service et SLA
- Droit d'audit
- Coopération en cas d'incident
- Stratégie de sortie / portabilité
- Sécurité des données et chiffrement
- Notification incidents
- Pour fonctions critiques : exigences renforcées (rétention preuves, tests d'incident, etc.)

#### Stratégie de sortie

Toujours documentée pour les prestataires de fonctions critiques. Doit inclure :
- Plan de transition
- Délai de réversibilité
- Tests de réversibilité

#### Prestataires TIC critiques (CTPP)

Les ESA désignent des prestataires comme "critiques" (typiquement les hyperscalers, certains SaaS très répandus). Ils deviennent **directement supervisés par les ESA**.

### Pilier 5 — Partage d'informations (Art. 45)

Les entités peuvent (encouragées) échanger entre elles sur les menaces, via accords formalisés. Pas obligatoire mais incité.

## Documents et livrables minimum DORA

| Document | Obligation | Fréquence |
|----------|------------|-----------|
| Cadre de gestion des risques TIC | Art. 6 | Revue annuelle |
| Politique sécurité information | Art. 9 | Revue annuelle |
| Inventaire actifs TIC | Art. 8 | Continu |
| Plan de continuité TIC | Art. 11 | Revue annuelle + test |
| Plan de réponse aux incidents | Art. 17 | Revue annuelle |
| Politique gestion risques tiers TIC | Art. 28 | Revue annuelle |
| Registre d'information fournisseurs TIC | Art. 28.3 | Annuel (déclaré) |
| Programme de tests de résilience | Art. 24 | Annuel |
| Stratégie de sortie par prestataire critique | Art. 28 | Continu |
| Rapport notification incident | Art. 19 | Par incident |

## Sanctions

Variables par État membre. France : ACPR et AMF peuvent infliger :
- Avertissements publics
- Amendes (montant calculé en fonction du CA, jusqu'à plusieurs millions €)
- Suspension d'agrément (sanction ultime)

Les **dirigeants** peuvent être sanctionnés personnellement.

## Mapping DORA / ISO 27001 / NIS2

| Sujet | DORA | ISO 27001 | NIS2 |
|-------|------|-----------|------|
| Gouvernance | Art. 5 | Clause 5 | Art. 20 |
| Risques TIC | Art. 6-15 | Clause 6 + Annexe A | Art. 21.1 |
| Incidents | Art. 17-23 (4h/72h/1m) | A.5.24-27 | Art. 23 (24h/72h/1m) |
| Tests résilience | Art. 24-27 (TLPT) | Pas explicite | Pas explicite |
| Supply chain | Art. 28-44 (très détaillé) | A.5.19-22 | Art. 21.4 |
| Continuité | Art. 11 | A.5.29-30 | Art. 21.3 |

**Point clé** : DORA est **le cadre le plus exigeant** sur la supply chain TIC et les tests. Si une entité est soumise à DORA + NIS2 + ISO 27001, le pilote opérationnel doit être DORA.

## Priorisation pour entité financière

Si l'utilisateur démarre la mise en conformité DORA :

### Quick wins (3 mois)
1. Compléter l'inventaire actifs TIC
2. Cartographier les prestataires TIC critiques
3. Établir le registre d'information (format ESA)
4. Tester un scénario d'incident avec délai 4h

### Chantiers structurants (6-12 mois)
1. Renégocier les contrats prestataires critiques (clauses art. 30)
2. Mettre en place un programme de tests annuel
3. Préparer le premier TLPT (si entité significative)
4. Stratégies de sortie pour chaque prestataire critique

### Maintien (continu)
- Notification incidents formalisée
- Revue annuelle cadre risques TIC
- Mise à jour du registre d'information

## Pièges à éviter

1. **Sous-estimer le registre fournisseurs** : c'est un travail de plusieurs centaines d'heures sur un SI complexe.
2. **Croire que SOC 2 ou ISO suffisent** : DORA exige des clauses contractuelles spécifiques que ces référentiels n'apportent pas.
3. **Repousser le TLPT** : 3 ans semble loin, mais la prépa prend 6 mois.
4. **Confondre incident TIC et incident métier** : DORA cible spécifiquement les incidents TIC.
5. **Pas de stratégie de sortie** : risque de blocage en cas de défaillance d'un hyperscaler ou SaaS critique.

## Liens utiles

- Règlement DORA : EUR-Lex 32022R2554
- Standards techniques (RTS/ITS) publiés par les ESA : eba.europa.eu, eiopa.europa.eu, esma.europa.eu
- France : ACPR (banques/assurances), AMF (marchés)
