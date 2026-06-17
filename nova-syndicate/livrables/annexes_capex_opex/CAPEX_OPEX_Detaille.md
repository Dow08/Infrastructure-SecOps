# ÉTUDE BUDGÉTAIRE CAPEX / OPEX DÉTAILLÉE
## Comparatif Solution Propriétaire vs. Solution Open-Source
### Client : Nova Syndicate

---

**Référence document** : NS-2026-ANX-01
**Auteur** : Dorian Poncelet — Responsable Technique
**Date** : Mai 2026
**Version** : 1.0
**Statut** : Annexe budgétaire au Rapport Phase I
**Classification** : Confidentiel – Diffusion restreinte client

---

## 1. PRÉAMBULE

### 1.1 Objet

Cette annexe détaille l'analyse comparative budgétaire entre trois trajectoires technologiques étudiées pour la modernisation de l'infrastructure Nova Syndicate :

- **Solution A** — Stack propriétaire (Microsoft, Cisco, Splunk, Veeam, etc.)
- **Solution B** — Stack open-source production-grade *(retenue)*
- **Solution C** — Hébergement cloud public (AWS / Azure)

L'objectif est de fournir une **base chiffrée** pour la décision d'investissement et de justifier le choix de la Solution B au regard du **TCO sur 3 ans**.

### 1.2 Méthodologie

- **CAPEX** (*Capital Expenditure*) : dépenses d'investissement initiales — matériel, licences perpétuelles, frais d'installation.
- **OPEX** (*Operational Expenditure*) : dépenses récurrentes — licences annuelles, support, maintenance, temps homme.
- **TCO** (*Total Cost of Ownership*) : somme CAPEX + OPEX cumulés sur la période d'analyse (3 ans).

Les chiffres sont **indicatifs** et basés sur :
- Tarifs publics éditeurs 2025-2026 (Splunk, Microsoft, Fortinet, etc.).
- Tarifs cloud public (AWS, Azure) 2025.
- Études marché (Gartner, IDC, ENISA).
- Coût ETP français 2025 (~4 500 € chargé mensuel).

Les chiffres définitifs nécessiteront une **consultation commerciale** auprès des éditeurs pour devis personnalisés.

### 1.3 Périmètre fonctionnel chiffré

Périmètre identique pour les 3 solutions :
- Hyperviseur ou équivalent compute
- Firewall périmétrique (Lyon + Marseille) + IDS
- Active Directory (85 utilisateurs)
- Base de données métier
- Serveur de fichiers (stockage cloud privé)
- Serveur web public
- Serveur de messagerie
- VPN site-to-site + VPN remote (20 commerciaux)
- SIEM + EDR
- Sauvegarde
- Supervision

---

## 2. SOLUTION A — STACK PROPRIÉTAIRE

### 2.1 Composants détaillés

#### 2.1.1 Virtualisation
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| VMware vSphere Standard | 1 000 € / CPU socket | 4 sockets | 4 000 € | 800 € (support Basic) |
| vCenter Server Standard | 6 000 € / instance | 1 | 6 000 € | 1 200 € (support) |
| **Sous-total virtualisation** | | | **10 000 €** | **2 000 €/an** |

*Source : VMware tarifs publics 2024 (post-acquisition Broadcom). Modèle de licence par socket révisé en 2024.*

#### 2.1.2 Firewall + IPS
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| Fortinet FortiGate 100F (hardware) | 4 500 € | 2 (Lyon + Marseille) | 9 000 € | — |
| FortiCare 8x5 Standard | 600 €/an | 2 | — | 1 200 € |
| FortiGuard UTM Bundle (IPS, AV, AppCtl, Web filter) | 1 200 €/an | 2 | — | 2 400 € |
| **Sous-total firewall** | | | **9 000 €** | **3 600 €/an** |

*Source : Fortinet distributeur 2025.*

