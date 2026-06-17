# RAPPORT D'ANALYSE — PHASE I
## Mission de modernisation de l'infrastructure IT
### Client : Nova Syndicate

---

**Référence document** : NS-2026-001
**Auteur** : Dorian Poncelet — Responsable Technique
**Date** : Mai 2026
**Version** : 1.0
**Statut** : Livrable Phase I — Analyse des besoins
**Classification** : Confidentiel – Diffusion restreinte client

---

## SOMMAIRE

1. [Synthèse exécutive](#1-synthèse-exécutive)
2. [Contexte de la mission](#2-contexte-de-la-mission)
3. [Présentation du client Nova Syndicate](#3-présentation-du-client-nova-syndicate)
4. [Cadre méthodologique](#4-cadre-méthodologique)
5. [Analyse des besoins](#5-analyse-des-besoins)
6. [Identification des contraintes](#6-identification-des-contraintes)
7. [Priorisation des objectifs](#7-priorisation-des-objectifs)
8. [Étude des solutions](#8-étude-des-solutions)
9. [Architecture proposée — Vue d'ensemble](#9-architecture-proposée--vue-densemble)
10. [Plan d'exécution prévisionnel](#10-plan-dexécution-prévisionnel)
11. [Synthèse et engagement](#11-synthèse-et-engagement)

---

## 1. Synthèse exécutive

Nova Syndicate, PME française spécialisée dans la distribution de composants high-tech destinés aux secteurs **médical, aérospatial et défense**, fait appel à notre cabinet pour conduire la **modernisation complète de son infrastructure informatique**.

L'audit initial a révélé une infrastructure **fragmentée, obsolète et non-centralisée**, incompatible avec les exigences de continuité, de traçabilité et de confidentialité imposées par les secteurs d'activité du client.

Notre analyse identifie **sept axes de transformation prioritaires** : centralisation des identités, sécurisation périmétrique, segmentation réseau, supervision continue, sauvegardes résilientes, accès distant sécurisé pour les commerciaux itinérants, et interconnexion sécurisée des deux sites (Lyon et Marseille).

La solution préconisée repose sur une **stack open-source production-grade** (Proxmox VE, OPNsense, Samba 4, Wazuh) déployée en Infrastructure-as-Code (Terraform + Cloud-Init). Cette approche permet de réduire le **TCO sur 3 ans de 89 %** par rapport à une solution propriétaire équivalente (Microsoft + Cisco + Splunk), tout en garantissant l'évolutivité, la reproductibilité et la souveraineté technologique.

**Indicateurs clés du livrable final visé** :
- 12 machines virtuelles déployées en 2 sites
- 5 VLANs segmentés + 6 bridges réseau isolés
- 1 tunnel IPsec IKEv2 AES-256 inter-sites
- Conformité **Deny-by-Default** sur l'ensemble des interfaces firewall
- SIEM avec collecte centralisée des logs
- TCO 3 ans estimé : **14 700 €** (vs. 132 920 € en solution propriétaire)

---

## 2. Contexte de la mission

### 2.1 Origine de la demande

Nova Syndicate a engagé une démarche de transformation numérique fin 2025. Sa direction générale a constaté que l'infrastructure héritée — accumulée au fil de la croissance — ne répondait plus aux exigences :
- de **continuité de service** indispensable à ses clients institutionnels,
- de **traçabilité et auditabilité** imposées par les secteurs réglementés,
- d'**agilité opérationnelle** face à une croissance de +30 %/an du chiffre d'affaires.

Le présent dossier formalise la mission confiée à notre cabinet en tant que **consultants informatiques externes**, mandatés pour la conception, le déploiement et la documentation de la cible.

### 2.2 Périmètre fonctionnel

Le périmètre couvre l'**intégralité de l'infrastructure interne** du client : serveurs, réseau, sécurité, supervision, sauvegardes, accès distants et interconnexion multi-sites.

Sont **hors périmètre** :
- Les postes de travail des collaborateurs (gérés par le service IT interne du client).
- Les applications métier hébergées en SaaS (non concernées par la transformation).
- La téléphonie sur IP (à étudier en phase ultérieure).

### 2.3 Modalités d'engagement

| Élément | Valeur |
|---------|--------|
| Type de mission | Consulting + Build + Documentation |
| Durée prévue | 4 jours pleins (sprint intensif) |
| Mode de livraison | Infrastructure-as-Code + dossier technique + démonstration |
| Engagement de résultat | Infrastructure fonctionnelle conforme aux exigences techniques minimales |
| Livraison documentaire | Dossier de spécifications + manuel d'exploitation + scripts |

---

## 3. Présentation du client Nova Syndicate

### 3.1 Identité de l'entreprise

| Caractéristique | Valeur |
|-----------------|--------|
| **Raison sociale** | Nova Syndicate |
| **Secteur** | Logistique de haute technologie / Distribution de composants cybernétiques |
| **Marchés clients** | Médical · Aérospatial · Défense |
| **Siège social** | Lyon, France |
| **Site secondaire** | Marseille, France (bureau régional) |
| **Effectif total** | 85 collaborateurs |
| **Statut juridique** | PME française |
| **Maturité numérique** | Faible (infrastructure héritée, non-centralisée) |

### 3.2 Répartition des effectifs

| Site / Statut | Effectif | Typologie |
|---------------|----------|-----------|
| **Lyon (siège)** | 40 | Direction, administration, R&D, IT |
| **Marseille (bureau régional)** | 25 | Logistique, support technique régional |
| **Commerciaux itinérants (remote)** | 20 | Force commerciale terrain — partout en France |
| **Total** | **85** | |

### 3.3 Activité et exigences sectorielles

Nova Syndicate distribue des composants critiques à destination de :
- **Secteur médical** : équipements de diagnostic, instruments chirurgicaux connectés, dispositifs implantables.
- **Secteur aérospatial** : composants embarqués avioniques, équipements de test au sol.
- **Secteur défense** : composants électroniques pour systèmes d'armes, équipements communicants durcis.

Ces secteurs imposent un cadre réglementaire et normatif strict :

| Norme / Régulation | Implication infrastructure |
|--------------------|-----------------------------|
| **RGPD (Règlement européen 2016/679)** | Protection des données personnelles clients et collaborateurs |
| **ISO 27001** | Système de management de la sécurité de l'information (visée) |
| **ISO 13485** (médical) | Traçabilité des produits et des accès |
| **DEF-STAN / EN 9100** (défense / aéro) | Confidentialité, segmentation, journalisation |
| **Loi de Programmation Militaire (LPM)** | Protection des données sensibles défense |

### 3.4 Diagnostic de l'existant (audit initial)

L'audit initial mené sur site (Lyon et Marseille) a mis en évidence :

**Constats négatifs :**
- Aucun annuaire centralisé : comptes utilisateurs créés manuellement sur chaque poste.
- Partage de fichiers via des disques réseau locaux non répliqués, sans contrôle d'accès granulaire.
- Aucun firewall périmétrique configuré : la box opérateur fait office de passerelle directe.
- Aucun système de supervision : les incidents ne sont identifiés qu'a posteriori, par les utilisateurs.
- Sauvegardes ponctuelles, sans procédure formalisée, sans test de restauration.
- Accès distant des commerciaux : VPN gratuits grand public installés à l'initiative individuelle.
- Aucune ségrégation entre serveurs critiques et postes utilisateurs.
- Aucune politique de mots de passe.

**Points forts identifiés :**
- Personnel IT motivé et compétent (2 ETP, principalement orientés support utilisateur).
- Direction sponsor du projet, budget validé pour 36 mois.
- Capacité d'investissement en infrastructure (matériel et licences open-source).

---

## 4. Cadre méthodologique

### 4.1 Démarche adoptée

Notre intervention suit une démarche structurée en **trois phases** alignée sur les bonnes pratiques de conduite de projet IT :

```
┌────────────────────────────────────────────────────────────────┐
│  PHASE I — Comprendre  →  PHASE II — Concevoir & Déployer      │
│                                            ↓                    │
│                              PHASE III — Améliorer & Renforcer  │
└────────────────────────────────────────────────────────────────┘
```

Le présent document constitue le livrable de la **Phase I**.

### 4.2 Référentiels appliqués

- **Architecture** : approche *Security by Design* (NIST SP 800-160).
- **Sécurité réseau** : modèle *Zero Trust* (NIST SP 800-207) + *Defense in Depth*.
- **Gestion des accès** : principe du *Least Privilege* (ANSSI).
- **Continuité d'activité** : ISO 22301.
- **Sécurité de l'information** : ISO 27001/27002.
- **Modélisation des menaces** : STRIDE (Microsoft Threat Modeling).

### 4.3 Outils de pilotage du projet

- **Gestion de projet** : Notion (Kanban + Gantt + budget + documentation).
- **Versioning** : Git (GitHub).
- **Infrastructure-as-Code** : Terraform + Cloud-Init.
- **Documentation technique** : Markdown + Excalidraw (schémas) + Word/PDF (livrables).

---

## 5. Analyse des besoins

### 5.1 Besoins fonctionnels

#### B-FCT-01 : Gestion centralisée des identités
**Description** : Disposer d'un annuaire unique répertoriant l'ensemble des 85 collaborateurs avec leurs droits d'accès aux ressources.
**Justification** : Suppression du provisionnement manuel par poste, traçabilité des comptes, conformité RGPD.
**Criticité** : ★★★ Critique

#### B-FCT-02 : Hébergement d'un portail web interne / public
**Description** : Plateforme web pour les commerciaux (consultation catalogue, suivi des commandes) avec exposition publique.
**Justification** : Mobilité des commerciaux, vitrine client, suivi en temps réel.
**Criticité** : ★★ Haute

#### B-FCT-03 : Base de données relationnelle métier
**Description** : Stockage centralisé du catalogue produits, des références clients, des historiques de commandes.
**Justification** : Données critiques de l'activité, requêtes complexes, intégrité référentielle.
**Criticité** : ★★★ Critique

#### B-FCT-04 : Partage de fichiers d'entreprise
**Description** : Espace de stockage centralisé, accessible avec authentification, depuis les deux sites.
**Justification** : Suppression des copies locales non synchronisées, contrôle d'accès, audit.
**Criticité** : ★★★ Critique

#### B-FCT-05 : Messagerie interne
**Description** : Service email interne pour les collaborateurs (volume initial : 85 boîtes).
**Justification** : Souveraineté des échanges (secteur défense), maîtrise des coûts récurrents.
**Criticité** : ★★ Haute

#### B-FCT-06 : Accès distant sécurisé pour les commerciaux
**Description** : Connexion VPN pour les 20 commerciaux itinérants leur permettant d'accéder aux ressources internes.
**Justification** : Mobilité commerciale, sécurisation des accès depuis l'extérieur.
**Criticité** : ★★★ Critique

#### B-FCT-07 : Interconnexion sécurisée des sites
**Description** : Liaison chiffrée et permanente entre Lyon et Marseille permettant le partage des ressources.
**Justification** : Productivité du site régional, accès AD et fichiers transverses.
**Criticité** : ★★★ Critique

### 5.2 Besoins non-fonctionnels

#### B-NFC-01 : Sécurité
- Chiffrement systématique des flux sortants (TLS, IPsec).
- Authentification forte pour les accès administrateurs.
- Politique *Deny-by-Default* sur l'ensemble du périmètre.
- Détection des intrusions sur le périmètre externe.

#### B-NFC-02 : Disponibilité
- Disponibilité cible globale : **99,5 %** (4 h d'indisponibilité tolérée par mois).
- Disponibilité du portail web public : **99,9 %**.
- Tolérance à la perte d'un site (continuité partielle si Marseille tombe).

#### B-NFC-03 : Confidentialité
- Segmentation stricte entre les segments réseau (DMZ / SERVERS / USERS / MGMT).
- Aucun accès direct depuis Internet vers les serveurs internes.
- Logs d'accès conservés au minimum 12 mois (exigence sectorielle).

#### B-NFC-04 : Traçabilité
- Journalisation centralisée de tous les événements de sécurité.
- Alerte temps réel en cas d'anomalie comportementale.
- Conservation des logs sur stockage isolé du périmètre attaqué (anti-falsification).

#### B-NFC-05 : Évolutivité
- Capacité à doubler le nombre d'utilisateurs sans refonte d'architecture.
- Provisionnement de nouvelles machines virtuelles en moins de 5 minutes via IaC.
- Modèle d'adressage permettant l'extension à un troisième site.

#### B-NFC-06 : Maintenabilité
- Configuration entièrement versionnée (Git).
- Procédures opérationnelles documentées.
- Capacité de reconstruction complète à partir du code en moins de 4 heures.

#### B-NFC-07 : Coût total de possession (TCO)
- Budget plafonné par la direction : **20 000 € HT sur 3 ans** (CAPEX + OPEX hors temps homme).
- Préférence pour les solutions open-source avec support communautaire.

---

## 6. Identification des contraintes

### 6.1 Contraintes techniques

| Code | Contrainte | Impact |
|------|------------|--------|
| C-TECH-01 | Multi-site (Lyon + Marseille) — pas de fibre dédiée inter-sites | Nécessité d'un tunnel chiffré via Internet (IPsec) |
| C-TECH-02 | Hétérogénéité des accès distants (commerciaux remote) | VPN nomade obligatoire (OpenVPN) |
| C-TECH-03 | Budget hardware limité | Mutualisation via virtualisation obligatoire |
| C-TECH-04 | Pas d'expertise interne sur les solutions propriétaires (VMware, Cisco) | Stack open-source privilégiée |
| C-TECH-05 | Délai serré (4 jours pour la mission) | Industrialisation IaC indispensable |

### 6.2 Contraintes sécuritaires

| Code | Contrainte | Impact |
|------|------------|--------|
| C-SEC-01 | Secteurs réglementés (médical/aéro/défense) | Segmentation forte + journalisation centralisée |
| C-SEC-02 | RGPD | Données personnelles isolées, chiffrement au repos et en transit |
| C-SEC-03 | Accès distant à des données classifiées | Bastion + VPN + MFA recommandé |
| C-SEC-04 | Surface d'attaque réduite obligatoire | DMZ stricte, egress filtré |

### 6.3 Contraintes organisationnelles

| Code | Contrainte | Impact |
|------|------------|--------|
| C-ORG-01 | Équipe IT interne réduite (2 ETP) | Documentation exhaustive + automatisation maximale |
| C-ORG-02 | Direction non-technique | Livrables avec restitution synthétique (slides) |
| C-ORG-03 | Croissance prévue +30 %/an | Architecture évolutive sans refonte |
| C-ORG-04 | Reproductibilité du déploiement exigée | Infrastructure-as-Code complète |

---

## 7. Priorisation des objectifs

La matrice ci-dessous priorise les objectifs selon la grille **Importance × Urgence** (Eisenhower).

| # | Objectif | Importance | Urgence | Priorité |
|---|----------|------------|---------|----------|
| 1 | Centralisation des identités (AD) | ★★★ | ★★★ | **P1 – À faire en premier** |
| 2 | Firewall périmétrique + segmentation | ★★★ | ★★★ | **P1 – À faire en premier** |
| 3 | Interconnexion sécurisée Lyon ↔ Marseille | ★★★ | ★★★ | **P1 – À faire en premier** |
| 4 | Supervision continue (SIEM) | ★★★ | ★★ | **P2 – À planifier** |
| 5 | Sauvegardes automatisées | ★★★ | ★★ | **P2 – À planifier** |
| 6 | Accès distant commerciaux (VPN) | ★★★ | ★★ | **P2 – À planifier** |
| 7 | Portail web + base de données métier | ★★ | ★★ | **P2 – À planifier** |
| 8 | Messagerie interne | ★★ | ★ | **P3 – À déléguer/différer** |
| 9 | Détection intrusion (IDS) | ★★★ | ★ | **P3 – À mettre en place ensuite** |
| 10 | Honeypot (leurre attaquant) | ★ | ★ | **P4 – Optionnel** |

---

## 8. Étude des solutions

### 8.1 Solutions étudiées

Trois trajectoires ont été instruites pour répondre aux besoins exprimés :

**Solution A — "Premium propriétaire"**
Stack entièrement basée sur des éditeurs leaders (Microsoft, Cisco, Splunk, VMware).
→ Coût élevé, support 24/7 inclus, courbe d'apprentissage maîtrisée.

**Solution B — "Open-source production-grade" (RETENUE)**
Stack open-source professionnelle (Proxmox, OPNsense, Samba, Wazuh).
→ Coût marginal, communauté active, contrôle total de la stack.

**Solution C — "Cloud public AWS/Azure"**
Migration intégrale vers un fournisseur cloud public.
→ OPEX élevé, dépendance fournisseur, problèmes de souveraineté pour la défense.

### 8.2 Comparatif TCO sur 3 ans

| Poste | Solution A — Propriétaire | Solution B — Open-source (retenue) | Solution C — Cloud public |
|-------|---------------------------|-----------------------------------|---------------------------|
| Hyperviseur | VMware vSphere : 8 000 € | Proxmox VE : 0 € | AWS EC2 : 12 000 €/an |
| Firewall | Fortinet 100F : 4 500 € + 5 400 € licences | OPNsense : 0 € | AWS Security Groups : inclus |
| SIEM | Splunk Enterprise : 22 000 €/an | Wazuh : 0 € | AWS GuardDuty : 4 200 €/an |
| EDR | MS Defender P2 : 5 400 €/an | inclus Wazuh | MS Defender P2 : 5 400 €/an |
| AD | Win Server + CAL : 8 000 € + 1 200 €/an | Samba 4 : 0 € | AWS Directory Service : 1 800 €/an |
| Backup | Veeam : 1 500 € + 600 €/an | rsync + scripts : 0 € | AWS Backup : 1 200 €/an |
| Mail | M365 Business Std : 6 480 €/an | Postfix + Dovecot : 0 € | M365 ou SES : 6 480 €/an |
| VPN remote | Cisco AnyConnect : 1 200 €/an | OpenVPN : 0 € | AWS Client VPN : 3 600 €/an |
| IDS | inclus Fortinet UTM | Suricata : 0 € | AWS GuardDuty : inclus |
| Supervision | PRTG : 1 800 € + 360 €/an | Wazuh : inclus | CloudWatch : 600 €/an |
| Hardware lab | 1 PC tour 32 GB : 1 200 € | 1 PC tour 32 GB : 1 200 € | 0 € (cloud) |
| Temps homme déploiement (1 ETP × 1 mois) | 4 500 € | 4 500 € | 4 500 € |
| **TOTAL CAPEX** | **23 200 €** | **1 200 €** | **0 €** |
| **TOTAL OPEX 3 ans** | **109 720 €** | **13 500 €** | **122 700 €** |
| **TCO 3 ans** | **132 920 €** | **14 700 €** | **122 700 €** |

### 8.3 Justification du choix — Solution B

| Critère | Solution A | Solution B (RETENUE) | Solution C |
|---------|------------|----------------------|------------|
| Coût TCO 3 ans | 132 920 € | **14 700 €** ✅ | 122 700 € |
| Conformité au budget client (20 000 €) | ❌ Dépassement | ✅ Respect | ❌ Dépassement |
| Souveraineté technologique | ❌ US-centric | ✅ Open-source | ❌ Hébergement US |
| Reproductibilité (IaC) | ⚠️ Partielle | ✅ Totale | ✅ Native cloud |
| Capacité d'apprentissage interne | ⚠️ Licences requises | ✅ Communauté libre | ⚠️ Compétences cloud |
| Conformité défense / classifié | ⚠️ Variable | ✅ Stack maîtrisée | ❌ Hébergement extérieur |
| Support 24/7 | ✅ Inclus | ⚠️ Communautaire | ✅ Cloud provider |
| Indépendance vis-à-vis d'un fournisseur unique | ❌ Lock-in | ✅ Aucun lock-in | ❌ Lock-in cloud |
| **Score global** | 4/8 | **7/8** ✅ | 4/8 |

**Décision** : la Solution B est retenue car elle satisfait toutes les contraintes (budget, souveraineté, reproductibilité, conformité sectorielle) avec une économie de **118 220 € sur 3 ans** par rapport à la Solution A.

**Tradeoffs assumés** :
- Pas de support contractuel 24/7 (mitigé par la documentation exhaustive et la formation de l'équipe interne).
- Courbe d'apprentissage initiale (mitigée par la stack standardisée et la livraison clé en main).
- Responsabilité du suivi sécuritaire interne (mitigée par Wazuh et automatisation des correctifs).

---

## 9. Architecture proposée — Vue d'ensemble

### 9.1 Topologie cible

```
                                Internet
                                    │
                       ┌────────────┴────────────┐
                       │       OPNsense Lyon      │ ◄─ IPsec IKEv2 AES-256 ─► OPNsense Marseille
                       │  (Hub firewall · IDS)   │                            (Spoke firewall)
                       └────────────┬────────────┘                                      │
                                    │                                                   │
        ┌──────────────────────────┼──────────────────────────┐                      │
        │                          │                          │                      │
   ┌────┴────┐              ┌──────┴──────┐           ┌───────┴───────┐         ┌────┴────┐
   │   DMZ   │              │   SERVERS   │           │     MGMT      │         │  LAN    │
   │ VLAN 5  │              │  VLAN 10    │           │   vmbr2 isolé │         │ Marseille│
   │         │              │             │           │               │         │  VLAN 50│
   │ Web-01  │              │ DC01 (AD)   │           │  Bastion-01   │         │ DNS-Mar │
   │ Proxy   │              │ Wazuh SIEM  │           │  (SSH jump)   │         │         │
   │ Mail    │              │ DB-01       │           │               │         │ RODC-01 │
   │ Honeypot│              │ File-01     │           │               │         │  (bonus)│
   └─────────┘              │ Backup-01   │           └───────────────┘         └─────────┘
                            └─────────────┘
                                  │
                          Collecte logs vmbr5
                            (Wazuh eth1)
```

### 9.2 Caractéristiques principales

| Composant | Caractéristique | Quantité |
|-----------|------------------|----------|
| Hyperviseur | Proxmox VE 9.1 | 1 |
| Bridges réseau | Linux Bridge (VLAN-aware sur vmbr1/vmbr3) | 6 |
| Pare-feu | OPNsense 26.x | 2 (Lyon + Marseille) |
| VLANs | Segmentation logique L2 | 5 |
| VMs Linux | Debian 12 cloud-init | 10 |
| Tunnel inter-sites | IPsec IKEv2 AES-256 SHA-512 PFS G20 | 1 |
| Annuaire | Samba 4 Active Directory | 1 (+ RODC option) |
| SIEM | Wazuh 4.x (Manager + Indexer + Dashboard) | 1 |
| Bastion | Linux Debian + SSH | 1 |

### 9.3 Principes architecturaux appliqués

- **Defense in Depth** : 4 niveaux de filtrage (périmètre, inter-VLAN, hôte, application).
- **Deny-by-Default** : aucune règle "allow any", chaque flux explicitement autorisé.
- **Least Privilege** : segmentation par fonction (DMZ ≠ SERVERS ≠ MGMT).
- **Network Segmentation** : 5 VLANs + bridges physiquement isolés (vmbr2 MGMT, vmbr4 Quarantaine).
- **Zero Trust** : authentification systématique, même intra-réseau.
- **Hub & Spoke** : Lyon = point d'entrée unique, Marseille transite via Lyon.
- **Isolation forte** : Bastion sur bridge dédié, pas de VLAN-hopping possible.
- **Infrastructure-as-Code** : Terraform + Cloud-Init + scripts CLI versionnés Git.

---

## 10. Plan d'exécution prévisionnel

### 10.1 Planning macro

| Jour | Activité | Livrable |
|------|----------|----------|
| **J1** | Phase II – Conception : déploiement Proxmox, Terraform, VMs Debian, OPNsense Lyon | Infrastructure de base |
| **J2** | Phase II – Conception : OPNsense Marseille, IPsec, AD Samba, Wazuh, Web, DB | Services métier opérationnels |
| **J3** | Phase II – Conception : Mail, File, Backup, OpenVPN | Services complémentaires |
| **J4** | Phase III – Amélioration : Sécurité avancée, tests, PCA/PRA, documentation | Livrables finaux |

### 10.2 Allocation des ressources

- **Hardware** : 1 PC bureautique 32 GB RAM avec virtualisation imbriquée.
- **Logiciel** : 100 % open-source (zéro licence à acquérir).
- **Humain** : 1 ETP (mission consulting).
- **Documentation** : rédigée en parallèle de la build pour garantir l'exhaustivité.

### 10.3 Jalons et points de contrôle

| Jalon | Critère de validation | Date |
|-------|------------------------|------|
| J1 — Fin de journée | OPNsense Lyon up + 10 VMs Debian configurées (Cloud-Init) | J1 17h |
| J2 — Fin de journée | AD opérationnel + Wazuh dashboard avec agents + web accessible | J2 17h |
| J3 — Fin de journée | Mail SMTP/IMAP + Nextcloud + Backup automatisé + VPN testé | J3 17h |
| J4 — Fin de mission | Tous livrables documentaires remis | J4 17h |

---

## 11. Synthèse et engagement

### 11.1 Engagement de notre cabinet

À l'issue de cette mission, nous nous engageons à livrer au client Nova Syndicate :

1. Une **infrastructure pleinement opérationnelle** conforme à l'architecture cible décrite.
2. Un **dossier de spécifications techniques** détaillant les choix et les configurations.
3. Un **plan de continuité d'activité (PCA)** et un **plan de reprise après sinistre (PRA)** adaptés au contexte.
4. Une **documentation d'exploitation** permettant à l'équipe interne du client de reprendre la main.
5. Un **ensemble de scripts d'automatisation** réduisant la charge opérationnelle récurrente.
6. Un **rapport de tests d'intrusion** validant le niveau de sécurité atteint.

### 11.2 Bénéfices attendus pour Nova Syndicate

| Bénéfice | Indicateur |
|----------|------------|
| Réduction du TCO IT | **−89 %** sur 3 ans vs solution propriétaire |
| Centralisation des identités | 1 annuaire vs 85 comptes manuels |
| Sécurisation des accès distants | 20 commerciaux protégés VPN au lieu de VPN grand public |
| Détection des incidents | Temps de détection : de plusieurs jours à **temps réel** |
| Continuité d'activité | Couverture multi-site avec interconnexion chiffrée |
| Reproductibilité | Reconstruction complète en **< 4 heures** depuis le code |
| Conformité sectorielle | Posture compatible avec ISO 27001, RGPD, exigences défense |

### 11.3 Prochaine étape

L'acceptation du présent rapport déclenche le **lancement de la Phase II – Conception et déploiement**, dont les livrables détaillés (schémas, documentation technique, preuves de fonctionnement) sont à produire dans les 3 jours ouvrés suivants.

---

**Document arrêté à la version 1.0** — Mai 2026

*Ce document est la propriété de [Cabinet] et de son client Nova Syndicate. Toute reproduction ou diffusion, partielle ou totale, est soumise à autorisation écrite préalable.*
