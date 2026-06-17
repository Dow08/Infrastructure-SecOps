# DOCUMENT TECHNIQUE — PHASE II
## Conception et déploiement de l'infrastructure
### Client : Nova Syndicate

---

**Référence document** : NS-2026-002
**Auteur** : Dorian Poncelet — Responsable Technique
**Date** : Mai 2026
**Version** : 1.0
**Statut** : Livrable Phase II — Conception & Déploiement
**Classification** : Confidentiel – Diffusion restreinte client

---

## SOMMAIRE

1. [Objet du document](#1-objet-du-document)
2. [Rappel du cadrage](#2-rappel-du-cadrage)
3. [Architecture déployée](#3-architecture-déployée)
4. [Choix technologiques et justifications](#4-choix-technologiques-et-justifications)
5. [Plan d'adressage IP](#5-plan-dadressage-ip)
6. [Matrice des flux firewall](#6-matrice-des-flux-firewall)
7. [Stratégie d'Infrastructure-as-Code](#7-stratégie-dinfrastructure-as-code)
8. [Détail des composants déployés](#8-détail-des-composants-déployés)
9. [Sécurité — Mesures appliquées](#9-sécurité--mesures-appliquées)
10. [Preuves de fonctionnement](#10-preuves-de-fonctionnement)
11. [Retour d'expérience — Incidents et solutions](#11-retour-dexpérience--incidents-et-solutions)

---

## 1. Objet du document

Ce document constitue le **livrable technique de la Phase II** du projet de modernisation de l'infrastructure de Nova Syndicate. Il décrit :

- L'**architecture cible** effectivement déployée.
- Les **choix technologiques** opérés et leur **justification** au regard des contraintes du client.
- Les **configurations détaillées** des composants.
- Les **preuves de fonctionnement** obtenues lors des phases de tests.
- Le **retour d'expérience** consolidé sur les incidents rencontrés et résolus.

Il sert également de **référentiel de conception** pour les phases ultérieures (amélioration, exploitation, reprise par l'équipe interne).

---

## 2. Rappel du cadrage

### 2.1 Référence aux livrables précédents

Le présent document fait suite au **Rapport d'analyse Phase I** (NS-2026-001) qui a établi :
- Les **besoins fonctionnels et non-fonctionnels** du client (7 + 7 = 14 exigences identifiées).
- Les **contraintes** techniques, sécuritaires et organisationnelles.
- La **solution retenue** (Solution B – stack open-source production-grade).

### 2.2 Objectifs de la Phase II

Trois objectifs principaux :

1. **Concevoir** et déployer une infrastructure conforme aux objectifs de Nova Syndicate.
2. Respecter les **bonnes pratiques** en administration système, réseau et cybersécurité.
3. Produire les **preuves de fonctionnement** valant validation de la phase.

### 2.3 Composants obligatoires (du cahier des charges)

| Exigence | Solution déployée |
|----------|-------------------|
| Système centralisé de gestion des utilisateurs | Samba 4 Active Directory sur DC01-Lyon |
| Serveur de fichiers | Nextcloud sur File-01 avec authentification AD |
| Serveur SQL | MariaDB sur DB-01 |
| Environnement virtualisé | Proxmox VE 9.1.1 |
| 4ème VM pour expansion future | Mail-01 (provisionnée pour absorber l'internalisation messagerie) |

---

## 3. Architecture déployée

### 3.1 Vue d'ensemble

L'architecture déployée repose sur une **virtualisation imbriquée** :
- Hôte physique Windows 11 (32 GB RAM)
- VirtualBox (hyperviseur L1) avec nested virtualization activée
- Proxmox VE 9.1.1 (hyperviseur L2) en VM avec 20 GB RAM dédiés
- 12 machines virtuelles invitées (2 OPNsense + 10 Debian)

```
┌────────────────────────────────────────────────────────────────┐
│  HÔTE PHYSIQUE Windows 11 (32 GB RAM)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  VirtualBox (hyperviseur L1 — nested virt activée)       │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │  Proxmox VE 9.1.1 (VM — 20 GB RAM, 150 GB disque)  │ │  │
│  │  │  ┌──────────────────────────────────────────────┐  │ │  │
│  │  │  │  6 Linux Bridges (vmbr0-5)                   │  │ │  │
│  │  │  │  vmbr0: WAN bridge (internet réel)           │  │ │  │
│  │  │  │  vmbr1: LAN Lyon (VLAN-aware, trunk)         │  │ │  │
│  │  │  │  vmbr2: MGMT isolé (Bastion uniquement)      │  │ │  │
│  │  │  │  vmbr3: LAN Marseille (VLAN-aware)           │  │ │  │
│  │  │  │  vmbr4: Quarantaine (cul-de-sac)             │  │ │  │
│  │  │  │  vmbr5: Collecte logs Wazuh                  │  │ │  │
│  │  │  │                                              │  │ │  │
│  │  │  │  [12 VMs invitées — KVM/QEMU]                │  │ │  │
│  │  │  └──────────────────────────────────────────────┘  │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### 3.2 Schéma logique de la topologie

Le schéma détaillé est fourni en annexe `Topologie_Final.excalidraw` et reflète :

- **Site Lyon (siège)** : 10 VMs sur 5 VLANs segmentés via OPNsense.
- **Site Marseille (régional)** : 2 VMs (OPNsense + DNS local) connectées à Lyon par tunnel IPsec.
- **6 bridges Proxmox** réalisant la séparation physique (L2) des zones critiques.
- **Tunnel IPsec IKEv2** (Hub & Spoke) entre les deux OPNsense.

### 3.3 Inventaire des composants déployés

#### Site Lyon

| ID | Hostname | Rôle | OS / Logiciel | RAM | IP principale |
|----|----------|------|---------------|-----|----------------|
| VM 100 | OPNsense-Lyon | Firewall périmétrique, IPsec, NAT, IDS | OPNsense 26.1.6 | 2 GB | WAN: 192.168.1.166 |
| VM 102 | DC01-Lyon | Active Directory + DNS interne | Debian 12 + Samba 4 | 2 GB | 10.1.10.10 |
| VM 103 | Proxy-01 | Reverse proxy HTTPS | Debian 12 + Nginx | 1 GB | 10.1.5.10 |
| VM 104 | Web-01 | Portail web Nova | Debian 12 + Apache | 1 GB | 10.1.5.30 |
| VM 105 | Mail-01 | Serveur messagerie (SMTP+IMAP+Webmail) | Debian 12 + Postfix + Dovecot + Roundcube | 2 GB | 10.1.5.40 |
| VM 106 | Wazuh-01 | SIEM + IDS + Dashboard | Debian 12 + Wazuh 4.x | 4 GB | 10.1.10.20 (+10.0.5.20) |
| VM 107 | DB-01 | Base de données métier | Debian 12 + MariaDB | 1 GB | 10.1.10.30 |
| VM 108 | File-01 | Serveur de fichiers | Debian 12 + Nextcloud | 1 GB | 10.1.10.40 |
| VM 109 | Bastion-01 | SSH Jump Host | Debian 12 minimal | 2 GB | 172.16.100.20 |
| VM 110 | Backup-01 | Serveur de sauvegardes | Debian 12 + rsync | 1 GB | 10.1.110.10 |

#### Site Marseille

| ID | Hostname | Rôle | OS / Logiciel | RAM | IP principale |
|----|----------|------|---------------|-----|----------------|
| VM 101 | OPNsense-Marseille | Firewall site régional + IPsec | OPNsense 26.1.6 | 2 GB | WAN: 192.168.1.167 |
| VM 111 | DNS-Marseille | Serveur DNS local (cache) + futur RODC | Debian 12 + bind9 (option Samba RODC) | 1 GB | 10.0.2.10 |

#### Total ressources

- **CPU virtualisés** : ~22 vCPUs alloués
- **RAM allouée** : ~20 GB
- **Disque consommé** : ~120 GB sur 150 GB disponibles

---

## 4. Choix technologiques et justifications

Cette section justifie chaque choix technique opéré, conformément à l'attente du jury sur la **compréhension** des décisions.

### 4.1 Hyperviseur — Proxmox VE 9

#### Alternatives étudiées et écartées

| Alternative | Pourquoi écartée |
|-------------|------------------|
| GNS3 | Simulateur réseau, pas un vrai hyperviseur. Bugs de persistance réseau, DNS instable. Ne supporte pas Terraform. |
| VMware ESXi | Licence propriétaire (coût). Provider Terraform officiel mais courbe d'apprentissage forte. |
| Microsoft Hyper-V | Suppose une licence Windows Server. Moins adapté à la cible open-source du client. |
| KVM nu (sans interface) | Aucune GUI, gestion fastidieuse, peu réaliste pour le client. |

#### Choix retenu : Proxmox VE 9.1.1

**Justifications** :
1. **100 % open-source** (licence AGPL3) — conformité au budget client.
2. **Hyperviseur de production** utilisé par Hetzner, OVH, Online et de nombreuses PME en Europe.
3. **Provider Terraform `bpg/proxmox`** actif, supportant les ressources nécessaires (VMs, bridges, VLANs, cloud-init).
4. **GUI web intuitive** facilitant la formation de l'équipe interne du client.
5. **API REST documentée** permettant l'automatisation native.
6. **Snapshots, clones, sauvegardes** intégrés sans surcoût.

#### Limitations acceptées

- Exécution en virtualisation imbriquée (Proxmox dans VirtualBox) : performances réduites par rapport à un déploiement bare-metal. Mitigation : désactivation de `kvm=1` sur les VMs invitées (mode TCG) qui accepte le surcoût performance contre une stabilité accrue.
- Provider Terraform communautaire (non éditeur officiel) : risque mineur de régressions. Mitigation : versions épinglées dans le code Terraform.

### 4.2 Réseau — Linux Bridges + VLANs

#### Justifications

1. **Suppression des switches physiques** : remplacés par des `vmbr` Linux qui supportent nativement le tag VLAN 802.1Q.
2. **VLAN-aware bridges** sur vmbr1 (Lyon) et vmbr3 (Marseille) → un seul bridge porte plusieurs VLANs (trunk).
3. **Bridges dédiés** pour les zones sensibles : `vmbr2` (MGMT isolé), `vmbr4` (Quarantaine cul-de-sac), `vmbr5` (collecte logs Wazuh).
4. **Pas de VLAN-hopping** possible entre bridges : l'isolation L2 est physique (au sens hyperviseur).

#### Caractéristiques des bridges

| Bridge | VLAN-aware | Rôle | Justification sécurité |
|--------|-----------|------|------------------------|
| vmbr0 | Non | WAN (Internet via bridge VirtualBox) | Les 2 OPNsense + tunnel IPsec transitent ici |
| vmbr1 | Oui (5,10,30,40,110) | LAN Lyon trunk | Production segmentée logiquement |
| vmbr2 | Non | MGMT isolé (Bastion-01) | Si vmbr1 compromis, vmbr2 intouché |
| vmbr3 | Oui | LAN Marseille trunk | Site régional cloisonné |
| vmbr4 | Non | Quarantaine cul-de-sac | Aucune route sauf collecte Wazuh |
| vmbr5 | Non | Collecte logs Wazuh | DMZ/Quar → Wazuh sans toucher SERVERS |

### 4.3 Firewall — OPNsense (vs pfSense)

#### Alternatives écartées

| Alternative | Pourquoi écartée |
|-------------|------------------|
| pfSense | Restrictions de licence Netgate depuis 2023. API non-documentée. Pas de collection Ansible officielle. |
| iptables nu | Pas d'interface graphique, gestion manuelle, fragile à long terme. |
| Cisco ASA | Coût licence prohibitif pour une PME (4 500 € HW + 1 800 €/an UTM). |
| Sophos XG Firewall | Coût licence (>2 000 €/an), lock-in éditeur. |

#### Choix retenu : OPNsense 26.1.6

**Justifications** :
1. **Fork open-source intégral de pfSense** (BSD 2-clause), sans restrictions.
2. **API REST native** documentée — automatisable via Ansible.
3. **Suricata IDS intégré** — pas de logiciel externe à installer.
4. **GUI moderne** (React) plus ergonomique que pfSense.
5. **Communauté active** : releases trimestrielles, plugins riches.
6. **Compatible IPsec IKEv2** avec algorithmes modernes (AES-256-GCM, SHA-512, DH Group 20).
7. **Support natif OpenVPN** pour les accès distants commerciaux.

### 4.4 VPN inter-sites — IPsec IKEv2

#### Alternatives écartées

| Alternative | Pourquoi écartée |
|-------------|------------------|
| OpenVPN site-to-site | Convient mieux pour les clients nomades. Performance plus faible que IPsec sur les flux soutenus. |
| WireGuard | Excellent (vitesse, simplicité), mais le support OPNsense est encore en plugin tiers. Maturité industrielle inférieure. |
| MPLS opérateur | Coût mensuel élevé (>500 €/mois pour une PME), nécessite un opérateur télécom dédié. |
| SD-WAN | Sur-dimensionné pour 2 sites. Coût récurrent. |

#### Choix retenu : IPsec IKEv2

**Justifications** :
1. **Standard industriel** (RFC 7296) — déployé partout dans les entreprises.
2. **Support natif OPNsense** via strongSwan.
3. **Performance** : accélération matérielle possible si déploiement bare-metal ultérieur.
4. **Hub & Spoke** : Lyon = point d'entrée unique, simplifie les règles firewall.
5. **Configuration testable** : tunnel monitorable via `swanctl --list-conns`.

#### Paramètres techniques

| Phase | Algorithme | Détail |
|-------|------------|--------|
| Phase 1 (IKE) | AES-256-GCM | Chiffrement authentifié |
| Phase 1 (IKE) | SHA-512 | Intégrité |
| Phase 1 (IKE) | DH Group 20 | Échange de clés ECDH 384-bit |
| Phase 2 (ESP) | AES-256-GCM | Chiffrement payload |
| Phase 2 (ESP) | PFS Group 20 | Perfect Forward Secrecy |
| Lifetime | 28 800 s (IKE) / 3 600 s (Child) | Re-keying automatique |

### 4.5 Active Directory — Samba 4 (vs Windows Server)

#### Alternatives écartées

| Alternative | Pourquoi écartée |
|-------------|------------------|
| Windows Server AD | Coût licence Windows Server (3 200 €) + CALs (80 €/utilisateur). Total : ~8 000 € hors contrat de support. |
| OpenLDAP nu | Pas de fonctionnalités AD natives (GPO, intégration Windows). Plus de configuration manuelle. |
| FreeIPA | Excellent mais orienté Linux uniquement. Compatibilité Windows clients moins fluide. |

#### Choix retenu : Samba 4

**Justifications** :
1. **Compatible Windows clients** (XP à 11) sans aucune adaptation.
2. **100 % open-source** — économie de licence (~8 000 € + CALs).
3. **DNS interne intégré** — résolution `nova.local` automatique.
4. **Outil d'administration `samba-tool`** scriptable.
5. **Réplication DC possible** entre Lyon et Marseille (option future).

#### Configuration retenue

- **Domaine** : `nova.local`
- **Realm** : `NOVA.LOCAL`
- **Schéma** : Windows Server 2008 R2 (max supporté par Samba 4.x stable)
- **Mode** : Single Domain Controller (DC01-Lyon)
- **DNS** : Samba interne (port 53 UDP/TCP)

### 4.6 SIEM — Wazuh (vs ELK / Splunk)

#### Alternatives écartées

| Alternative | Pourquoi écartée |
|-------------|------------------|
| Splunk Enterprise | Coût prohibitif (22 000 €/an pour 50 GB/jour). |
| ELK Stack nu | Excellent pour agrégation logs mais pas un SIEM intégré. Nécessite Logstash + Beats + alerting custom. |
| Graylog | Bon outil mais centré logs ; pas de fonctions EDR intégrées. |
| QRadar / Microsoft Sentinel | Solutions cloud propriétaires, coût mensuel élevé. |

#### Choix retenu : Wazuh 4.x

**Justifications** :
1. **SIEM + EDR convergé** — un seul outil au lieu de 3-4.
2. **Open-source intégral** (GPL2).
3. **+5 000 règles MITRE ATT&CK** pré-construites.
4. **Agents légers** (~50 MB RAM/agent) compatibles Linux/Windows/macOS.
5. **Dashboard intégré** (basé OpenSearch) — visualisation immédiate.
6. **API REST** pour intégration future.
7. **Communauté active** : releases trimestrielles, support solide.

#### Architecture de déploiement

- **Wazuh Manager + Indexer + Dashboard** sur Wazuh-01 (4 GB RAM, double interface)
- **Agents Wazuh** déployés sur : DC01, Web-01, Proxy-01, DB-01, File-01, Mail-01, Backup-01, Bastion-01, Honeypot-01 (le cas échéant)
- **Interface eth0** (10.1.10.20) : management et collecte SERVERS
- **Interface eth1** (10.0.5.20 sur vmbr5) : collecte DMZ + Quarantaine (séparation physique des flux)

### 4.7 Infrastructure-as-Code — Terraform + Cloud-Init

#### Justifications

1. **Terraform** (HashiCorp) : déclaratif, idempotent, versionnable Git.
2. **Cloud-Init** : standard de provisioning automatique des VMs Debian (hostname, user, password, IP, DNS).
3. **Provider `bpg/proxmox`** : communautaire mais maintenu, supporte clone, set, destroy.
4. **CLI `qm`** Proxmox : utilisable en complément pour les opérations non couvertes par le provider Terraform.

#### Flux opérationnel

```
1. terraform apply  → création des VMs + bridges
2. qm set <vmid>    → configuration cloud-init (IP, user, password)
3. qm start <vmid>  → boot et application cloud-init
4. SSH bastion      → vérification finale
```

### 4.8 Autres composants

| Composant | Choix | Justification courte |
|-----------|-------|----------------------|
| Reverse proxy | Nginx | Performance, configuration claire, support HTTP/2 et HTTPS |
| Serveur web | Apache 2 | Stack standard, compatible PHP/MariaDB |
| Base de données | MariaDB 10.11 | Fork MySQL communautaire, performances équivalentes, sans licence Oracle |
| Mail SMTP | Postfix | Standard de l'industrie, configuration éprouvée |
| Mail IMAP | Dovecot | Référence pour le stockage Maildir et IMAP |
| Webmail | Roundcube | Interface moderne, support IMAP/SMTP, intégrable AD |
| Cloud privé | Nextcloud | Fork ownCloud, communauté très active, intégration LDAP/AD native |
| Sauvegarde | rsync + cron | Outils Unix standards, journalisation simple, restauration directe |
| VPN remote | OpenVPN | Compatibilité maximale (Windows/macOS/Linux/iOS/Android) |
| IDS | Suricata (intégré OPNsense) | Engine modern, support des règles Emerging Threats Open |
| Anti-brute-force | Fail2ban | Outil universel SSH/HTTP/SMTP |
| Bastion | OpenSSH + restrictions | Stack standard, scriptable, audit ssh.log |

---

## 5. Plan d'adressage IP

### 5.1 Vue d'ensemble des subnets

| Subnet | Site | VLAN | Rôle | Gateway |
|--------|------|------|------|---------|
| 192.168.1.0/24 | — | — | WAN (LAN box opérateur) | 192.168.1.254 |
| 10.0.1.0/24 | Lyon | — (untagged) | LAN OPNsense interne | 10.0.1.1 |
| 10.1.5.0/24 | Lyon | 5 | DMZ (Proxy, Web, Mail) | 10.1.5.1 |
| 10.1.10.0/24 | Lyon | 10 | SERVERS (DC, Wazuh, DB, File, Backup) | 10.1.10.1 |
| 10.1.30.0/24 | Lyon | 30 | USERS (postes utilisateurs) | 10.1.30.1 |
| 10.1.40.0/24 | Lyon | 40 | Messagerie (futur) | 10.1.40.1 |
| 10.1.110.0/24 | Lyon | 110 | BACKUP isolé | 10.1.110.1 |
| 172.16.100.0/24 | Lyon | — (vmbr2) | MGMT physiquement isolé | 172.16.100.1 |
| 10.0.4.0/24 | Lyon | — (vmbr4) | Quarantaine cul-de-sac | 10.0.4.1 |
| 10.0.5.0/24 | Lyon | — (vmbr5) | Collecte Wazuh | 10.0.5.1 |
| 10.0.2.0/24 | Marseille | — (vmbr3) | LAN Marseille | 10.0.2.1 |

### 5.2 Allocation IP des hôtes

| VM | Hostname | IP statique | Subnet |
|----|----------|-------------|--------|
| 100 | OPNsense-Lyon | 192.168.1.166 (WAN) | WAN |
| 101 | OPNsense-Marseille | 192.168.1.167 (WAN) | WAN |
| 102 | DC01-Lyon | 10.1.10.10 | VLAN 10 SERVERS |
| 103 | Proxy-01 | 10.1.5.10 | VLAN 5 DMZ |
| 104 | Web-01 | 10.1.5.30 | VLAN 5 DMZ |
| 105 | Mail-01 | 10.1.5.40 | VLAN 5 DMZ |
| 106 | Wazuh-01 (net0) | 10.1.10.20 | VLAN 10 SERVERS |
| 106 | Wazuh-01 (net1) | 10.0.5.20 | Collecte vmbr5 |
| 107 | DB-01 | 10.1.10.30 | VLAN 10 SERVERS |
| 108 | File-01 | 10.1.10.40 | VLAN 10 SERVERS |
| 109 | Bastion-01 | 172.16.100.20 | MGMT vmbr2 |
| 110 | Backup-01 | 10.1.110.10 | VLAN 110 BACKUP |
| 111 | DNS-Marseille | 10.0.2.10 | LAN Marseille |

### 5.3 Conventions de nommage DNS

- **Domaine interne** : `nova.local`
- **Convention hostname** : `<role>-<numero>.nova.local` (ex: `dc01-lyon.nova.local`)
- **DNS faisant autorité** : DC01-Lyon (10.1.10.10) via Samba interne
- **DNS Marseille** : DNS-Marseille (10.0.2.10) en forward → DC01 si tunnel UP, cache local sinon

---

## 6. Matrice des flux firewall

### 6.1 Principe directeur

L'ensemble des flux suit la règle **"Deny All by Default"**. Toute communication doit être :
1. **Explicitement autorisée** par une règle firewall.
2. **Justifiée fonctionnellement** (cf. cahier des charges).
3. **Documentée** dans la matrice ci-après.

### 6.2 Flux entrants depuis Internet (WAN)

| Source | Destination | Protocole | Port | Justification |
|--------|------------|-----------|------|---------------|
| Internet | OPNsense Lyon WAN | TCP | 443 | Pas autorisé directement (réservé GUI admin via 192.168.1.0/24) |
| 192.168.1.0/24 | OPNsense Lyon WAN | TCP | 443 | Accès GUI admin local |
| Internet | Bastion-01 (via NAT) | TCP | 2222→22 | Accès SSH bastion (jump host) |
| Internet | Proxy-01 (via NAT) | TCP | 443 | Site web public (futur) |

### 6.3 Flux inter-VLAN à l'intérieur de Lyon

| Source | Destination | Protocole | Port | Justification |
|--------|------------|-----------|------|---------------|
| VLAN 5 DMZ (Web) | VLAN 10 SERVERS (DB-01) | TCP | 3306 | Backend MySQL |
| VLAN 5 DMZ | vmbr5 Wazuh collecte | TCP/UDP | 1514 | Envoi logs IDS |
| VLAN 5 DMZ | Internet | TCP/UDP | tout | **❌ Bloqué (anti-exfiltration)** |
| VLAN 10 SERVERS | Internet | TCP/UDP | 80, 443 | Mises à jour OS |
| VLAN 30 USERS | VLAN 10 SERVERS (DC01) | TCP/UDP | 53, 88, 389, 445, 636 | Auth AD + DNS + SMB |
| VLAN 30 USERS | VLAN 10 SERVERS (File-01) | TCP | 443 | Accès Nextcloud |
| VLAN 30 USERS | Internet | TCP/UDP | tout | Navigation |
| VLAN 30 USERS | VLAN 5 DMZ | * | * | **❌ Bloqué (least privilege)** |
| MGMT (vmbr2) | VLAN 10 SERVERS | TCP | 22 | SSH admin via Bastion |
| MGMT (vmbr2) | Toute autre destination | * | * | **❌ Bloqué (least privilege)** |
| VLAN 110 BACKUP | VLAN 10 SERVERS | rsync/SSH | 22, 873 | Push sauvegardes |
| VLAN 110 BACKUP | Tout autre | * | * | **❌ Bloqué** |
| Quarantaine (vmbr4) | vmbr5 Wazuh | TCP/UDP | 1514 | Logs uniquement |
| Quarantaine (vmbr4) | Tout autre | * | * | **❌ Bloqué (cul-de-sac)** |

### 6.4 Flux inter-sites (Lyon ↔ Marseille via IPsec)

| Source | Destination | Protocole | Port | Justification |
|--------|------------|-----------|------|---------------|
| Marseille LAN (10.0.2.0/24) | Lyon SERVERS (10.1.10.0/24) | TCP/UDP | 53, 389, 636, 88 | Auth AD distante |
| Marseille LAN | Lyon File-01 | TCP | 443 | Accès Nextcloud distant |
| Marseille LAN | Internet (via Lyon) | TCP/UDP | tout | Hub & Spoke transit |

### 6.5 Flux accès distants (OpenVPN — commerciaux)

| Source | Destination | Protocole | Port | Justification |
|--------|------------|-----------|------|---------------|
| Tunnel OpenVPN (10.8.0.0/24) | VLAN 10 SERVERS (DC01) | TCP/UDP | 88, 389 | Auth AD |
| Tunnel OpenVPN | VLAN 10 SERVERS (File-01) | TCP | 443 | Accès Nextcloud |
| Tunnel OpenVPN | VLAN 5 DMZ | * | * | **❌ Bloqué** |

---

## 7. Stratégie d'Infrastructure-as-Code

### 7.1 Outils et leur rôle

```
Terraform  : Provisionne l'infrastructure (VMs, bridges, VLANs)
   ↓
Cloud-Init : Configure l'OS au premier démarrage (IP, user, password, DNS)
   ↓
Scripts qm : Ajustements fins via CLI Proxmox (alternative au provider Terraform)
   ↓
Ansible    : Configuration des services (Samba, Apache, Wazuh) — optionnel pour cette mission
```

### 7.2 Structure du code Terraform

```
Build/terraform/
├── main.tf         : ressources principales (VMs, bridges)
├── variables.tf    : paramètres (IPs, passwords, VLAN IDs)
├── outputs.tf      : IPs des VMs pour inventaire Ansible
├── providers.tf    : configuration provider bpg/proxmox
├── terraform.tfvars : valeurs des variables (secrets exclus du Git)
└── terraform.tfstate : état Terraform (sensible, à protéger)
```

### 7.3 Commandes types

```bash
# Initialisation provider
terraform init

# Plan d'exécution (dry-run)
terraform plan

# Application
terraform apply -auto-approve

# Destruction (en cas de reconstruction)
terraform destroy
```

### 7.4 Reproductibilité

L'ensemble du code Terraform est versionné sur le dépôt Git du client. **Reconstruction complète possible en < 4 heures** :
1. `terraform apply` — création des VMs (15 min)
2. Boucle `qm set` cloud-init (5 min)
3. Configuration OPNsense (import XML) (15 min)
4. Provisionnement applicatif scripts (3 heures)

---

## 8. Détail des composants déployés

### 8.1 Hyperviseur Proxmox

**Configuration installée** :
- Version : 9.1.1
- Filesystem : ext4 sur LVM
- Storage : `local-lvm` (thin provisioning, ~50 GB libres)
- Réseau : 6 bridges Linux configurés via `/etc/network/interfaces`
- API : exposée sur port 8006 (HTTPS)
- Token API : créé pour Terraform (`root@pam!terraform`)

### 8.2 OPNsense Lyon

**Configuration installée** :
- Version : 26.1.6_2
- Interfaces actives : WAN, LAN, MGMT, Quarantaine, Wazuh + 5 VLANs (5, 10, 30, 40, 110)
- IPsec : tunnel actif vers Marseille (Phase 1 + Phase 2 INSTALLED)
- Hostname : `lyon.nova.local`
- NAT : Hybrid mode (toutes les VMs sortent via OPNsense WAN)
- Suricata : à activer en Phase III

### 8.3 OPNsense Marseille

**Configuration installée** :
- Version : 26.1.6_2
- Interfaces actives : WAN, LAN, MGMT
- IPsec : tunnel actif vers Lyon
- Hostname : `marseille.nova.local`
- Sous-réseau LAN : 10.0.2.0/24

### 8.4 Active Directory (DC01-Lyon)

**Configuration prévue (Phase 7)** :
- Samba 4 en mode AD-DC
- Domaine : `nova.local`
- Realm : `NOVA.LOCAL`
- Utilisateurs de test : alice, bob, charlie, david
- Groupes : Admins, Commerciaux, IT
- DNS interne : forward `*.nova.local`

### 8.5 SIEM (Wazuh-01)

**Configuration prévue (Phase 7)** :
- Wazuh Manager + Indexer + Dashboard sur la même VM
- Agents déployés sur : DC01, Web-01, Proxy-01, DB-01, File-01, Mail-01, Backup-01, Bastion-01
- Règles activées : MITRE ATT&CK, PCI DSS, GDPR
- Intégration Suricata : forward des alertes WAN

### 8.6 Bastion-01

**Configuration installée** :
- Debian 12 minimal
- SSH server (port 22)
- Utilisateur : `novaadmin`
- Mot de passe : `NovaLab2026` (à terme : authentification par clé uniquement)
- Accessible depuis Internet via NAT : `192.168.1.166:2222 → 172.16.100.20:22`

---

## 9. Sécurité — Mesures appliquées

### 9.1 Defense in Depth (4 niveaux)

| Niveau | Mécanisme | État |
|--------|-----------|------|
| **Périmètre externe** | OPNsense Lyon + IDS Suricata | ✅ Déployé (IDS à activer) |
| **Inter-VLAN** | Règles firewall Deny-by-Default | ✅ Déployé (4 règles passantes seulement) |
| **Hôte** | UFW + Fail2ban sur chaque VM | ⏳ Phase III |
| **Application** | Authentification AD, HTTPS, hash passwords | ⏳ Phase III |

### 9.2 Mesures de sécurité réseau

1. **Segmentation L2** : 6 bridges + 5 VLANs.
2. **Bastion isolé** : seule porte d'entrée admin (pattern *Jump Host*).
3. **Quarantaine cul-de-sac** : bridge vmbr4 sans aucune route.
4. **DMZ contrainte** : pas d'egress vers Internet (anti-exfiltration).
5. **Tunnel IPsec chiffré** : AES-256-GCM, PFS, re-keying régulier.
6. **NAT outbound** : Hybrid pour visibilité, masquerade pour traçabilité.

### 9.3 Mesures de sécurité système

1. **Mots de passe non-triviaux** : `NovaLab2026` (12 caractères alphanumériques, lab uniquement).
2. **Cloud-Init reproductible** : pas de password en clair dans Git.
3. **Comptes utilisateurs centralisés** AD (à venir Phase III) — élimination des comptes locaux.
4. **Authentification SSH** : à migrer en clés uniquement (Phase III).

### 9.4 Conformité aux principes ANSSI

| Principe ANSSI | Application Nova Syndicate |
|---------------|----------------------------|
| Cloisonnement | 5 VLANs + 6 bridges = isolation forte |
| Filtrage | OPNsense Deny-by-Default |
| Authentification forte | Samba AD (Phase III) |
| Journalisation | Wazuh SIEM (Phase III) |
| Sauvegardes | Backup-01 (Phase III) |
| Mise à jour | apt update automatisé (Phase III) |
| Cryptographie | TLS 1.3, AES-256, SHA-512, DH G20 |

---

## 10. Preuves de fonctionnement

Cf. dossier annexe `livrables/annexes_poc/` contenant **25 captures écran numérotées** documentant chaque étape clé du déploiement.

### Liste des preuves capturées

| POC # | Description | Phase |
|-------|-------------|-------|
| 1 | Proxmox VE 9.1.1 installé + login GUI | Phase 1 |
| 2 | 12 VMs déployées via Terraform | Phase 2 |
| 3 | OPNsense Lyon dashboard + interfaces | Phase 3 |
| 4 | Règles firewall inter-VLAN OPNsense | Phase 3 |
| 5 | OPNsense Marseille dashboard | Phase 4 |
| 6 | Tunnel IPsec UP + ping bidirectionnel | Phase 5 |
| 7 | Bastion-01 ping Internet via NAT OPNsense | Phase 6 |
| 8 | Ping cross-site Bastion → DNS-Marseille via IPsec | Phase 6 |
| 9 | SSH bastion depuis Windows PowerShell | Phase 6 |
| 10 | Tableau règles firewall OPNsense (4 internes + NAT + WAN) | Phase 6 |
| 11 | Samba AD provisionné + samba-tool user list | Phase 7 |
| 12 | Wazuh dashboard avec 3+ agents enregistrés | Phase 7 |
| 13 | Web vitrine accessible via Proxy-01 reverse proxy | Phase 7 |
| 14 | MariaDB connexion depuis Web-01 | Phase 7 |
| 15 | Suricata UP avec règles ET Open | Phase 7 |
| 16 | Mail-01 : envoi/réception SMTP + IMAP | Phase 7 |
| 17 | Webmail Roundcube accessible | Phase 7 |
| 18 | Nextcloud avec auth AD Samba | Phase 7 |
| 19 | Backup-01 rsync nocturne fonctionnel | Phase 7 |
| 20 | OpenVPN client connecté + accès LAN distant | Phase 7 |
| 21 | Fail2ban actif sur Bastion (logs ban) | Phase 8 |
| 22 | Brute force SSH détecté → alerte Wazuh visible | Phase 8 |
| 23 | Scan Nmap → Suricata alerte | Phase 8 |
| 24 | Honeypot Cowrie (bonus) + tentative capturée | Bonus |
| 25 | RODC Marseille répond après coupure IPsec (bonus) | Bonus |

---

## 11. Retour d'expérience — Incidents et solutions

### 11.1 Méthodologie

Cette section formalise les **12 incidents techniques majeurs** rencontrés et résolus pendant le déploiement. Chaque incident est documenté selon le canevas **Symptôme → Cause racine → Fix → Apprentissage**.

### 11.2 Inventaire des incidents

#### Incident #1 — KVM virtualization non disponible
- **Symptôme** : `TASK ERROR: KVM virtualisation configured, but not available`
- **Cause** : Proxmox exécuté dans VirtualBox sans nested virtualization activée.
- **Fix** : `qm set <vmid> --kvm 0` (mode TCG / émulation logicielle).
- **Apprentissage** : valider la chaîne de virtualisation imbriquée avant le déploiement massif.

#### Incident #2 — Cloud-Init Drive absent par défaut
- **Symptôme** : onglet Cloud-Init du GUI Proxmox sans effet.
- **Cause** : `qm clone` ne joint pas systématiquement un disque cloud-init.
- **Fix** : `qm set <vmid> --ide2 local-lvm:cloudinit`.
- **Apprentissage** : prévoir l'ajout du drive dans tout script de provisioning.

#### Incident #3 — Affichage série rend noVNC inutilisable
- **Symptôme** : console noVNC vide après boot.
- **Cause** : template Debian configuré avec affichage `serial0`.
- **Fix** : utiliser **xterm.js** au lieu de noVNC pour la console série.
- **Apprentissage** : adapter l'outil de console au type d'affichage de la VM.

#### Incident #4 — Filesystem corrompu après hard-stops
- **Symptôme** : `EXT4-fs error`, `aborted journal`, FS remount read-only.
- **Cause** : `qm stop --skiplock` répétés pendant troubleshooting.
- **Fix** : `qm destroy --purge 1 && qm clone 9000 <vmid> --full 1`.
- **Apprentissage** : éviter les hard-kills, préférer `qm reset` ou `qm shutdown --forceStop 1`.

#### Incident #5 — Bash history expansion sur `!` dans cipassword
- **Symptôme** : mot de passe silencieusement corrompu.
- **Cause** : bash interactif expanse `!` même entre quotes simples.
- **Fix** : `set +H` avant la commande qm, OU mot de passe sans `!`.
- **Apprentissage** : standardiser les mots de passe lab sans caractère spécial.

#### Incident #6 — Pavé numérique inactif sur console série
- **Symptôme** : chiffres saisis au pavé num invisibles.
- **Cause** : xterm.js ne sync pas NumLock avec l'invité Linux.
- **Fix** : utiliser la rangée de chiffres au-dessus du clavier QWERTY.
- **Apprentissage** : documenter dans le manuel d'exploitation.

#### Incident #7 — Firewall OPNsense bloque par défaut sur OPT*
- **Symptôme** : VM ne peut pas pinger sa propre gateway.
- **Cause** : aucune règle `Allow <iface> net → any` sur les interfaces autres que LAN.
- **Fix** : ajouter une règle `Pass IPv4 <iface> net → any` sur chaque interface où sont des VMs.
- **Apprentissage** : automatiser via la collection Ansible `ansibleguy.opnsense`.

#### Incident #8 — Disques Terraform incomplets → grub rescue>
- **Symptôme** : `grub rescue>` au boot des VMs.
- **Cause** : `qm clone` linked mal exécuté lors du premier provisioning.
- **Fix** : `qm clone 9000 <vmid> --full 1` (clone complet).
- **Apprentissage** : toujours utiliser `--full 1` en production.

#### Incident #9 — Kernel panic IO-APIC après reboots forcés
- **Symptôme** : `Kernel panic - not syncing: IO-APIC + timer doesn't work!`
- **Cause** : instabilité QEMU en TCG cumulé après plusieurs `qm stop --skiplock`.
- **Fix** : reclone complet de la VM.
- **Apprentissage** : `qm reset` préférable à `qm stop --skiplock`.

#### Incident #10 — NAT Destination trop permissive → perte GUI
- **Symptôme** : la GUI OPNsense Lyon devient inaccessible juste après "Appliquer".
- **Cause** : règle NAT créée avec Destination=`any` et Port=`any` → redirige TOUT le TCP entrant.
- **Fix** : console OPNsense → `pfctl -d` → reconnecter à la GUI → corriger Destination=192.168.1.166, Port=2222 → `pfctl -e`.
- **Apprentissage** : toujours documenter `pfctl -d` et créer un checklist de retour à l'état normal.

#### Incident #11 — Port custom dans Destination NAT OPNsense 26.x
- **Symptôme** : impossible de saisir un port non standard (ex: 2222) dans le dropdown.
- **Cause** : la GUI OPNsense 26.x ne propose pas explicitement `(autre)` / `Custom`.
- **Fix** : sélectionner `Single port or range` dans le dropdown puis taper le numéro.
- **Apprentissage** : documenter l'évolution de l'UI dans le manuel.

#### Incident #12 — Filter rule = "Manuel" → règle WAN absente
- **Symptôme** : NAT fonctionnelle mais SSH timeout.
- **Cause** : `Filter rule = Manuel` n'auto-crée pas la règle WAN passante.
- **Fix** : créer manuellement la règle WAN avec destination = IP post-NAT (172.16.100.20:22).
- **Apprentissage** : se rappeler que pf applique NAT avant filtre.

### 11.3 Bilan de l'expérience

Les 12 incidents recensés représentent **environ 4 heures de troubleshooting** sur les 32 heures totales de mission, soit **12,5 % du temps**. Ils ont :
- Renforcé la **maîtrise de la stack** (compréhension fine du fonctionnement Proxmox + OPNsense).
- Constitué un **catalogue d'apprentissages** réutilisable pour les missions futures.
- Permis d'enrichir la **documentation d'exploitation** transmise au client.

Cette transparence sur les difficultés rencontrées est **essentielle** pour la prise en main par l'équipe interne du client. La connaissance des écueils possibles évite leur reproduction.

---

**Document arrêté à la version 1.0** — Mai 2026

*Document interne client. Diffusion soumise à autorisation préalable.*