#### 2.1.3 Active Directory
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| Windows Server 2022 Standard | 800 € | 2 (1 DC Lyon + 1 RODC Marseille) | 1 600 € | — |
| CAL Utilisateur Windows Server | 35 € | 85 | 2 975 € | — |
| Software Assurance (mises à jour) | 20 % du prix licence/an | — | — | 915 € |
| **Sous-total AD** | | | **4 575 €** | **915 €/an** |

*Source : Microsoft Volume Licensing 2025 (Open Value).*

#### 2.1.4 SIEM + EDR
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| Splunk Enterprise (10 GB/jour ingestion) | — | 1 instance | — | 18 000 € |
| Microsoft Defender for Endpoint P2 | 5,20 €/poste/mois | 85 | — | 5 304 € |
| **Sous-total SIEM/EDR** | | | **0 €** | **23 304 €/an** |

*Sources : Splunk pricing.docs (2024), Microsoft 365 pricing.*

> Note : Splunk Cloud peut s'avérer encore plus cher pour les volumes croissants. Volume cible Nova Syndicate estimé à 5-10 GB/jour.

#### 2.1.5 Backup et stockage
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| Veeam Backup & Replication Essentials | 1 500 € | 1 | 1 500 € | — |
| Support Veeam Premier | 400 €/an | 1 | — | 400 € |
| Stockage NAS Synology RS1221+ (8 To) | 1 800 € | 1 | 1 800 € | — |
| **Sous-total backup** | | | **3 300 €** | **400 €/an** |

#### 2.1.6 Messagerie
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| Microsoft 365 Business Standard | 10,50 €/utilisateur/mois | 85 | — | 10 710 € |
| **Sous-total messagerie** | | | **0 €** | **10 710 €/an** |

*Source : Microsoft 365 pricing France 2025.*

#### 2.1.7 VPN remote (commerciaux)
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| Cisco AnyConnect Plus (licence) | 70 €/user/an | 20 | — | 1 400 € |
| **Sous-total VPN** | | | **0 €** | **1 400 €/an** |

*Source : Cisco SMARTnet 2024.*

#### 2.1.8 Supervision infra
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| PRTG 1000 sensors | 1 800 € | 1 | 1 800 € | — |
| Maintenance PRTG | 20 % CAPEX/an | — | — | 360 € |
| **Sous-total supervision** | | | **1 800 €** | **360 €/an** |

#### 2.1.9 Hardware d'hébergement
| Composant | Tarif unitaire | Quantité | CAPEX | OPEX annuel |
|-----------|----------------|----------|-------|-------------|
| Serveur Dell PowerEdge R650 (2x Xeon, 64 GB RAM, 4 To) | 6 500 € | 1 | 6 500 € | — |
| Onduleur APC Smart-UPS 3000VA | 1 000 € | 1 | 1 000 € | — |
| Switch Cisco Catalyst 1300-24P | 800 € | 1 | 800 € | — |
| **Sous-total hardware** | | | **8 300 €** | **0 €** |

#### 2.1.10 Temps homme déploiement
| Poste | Tarif | Charge | CAPEX |
|-------|-------|--------|-------|
| Architecte / Consultant senior | 800 €/jour | 4 jours | 3 200 € |
| Ingénieur déploiement | 600 €/jour | 8 jours | 4 800 € |
| **Sous-total temps homme** | | | **8 000 €** |

### 2.2 Récapitulatif Solution A

| Poste | CAPEX | OPEX/an | OPEX 3 ans |
|-------|-------|---------|------------|
| Virtualisation | 10 000 € | 2 000 € | 6 000 € |
| Firewall | 9 000 € | 3 600 € | 10 800 € |
| Active Directory | 4 575 € | 915 € | 2 745 € |
| SIEM/EDR | 0 € | 23 304 € | 69 912 € |
| Backup | 3 300 € | 400 € | 1 200 € |
| Messagerie | 0 € | 10 710 € | 32 130 € |
| VPN remote | 0 € | 1 400 € | 4 200 € |
| Supervision | 1 800 € | 360 € | 1 080 € |
| Hardware | 8 300 € | 0 € | 0 € |
| Temps homme | 8 000 € | 0 € | 0 € |
| **TOTAL** | **44 975 €** | **42 689 €** | **128 067 €** |

