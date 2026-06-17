# Plan de Continuité d'Activité (PCA) et Plan de Reprise d'Activité (PRA)

**Référentiels** : ISO 22301, ISO 27001 A.5.29, A.5.30, A.8.14, NIS2 art. 21.2.c, DORA art. 11
**Document** : PCA/PRA
**Version** : 1.0
**Date** : [JJ/MM/AAAA]
**Owner** : Direction Générale (sponsor) / RSSI (opérationnel)

---

## 1. Pourquoi un PCA/PRA

Garantir la **continuité des activités critiques** en cas de sinistre majeur :
- crise cyber (ransomware, fuite massive),
- indisponibilité d'un site, d'un datacenter, d'un fournisseur,
- catastrophe (incendie, inondation, pandémie),
- crise sociale ou géopolitique.

**Distinction** :
- **PCA** = maintenir l'activité **pendant** la crise (mode dégradé, sites de secours, télétravail massif).
- **PRA** = **reprendre** les systèmes informatiques après sinistre (restauration, bascule sur site de secours).

**Exigence réglementaire** :
- NIS2 art. 21.2.c : gestion de la continuité et reprise après sinistre.
- DORA art. 11 : politique et plans de continuité TIC + tests réguliers.
- RGPD art. 32.1.c : restauration en cas d'incident.

---

## 2. Périmètre

### 2.1 Activités couvertes

| Activité | Criticité (1-4) | Justification |
|---|---|---|
| Production / livraison clients | 4 | CA direct |
| Service client / SAV | 3 | Satisfaction, contrats SLA |
| Facturation / encaissements | 4 | Trésorerie |
| Paie | 2 | Mensuelle, tolérance 5j |
| Communication externe | 2 | Image |
| Support IT interne | 3 | Productivité globale |

### 2.2 Exclusions

Activités non couvertes par ce PCA et leur justification (à compléter).

---

## 3. Bilan d'Impact sur l'Activité (BIA)

### 3.1 Méthode

Pour chaque processus critique, identifier :
- **RTO** (Recovery Time Objective) = durée maximale d'interruption acceptable
- **RPO** (Recovery Point Objective) = quantité maximale de données perdues acceptable
- **MTPD** (Maximum Tolerable Period of Disruption) = durée au-delà de laquelle l'activité ne peut plus reprendre

### 3.2 Tableau BIA

| Processus | RTO | RPO | MTPD | Impact financier 24h | Impact financier 1 semaine | Dépendances clés |
|---|---|---|---|---|---|---|
| Site e-commerce | 4h | 15 min | 48h | 50 k€ | 800 k€ | Hébergement, CDN, paiement |
| ERP comptabilité | 24h | 4h | 5 jours | 10 k€ | 250 k€ | Datacenter principal, base SQL |
| Messagerie | 8h | 1h | 3 jours | 5 k€ | 100 k€ | M365, AD |
| Production usine | 2h | 0 | 24h | 200 k€ | 3 M€ | SCADA, automates, ERP MES |
| Service client | 4h | 30 min | 48h | 15 k€ | 200 k€ | CRM, téléphonie, knowledge base |

### 3.3 Cartographie des ressources critiques

| Ressource | Type | Site | Criticité | Redondance |
|---|---|---|---|---|
| Datacenter Paris | Infrastructure | Paris | 4 | DC secondaire Lille |
| Salesforce | SaaS | UE | 4 | DR région secondaire |
| Connexion Internet | Réseau | Tous sites | 4 | 2 opérateurs SLA 99.9 |
| Personnel cyber (RSSI + 2) | Humain | Paris | 3 | Astreinte 24/7 |
| Fournisseur Y (composant unique) | Supply chain | Allemagne | 4 | Pas de redondance - risque |

---

## 4. Stratégie de continuité

### 4.1 Sites de repli

| Site principal | Site de repli | Type | Capacité | Délai bascule |
|---|---|---|---|---|
| Siège Paris | Bureau Lille | Chaud | 30 postes / 100 | < 4h |
| Datacenter Paris | Datacenter Lille | Tiède | 100% prod critique | < 2h (RTO infra) |
| Cloud principal eu-west-3 | eu-west-1 | DR Multi-Région | 80% capacité | < 4h |

**Niveaux** :
- **Chaud** : équipements opérationnels, données répliquées en quasi temps réel
- **Tiède** : équipements présents, restauration depuis sauvegarde nécessaire
- **Froid** : locaux et alimentation, équipements à déployer

### 4.2 Modes dégradés

| Activité | Mode normal | Mode dégradé | Limites |
|---|---|---|---|
| Prise de commande | Site e-commerce | Téléphone + tableur | 100 commandes/jour vs 5 000 |
| Facturation | ERP automatique | Saisie manuelle Excel | Délai +5j sur clôture |
| Communication interne | Teams | WhatsApp Business + SMS | Pas de partage docs sensibles |
| Production | Pleine cadence | 50% capacité | Stocks tampon 1 semaine |

### 4.3 Sauvegardes

**Règle 3-2-1-1-0** :
- **3** copies des données,
- **2** supports différents,
- **1** copie hors site,
- **1** copie immuable / déconnectée (anti-ransomware),
- **0** erreur lors du dernier test de restauration.

| Donnée | Fréquence | Type | Site | Rétention | Chiffrement | Test restauration |
|---|---|---|---|---|---|---|
| Bases SQL prod | Continue (CDC) + snapshot 4h | Disque + bande | DC + Cloud + offline | 90 jours + 7 ans archives | AES-256 | Trimestriel |
| Fichiers métier | Quotidien | Disque + Cloud | DC + Cloud | 30 jours | AES-256 | Trimestriel |
| Postes de travail | Hebdomadaire | Cloud | OneDrive | 90 jours | AES-256 | Annuel |
| Configurations IaC | À chaque commit | Git | GitLab + miroir | Permanent | AES-256 | Mensuel |