> **TCO 3 ans Solution A : ~ 173 042 €**

---

## 3. SOLUTION B — STACK OPEN-SOURCE *(RETENUE)*

### 3.1 Composants détaillés

#### 3.1.1 Virtualisation
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| Proxmox VE 9 (Community) | 0 € | 0 € | 0 € |
| Proxmox VE Subscription Basic (optionnel) | 510 €/an/socket | — | 0 € (community choisi) |
| **Sous-total** | | **0 €** | **0 €/an** |

#### 3.1.2 Firewall + IDS
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| OPNsense 26.x (community) | 0 € | 0 € | 0 € |
| OPNsense Business Edition (optionnel) | 12,50 €/mois × 2 | — | 0 € (community choisi) |
| Suricata IDS (intégré OPNsense) | 0 € | 0 € | 0 € |
| Emerging Threats Open ruleset | 0 € | 0 € | 0 € |
| **Sous-total** | | **0 €** | **0 €/an** |

#### 3.1.3 Active Directory
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| Samba 4 (debian package) | 0 € | 0 € | 0 € |
| **Sous-total** | | **0 €** | **0 €/an** |

#### 3.1.4 SIEM + EDR
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| Wazuh 4.x (Manager + Indexer + Dashboard) | 0 € | 0 € | 0 € |
| Wazuh Cloud (optionnel managed) | — | — | 0 € (self-hosted) |
| **Sous-total** | | **0 €** | **0 €/an** |

#### 3.1.5 Backup et stockage
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| rsync + scripts maison | 0 € | 0 € | 0 € |
| GPG (chiffrement archives) | 0 € | 0 € | 0 € |
| Stockage NAS Synology RS1221+ (mêmes besoins) | 1 800 € | 1 800 € | 0 € |
| Cloud Storage OVH (100 GB hors site) | 5 €/mois | — | 60 €/an |
| **Sous-total** | | **1 800 €** | **60 €/an** |

#### 3.1.6 Messagerie
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| Postfix + Dovecot + Roundcube | 0 € | 0 € | 0 € |
| Certificat Let's Encrypt | 0 € | 0 € | 0 € |
| **Sous-total** | | **0 €** | **0 €/an** |

#### 3.1.7 VPN remote
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| OpenVPN (intégré OPNsense) | 0 € | 0 € | 0 € |
| **Sous-total** | | **0 €** | **0 €/an** |

#### 3.1.8 Supervision (inclus dans Wazuh)
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| Wazuh metrics + custom dashboards | 0 € | 0 € | 0 € |
| **Sous-total** | | **0 €** | **0 €/an** |

#### 3.1.9 Hardware
| Composant | Tarif | CAPEX | OPEX annuel |
|-----------|-------|-------|-------------|
| Serveur Dell PowerEdge R650 (mêmes specs) | 6 500 € | 6 500 € | 0 € |
| Onduleur APC | 1 000 € | 1 000 € | 0 € |
| Switch Netgear GS324T (administrable, moins cher que Cisco) | 250 € | 250 € | 0 € |
| **Sous-total** | | **7 750 €** | **0 €** |

#### 3.1.10 Temps homme déploiement
| Poste | Tarif | Charge | CAPEX |
|-------|-------|--------|-------|
| Architecte / Consultant (mission complète) | 800 €/jour | 4 jours | 3 200 € |
| Ingénieur (formation interne + ajustements) | 600 €/jour | 4 jours | 2 400 € |
| **Sous-total** | | | **5 600 €** |

> Note : temps homme inférieur grâce à l'industrialisation IaC (Terraform + Cloud-Init). Le déploiement est largement automatisé.

### 3.2 Récapitulatif Solution B

| Poste | CAPEX | OPEX/an | OPEX 3 ans |
|-------|-------|---------|------------|
| Virtualisation | 0 € | 0 € | 0 € |
| Firewall + IDS | 0 € | 0 € | 0 € |
| Active Directory | 0 € | 0 € | 0 € |
| SIEM/EDR | 0 € | 0 € | 0 € |
| Backup | 1 800 € | 60 € | 180 € |
| Messagerie | 0 € | 0 € | 0 € |
| VPN remote | 0 € | 0 € | 0 € |
| Supervision | 0 € | 0 € | 0 € |
| Hardware | 7 750 € | 0 € | 0 € |
| Temps homme déploiement | 5 600 € | 0 € | 0 € |
| Temps homme exploitation interne (½ ETP) | — | 27 000 € | 81 000 € |
| **TOTAL** | **15 150 €** | **27 060 €** | **81 180 €** |

> **TCO 3 ans Solution B : ~ 96 330 €**

#### Note importante sur l'exploitation interne

Le temps homme d'exploitation est conservé identique entre Solution A et Solution B dans les deux cas. La Solution A ne supprime pas le besoin d'administration interne — elle réduit uniquement la complexité de certains aspects (interfaces graphiques familières). Inversement, la Solution B exige un effort initial de formation mais offre une **maîtrise totale** de la stack à terme.

Pour une comparaison équitable, le temps homme d'exploitation a été retiré du TCO ci-dessous (puisqu'identique dans les deux trajectoires).

---

## 4. SOLUTION C — CLOUD PUBLIC (AWS / Azure)

### 4.1 Estimation rapide

| Composant | Tarif mensuel | CAPEX | OPEX annuel |
|-----------|---------------|-------|-------------|
| EC2 t3.large × 10 instances | 800 € | 0 € | 9 600 € |
| EFS / EBS 500 GB | 100 € | 0 € | 1 200 € |
| AWS WAF + Shield Standard | 50 € | 0 € | 600 € |
| Cognito (auth) ou AD managed | 50 € | 0 € | 600 € |
| GuardDuty (SIEM-light) | 350 € | 0 € | 4 200 € |
| Client VPN | 300 € | 0 € | 3 600 € |
| Data Transfer Out (estimation) | 200 € | 0 € | 2 400 € |
| Backup AWS | 100 € | 0 € | 1 200 € |
| M365 (messagerie) | 893 € | 0 € | 10 710 € |
| Temps homme déploiement cloud | — | 8 000 € | 0 € |
| **TOTAL** | | **8 000 €** | **34 110 €/an** |

> **TCO 3 ans Solution C : ~ 110 330 €**

### 4.2 Points de vigilance Solution C

- **Souveraineté** : hébergement par défaut sur des datacenters US (CLOUD Act).
- **Confidentialité défense** : nécessite AWS GovCloud ou Azure for Government (non disponibles en Europe à coût raisonnable).
- **Lock-in** : difficile de migrer après 2-3 ans (dépendance forte aux services managés).
- **Variabilité OPEX** : la facture peut s'envoler avec la croissance d'usage (data transfer, requêtes API).

---

## 5. SYNTHÈSE COMPARATIVE

### 5.1 Tableau de synthèse TCO

| Critère | Solution A — Propriétaire | Solution B — Open-source ✅ | Solution C — Cloud |
|---------|----------------------------|------------------------------|---------------------|
| **CAPEX** | 44 975 € | **15 150 €** | 8 000 € |
| **OPEX 3 ans** | 128 067 € | **23 580 €** *(hors temps homme expl.)* | 102 330 € |
| **TCO 3 ans hors expl.** | **173 042 €** | **38 730 €** ✅ | **110 330 €** |
| **Écart vs Solution B** | +134 312 € | référence | +71 600 € |
| **Économie %** | -78 % | référence | -65 % |

> **Solution B = -78 % par rapport à A** sur 3 ans.

### 5.2 Visualisation

```
TCO sur 3 ans (en €, hors temps homme exploitation)

Solution A — Propriétaire   ██████████████████████████████████████████  173 042 €
Solution C — Cloud public   ██████████████████████████                  110 330 €
Solution B — Open-source ✅ █████████                                    38 730 €
```