---

## 5. Organisation de crise

### 5.1 Cellule de crise

| Rôle | Titulaire | Suppléant | Contact 24/7 |
|---|---|---|---|
| Directeur de crise | DG | DAF | +33 ... |
| Coordinateur opérationnel | RSSI | DSI | +33 ... |
| Communication | Dircom | RH | +33 ... |
| Juridique / réglementaire | DPO + Juriste | Cabinet externe | +33 ... |
| Technique | Lead Ops | Architecte | +33 ... |
| Métier | Directeurs BU | Adjoints | +33 ... |
| Support externe | CERT-FR + Assureur cyber | Avocat cyber | 0800 ... |

### 5.2 Procédure d'activation

1. **Détection** : alerte SOC, SIEM, signalement, panne...
2. **Qualification** (sous 30 min) : par le RSSI ou astreinte → activation ou non du PCA ?
3. **Activation niveau 1** (incident significatif) : cellule cyber + métier impacté
4. **Activation niveau 2** (crise majeure) : cellule de crise complète + Direction
5. **Communication** : interne (Teams, SMS), externe (clients, autorités, presse)
6. **Pilotage** : war room physique ou virtuelle, point toutes les 2h
7. **Sortie de crise** : retour nominal, RETEX, mise à jour PCA

### 5.3 Notifications réglementaires

| Référentiel | Délai | Destinataire | Déclenchement |
|---|---|---|---|
| RGPD (violation données) | 72h | CNIL + personnes si risque élevé | Confidentialité personnelle compromise |
| NIS2 (incident significatif) | 24h alerte précoce / 72h notification / 1 mois rapport final | ANSSI + autorité sectorielle | Indisponibilité service essentiel |
| DORA (incident TIC majeur) | 4h / 72h / 1 mois | Autorité financière | Selon classification critère |
| LPM (OIV) | Immédiat | ANSSI | Incident sécurité SI critique |
| Plainte pénale | Sans délai | Procureur / police | Cybercriminalité |

---

## 6. Tests et exercices

### 6.1 Programme annuel

| Type de test | Fréquence | Périmètre | Responsable |
|---|---|---|---|
| Test de restauration de sauvegarde | Trimestriel | Échantillon de données critiques | Ops |
| Bascule applicative DR | Semestriel | 1 application critique | DSI + RSSI |
| Exercice sur table (tabletop) | Annuel | Scénario crise complet | Direction + RSSI |
| Exercice simulation (red team) | Annuel ou bi-annuel | Cyberattaque réelle | RSSI + prestataire |
| Test PCA complet (bascule réelle) | Annuel | Tout le périmètre | Direction |
| **TLPT (DORA)** si applicable | Tous les 3 ans | Systèmes financiers critiques | TLPT manager certifié |

### 6.2 Critères de réussite

- RTO et RPO réels mesurés ≤ objectifs
- Aucun blocage majeur dans l'enchaînement des étapes
- Cellule de crise réactive (< 30 min activation)
- Communication interne et externe maîtrisée
- RETEX produit dans les 15 jours
- Plan d'action de correction des écarts

---

## 7. Documentation et maintenance

### 7.1 Documents associés

- Politique de continuité (Direction)
- Procédures techniques de restauration (DSI)
- Annuaire de crise (mis à jour mensuellement)
- Contrats fournisseurs critiques (clauses continuité)
- Conventions sites de repli
- Polices d'assurance cyber

### 7.2 Revue

- **Annuelle minimum** par le RSSI + Direction.
- **À chaque changement majeur** : nouveau site, nouvelle application critique, M&A, nouveau prestataire critique.
- **Après chaque crise réelle** : RETEX intégré dans la version suivante.

---

## 8. Indicateurs de pilotage

| KPI | Cible | Fréquence | Source |
|---|---|---|---|
| % processus critiques avec BIA à jour | 100% | Annuel | Cartographie |
| % activités testées dans l'année | 100% | Annuel | Plan de tests |
| Taux de réussite tests de restauration | > 95% | Trimestriel | Rapports Ops |
| Délai moyen d'activation cellule de crise | < 30 min | Par exercice | Logs |
| Couverture sauvegardes (vs périmètre) | 100% | Mensuel | Outil backup |
| % personnel cellule de crise formé | 100% | Annuel | RH/RSSI |
| Tests fournisseurs critiques sur la continuité | 100% par an | Annuel | Achats |

---

## 9. Budget

| Poste | CAPEX | OPEX annuel |
|---|---|---|
| Site de repli (loyer + équipements) | 50 k€ | 30 k€ |
| Réplication DR Cloud | 0 | 80 k€ |
| Solution sauvegarde immuable | 40 k€ | 15 k€ |
| Astreinte 24/7 + formation | 0 | 60 k€ |
| Tests et exercices (prestataires) | 0 | 25 k€ |
| Assurance cyber | 0 | 40 k€ |
| **Total** | **90 k€** | **250 k€** |

---

## Annexes

- Annexe A : Annuaire de crise détaillé (confidentiel, accès restreint)
- Annexe B : Procédures techniques de restauration par application
- Annexe C : Scripts d'automatisation bascule DR
- Annexe D : Templates communication clients / médias / autorités
- Annexe E : Contrats fournisseurs critiques (clauses continuité, SLA, audit)
- Annexe F : Rapports des derniers tests et RETEX