### 5.3 Critères qualitatifs

| Critère | A — Propriétaire | B — Open-source | C — Cloud |
|---------|------------------|-----------------|-----------|
| Conformité au budget client (20 000 € sur 3 ans hors temps) | ❌ Largement dépassé | ✅ Dans le budget | ⚠️ Limite |
| Souveraineté technologique | ⚠️ US-centric | ✅ Stack maîtrisée | ❌ Hébergement US par défaut |
| Conformité défense / classifié | ⚠️ Variable | ✅ Self-hosted | ❌ Hébergement étranger |
| Support 24/7 inclus | ✅ Oui | ⚠️ Communautaire | ✅ Cloud provider |
| Indépendance fournisseur | ❌ Lock-in licences | ✅ Aucun lock-in | ❌ Lock-in cloud |
| Reproductibilité (IaC) | ⚠️ Partielle | ✅ Totale | ✅ Native |
| Courbe d'apprentissage interne | ⚠️ Licences à acquérir | ⚠️ Curve initiale | ⚠️ Compétences cloud |
| Évolutivité | ⚠️ Licences supplémentaires | ✅ Aucun coût marginal | ✅ Élastique |

### 5.4 Recommandation finale

**Solution B retenue** au regard de :
- Économie financière de **78 %** sur 3 ans (~ 134 k€).
- Respect strict du budget plafond client (20 000 €).
- Adéquation aux exigences sectorielles (médical/aéro/défense).
- Reproductibilité totale via Infrastructure-as-Code.
- Maîtrise complète de la stack technologique.

**Tradeoffs assumés** :
- Pas de contrat de support 24/7 vendor.
- Investissement initial en formation interne nécessaire.
- Responsabilité du suivi sécuritaire repose sur l'équipe interne.

**Mitigations** :
- Documentation exhaustive transmise au client.
- Possibilité d'achat de support communautaire (Wazuh CES, OPNsense Business) si besoin futur.
- Formation interne planifiée sur 2 jours.

---

## 6. ANNEXES

### 6.1 Sources tarifaires consultées

- **VMware** : *VMware vSphere Standard pricing 2025* (post-acquisition Broadcom).
- **Microsoft** : *Microsoft Volume Licensing pricing* — Office of Licensing Programs 2025.
- **Splunk** : *Splunk Pricing Calculator* — splunk.com/pricing 2024.
- **Fortinet** : Devis distributeur Watsoft / D2B / Hermitage Solutions 2025.
- **Cisco** : *Cisco SMARTnet pricing* — partenaire local 2025.
- **Veeam** : *Veeam pricing* — partenaire 2025.
- **AWS** : *AWS Pricing Calculator* — aws.amazon.com/calculator 2025.
- **Microsoft 365** : *Microsoft 365 pricing France* — microsoft.com 2025.
- **OVH** : *OVH Cloud pricing* — ovhcloud.com 2025.
- **Salaires** : *Etude de rémunération Hays 2025* — secteur IT.

### 6.2 Hypothèses retenues

- Période d'analyse : 3 ans (mai 2026 - mai 2029).
- Inflation IT : intégrée dans les tarifs publics (~3-5%/an).
- Volumétrie SIEM Splunk : 10 GB/jour ingestion estimée pour Nova Syndicate.
- Effectif stable sur la période (85 collaborateurs).
- Pas de coûts cachés (telecom, climatisation datacenter) — hors périmètre.

### 6.3 Limitations

- Les tarifs Splunk varient fortement selon les négociations commerciales. La fourchette indiquée (18 000-22 000 €/an) est une médiane.
- Les coûts cloud (Solution C) sont des estimations basées sur des charges constantes ; en réalité, ils varient selon l'usage réel.
- Le coût ETP utilisé (4 500 € chargé mensuel) est une moyenne France 2025 pour un profil IT senior junior.

---

**Document arrêté à la version 1.0** — Mai 2026

*Cette annexe complète le Rapport Phase I. Elle est destinée à éclairer la décision d'investissement du commanditaire.*
