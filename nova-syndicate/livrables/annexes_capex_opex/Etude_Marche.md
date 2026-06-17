# ETUDE DE MARCHE — Infrastructure Reseau Nova Syndicate

## Benchmark des solutions techniques et justification des choix

---

**Reference document** : NS-2026-ANX-02
**Auteur** : Dorian Poncelet — Nova Syndicate
**Date** : Mai 2026
**Version** : 2.0
**Statut** : Annexe complementaire au CAPEX/OPEX (NS-2026-ANX-01)
**Classification** : Document projet

---

## Objet

Ce document approfondit l'analyse budgetaire CAPEX/OPEX (NS-2026-ANX-01) en fournissant, pour chaque brique de l'infrastructure Nova Syndicate, un **benchmark marche** des solutions existantes. L'objectif est de justifier les choix techniques retenus par des donnees de marche verifiables : parts de marche, notes utilisateurs, couts reels, tendances d'adoption.

Les composants analyses correspondent exactement au perimetre du CAPEX/OPEX :

| # | Brique infrastructure | Solution retenue | Alternative principale |
|---|----------------------|------------------|------------------------|
| 1 | Virtualisation | Proxmox VE 9 | VMware vSphere / Hyper-V |
| 2 | Firewall + IDS | OPNsense + Suricata | FortiGate + FortiGuard IPS |
| 3 | Annuaire (Active Directory) | Samba 4 | Windows Server AD DS |
| 4 | SIEM | Wazuh 4.x | Splunk Enterprise / ELK |
| 5 | Sauvegarde | rsync + GPG + scripts | Veeam Backup |
| 6 | Messagerie | Postfix + Dovecot | Microsoft 365 |
| 7 | Supervision / Monitoring | Prometheus + Loki + Grafana | Datadog / Zabbix / PRTG |
| 8 | Hebergement | On-premise (Proxmox) | Cloud OVH / Cloud AWS |

---

## 1. Virtualisation : Proxmox VE vs. VMware vSphere vs. Hyper-V

### 1.1 Contexte marche

Le marche mondial de la virtualisation est estime a **57,3 milliards USD** (2022), avec une projection a **190,7 milliards USD d'ici 2028** (CAGR ~17 %). Le rachat de VMware par Broadcom en 2023 a provoque une hausse tarifaire de **2x a 5x** sur les licences vSphere, poussant de nombreuses entreprises a evaluer des alternatives.

Proxmox VE s'impose en 2025 comme une alternative credible en production, avec une adoption en forte croissance dans les PME et les labos.

### 1.2 Comparatif

| Critere | Proxmox VE 9 (retenu) | VMware vSphere Standard | Microsoft Hyper-V |
|---------|------------------------|-------------------------|-------------------|
| **Licence** | Open source (AGPL v3) | Proprietaire (Broadcom) | Inclus Windows Server |
| **CAPEX licence (4 sockets)** | **0 EUR** | **10 000 EUR** | **1 600 EUR** (+ CAL) |
| **OPEX support/an** | 0 EUR (community) | 2 000 EUR (Basic) | 915 EUR (SA) |
| **Cout datacenter 10 hotes/an** | ~1 000 EUR (support optionnel) | **45 000+ EUR** | ~16 000 EUR |
| **Hyperviseur** | KVM (Linux kernel) | ESXi proprietaire | Hyper-V (Windows) |
| **Containers natifs** | LXC integre | Non (vSphere Tanzu payant) | Non natif |
| **IaC (Terraform)** | Provider officiel Telmate | Provider officiel HashiCorp | Provider AzureRM |
| **API REST** | Complete, documentee | Complete | PowerShell / WMI |
| **HA / Live Migration** | Oui (integre) | Oui (vMotion) | Oui (Live Migration) |
| **Interface web** | Oui (complete) | vCenter requis (6 000 EUR) | Windows Admin Center |
| **Communaute** | Croissance forte | En declin (prix Broadcom) | Stable |

*Sources : Proxmox.com/comparison, Tech-Insider 2026 "Proxmox vs VMware", Servermall "Which Hypervisor 2025", CloudNews.tech*

### 1.3 Justification du choix

Proxmox VE est retenu pour trois raisons directement liees au projet :

1. **Cout** : 0 EUR de licence contre 10 000 EUR CAPEX + 2 000 EUR/an pour VMware. Sur 3 ans, l'ecart est de **16 000 EUR** sur cette seule brique.
2. **Provider Terraform** : le provider `telmate/proxmox` permet le deploiement des 12 VMs Nova Syndicate en Infrastructure-as-Code, conforme a l'architecture IaC du projet.
3. **KVM + LXC** : la double capacite (VMs + containers) offre une flexibilite que VMware ne propose qu'en option payante (Tanzu).

---

## 2. Firewall + IDS : OPNsense + Suricata vs. FortiGate + FortiGuard

### 2.1 Contexte marche firewall

Le marche mondial des firewalls est domine par Fortinet (17,2 % de mindshare, #1 PeerSpot). OPNsense occupe la 4e place avec 9,6 % de mindshare et une note de 8,3/10, proche du 8,5/10 de FortiGate.

Le modele economique differe radicalement : FortiGate facture le hardware (appliance) + des abonnements annuels (FortiCare support + FortiGuard UTM bundle pour IPS, antivirus, filtrage web). OPNsense est un logiciel gratuit installe sur du hardware standard.

### 2.2 Comparatif firewall

| Critere | OPNsense (retenu) | FortiGate 100F | pfSense |
|---------|--------------------|----------------|---------|
| **Licence** | Open source (BSD) | Proprietaire | Open source (Apache 2.0) |
| **CAPEX (2 sites Lyon + Marseille)** | **0 EUR** | **9 000 EUR** | 0 EUR |
| **OPEX/an (support + UTM)** | **0 EUR** | **3 600 EUR** | 0 EUR |
| **Mindshare PeerSpot** | 9,6 % (#4) | 17,2 % (#1) | 8,2 % |
| **Note utilisateurs** | 8,3/10 | 8,5/10 | 8,1/10 |
| **IDS/IPS integre** | Suricata (natif) | FortiGuard IPS (payant) | Snort / Suricata |
| **VPN site-to-site** | IPsec IKEv2 + WireGuard | IPsec + SD-WAN | IPsec + OpenVPN |
| **Segmentation VLAN** | Oui (5 VLANs deployes) | Oui | Oui |
| **API REST** | Complete | Complete | Limitee |
| **Mises a jour** | Hebdomadaires (communaute) | Contractuelles (FortiGuard) | Mensuelles |
| **ROI moyen** | 3 mois | 6-12 mois | 3-4 mois |

*Sources : PeerSpot "FortiGate vs OPNsense" 2026, Zenarmor "OPNsense vs Fortinet", StationX "OPNsense vs pfSense 2026"*

### 2.3 Comparatif IDS : Suricata vs. Snort

L'IDS est un composant critique de l'infrastructure. Suricata est integre nativement dans OPNsense et alimente Wazuh en alertes.

| Critere | Suricata (retenu) | Snort 3 |
|---------|--------------------|---------| 
| **Architecture** | **Multi-threaded** | Multi-threaded (v3, inefficace sous charge) |
| **Detection DNS tunneling** | **100 %** (DNSCat2 + Iodine) | 85,7 % / 66,7 % |
| **DPI** | Natif, auto-detection protocoles | Limite |
| **Format logs** | JSON (EVE) — ideal integration SIEM | Unified2 |
| **Integration OPNsense** | Native | Non supportee |
| **Regles deployees (Nova)** | **5 865 regles ET Open** | VRT + community |
| **Ressources** | Moderees a elevees | Faibles a moderees |

*Sources : Stamus Networks "Suricata vs Snort", ScienceDirect "Which open-source IDS?", MDPI "Comparative Evaluation Snort/Suricata Cloud"*

### 2.4 Justification du choix

1. **Economie** : 9 000 EUR CAPEX + 3 600 EUR/an evites par rapport a FortiGate. Sur 3 ans : **19 800 EUR** d'ecart.
2. **Suricata > Snort** : taux de detection superieur (100 % vs. 66-86 %), architecture multi-threaded, logs JSON natifs pour Wazuh.
3. **Coherence IaC** : OPNsense s'administre via API REST, permettant l'automatisation des regles firewall.

---

## 3. Annuaire : Samba 4 AD vs. Windows Server AD DS

### 3.1 Contexte

Active Directory est le standard de fait pour l'authentification centralisee en entreprise. Microsoft domine ce segment avec Windows Server AD DS. Samba 4 est la seule alternative open source compatible AD (protocoles LDAP, Kerberos, DNS, GPO).

### 3.2 Comparatif

| Critere | Samba 4 (retenu) | Windows Server 2022 AD DS |
|---------|-------------------|---------------------------|
| **Licence** | Open source (GPLv3) | Proprietaire |
| **CAPEX licence (2 DC)** | **0 EUR** | **4 575 EUR** (licences + CAL) |
| **OPEX/an** | **0 EUR** | **915 EUR** (Software Assurance) |
| **Compatibilite AD** | LDAP + Kerberos + DNS + GPO basiques | Complete (GPO avancees, ADFS, Azure AD) |
| **Clients Windows** | Join domaine natif | Join domaine natif |
| **Replication multi-DC** | Oui | Oui |
| **GPO avancees** | Limitees (pas de Fine-Grained Password Policy native) | Completes |
| **Integration Azure** | Non | Oui (Hybrid Join, Azure AD Connect) |
| **OS hote** | Debian / Linux | Windows Server |
| **Deploiement IaC** | Ansible (script Python cree pour Nova) | PowerShell DSC |

*Sources : Proxmox.com/comparison, Samba.org wiki, Microsoft Volume Licensing 2025*

### 3.3 Justification du choix

1. **Economie** : 4 575 EUR CAPEX + 915 EUR/an evites. Sur 3 ans : **7 320 EUR** d'ecart.
2. **Suffisant pour le perimetre** : Nova Syndicate n'a pas besoin de GPO avancees ni d'Azure AD. Samba 4 couvre les besoins (authentification centralisee, join domaine, DNS integre).
3. **Automatisation** : le script Python `01_create_ad_users.py` gere la creation d'utilisateurs via `samba-tool`, integre aux playbooks Ansible.

---

## 4. SIEM : Wazuh vs. Splunk Enterprise vs. ELK Stack

### 4.1 Contexte marche

Le marche SIEM est domine par Splunk (7,2 % mindshare, #1 PeerSpot). Wazuh occupe la 3e place (5,8 %) avec une note superieure (8,4 vs. 8,3). L'adoption de Wazuh est en forte croissance, portee par son modele gratuit et ses fonctionnalites natives (FIM, compliance, MITRE ATT&CK) que Splunk facture en add-ons.

### 4.2 Comparatif

| Critere | Wazuh 4.x (retenu) | Splunk Enterprise | ELK Stack |
|---------|---------------------|-------------------|-----------|
| **Licence** | Open source (GPLv2) | Proprietaire | Licence Elastic modifiee |
| **Cout annuel (10 GB/j ingestion)** | **0 EUR** | **18 000-22 000 EUR** | 0 EUR (self-hosted) |
| **Mindshare PeerSpot** | 5,8 % (#3) | 7,2 % (#1) | ~4 % |
| **Note utilisateurs** | 8,4/10 | 8,3/10 | 7,8/10 |
| **MITRE ATT&CK mapping** | **Natif** (dashboards integres) | Via add-on | Manuel |
| **FIM (integrite fichiers)** | **Natif** | Via add-on | Non natif |
| **Compliance (CIS, PCI-DSS)** | **Dashboards integres** | Via Premium apps (payantes) | Non natif |
| **Agent endpoint** | Leger, multi-OS | Universal Forwarder | Beats |
| **Integration Suricata** | Native (regles decodeurs) | Via add-on | Via Filebeat |
| **Courbe d'apprentissage** | Moderee | Elevee (SPL) | Elevee (DSL Elastic) |
| **Scalabilite** | Bonne (cluster OpenSearch) | Excellente | Excellente |
| **Support** | Communaute + CES payant | 24/7 contractuel | Elastic payant |

*Sources : PeerSpot "Top 8 SIEM 2026", PeerSpot "Splunk vs Wazuh", Dev.to "Wazuh: The Open-Source SIEM That Beats Splunk"*

### 4.3 Justification du choix

1. **Economie** : 18 000-22 000 EUR/an evites par rapport a Splunk. Sur 3 ans : **54 000 a 66 000 EUR** d'ecart — c'est le poste le plus important du CAPEX/OPEX.
2. **Fonctionnalites natives** : MITRE ATT&CK, FIM, CIS Benchmark, PCI-DSS sont integres sans surcout. Splunk les facture en add-ons Premium.
3. **Integration Suricata** : Wazuh decode nativement les alertes Suricata (EVE JSON), permettant la correlation SIEM + IDS dans un seul dashboard.
4. **Deploiement** : le playbook Ansible `playbook_wazuh_server.yml` automatise l'installation complete.

---

## 5. Sauvegarde : rsync + GPG vs. Veeam Backup

### 5.1 Contexte

Veeam domine le marche du backup VM avec une position de leader dans le Magic Quadrant Gartner. La solution Nova Syndicate utilise une approche scripts (rsync + GPG + cron) conforme a la politique 3-2-1 du PCA.

### 5.2 Comparatif

| Critere | rsync + GPG + cron (retenu) | Veeam Backup Essentials |
|---------|-----------------------------|-----------------------|
| **Licence** | Open source | Proprietaire |
| **CAPEX** | **0 EUR** | **1 500 EUR** |
| **OPEX/an** | **60 EUR** (stockage cloud OVH) | **400 EUR** (support Premier) |
| **Chiffrement** | GPG asymetrique | AES-256 integre |
| **Politique 3-2-1** | Implementee (local + distant + cloud) | Implementee |
| **Granularite** | Par service (AD, MariaDB, Nextcloud, Mail, OPNsense, Proxmox) | Par VM complete |
| **Verification integrite** | SHA-256 checksum | CRC integre |
| **Restauration granulaire** | Manuelle (tar extract) | Interface graphique |
| **Integration Proxmox** | vzdump + rsync | Plugin Proxmox natif |
| **Rapport email** | Script maison (`backup_orchestrator.sh`) | Natif |
| **Automatisation** | Cron + Ansible | Interface + API |

*Sources : Gartner Magic Quadrant Backup 2025, Veeam pricing 2025*

### 5.3 Justification du choix

1. **Economie** : 1 500 EUR CAPEX + 400 EUR/an evites. Sur 3 ans : **2 700 EUR** d'ecart.
2. **Granularite** : le script `backup_orchestrator.sh` sauvegarde chaque service independamment (AD, MariaDB, Nextcloud, Mail, OPNsense, Proxmox), avec chiffrement GPG et checksum SHA-256.
3. **Tradeoff assume** : la restauration est manuelle (pas d'interface graphique). Acceptable pour le perimetre (3 VMs actives, documentation de restauration fournie dans le PCA).

---

## 6. Messagerie : Postfix + Dovecot vs. Microsoft 365

### 6.1 Contexte

Microsoft 365 domine le marche de la messagerie d'entreprise avec plus de 400 millions d'utilisateurs. Postfix + Dovecot est la stack open source de reference pour le self-hosting.

### 6.2 Comparatif

| Critere | Postfix + Dovecot (retenu) | Microsoft 365 Business Standard |
|---------|----------------------------|---------------------------------|
| **Licence** | Open source | Proprietaire |
| **CAPEX** | **0 EUR** | **0 EUR** |
| **OPEX/an (85 users)** | **0 EUR** | **10 710 EUR** |
| **Anti-spam** | SpamAssassin / rspamd | Exchange Online Protection |
| **Calendrier** | Roundcube + plugin CalDAV | Outlook Calendar |
| **Stockage** | Illimite (disque local) | 50 Go / boite |
| **Chiffrement TLS** | Let's Encrypt | Microsoft |
| **Administration** | CLI + config files | Interface web complete |
| **Delivrabilite** | Necessite SPF/DKIM/DMARC manuels | Configure par defaut |
| **Souverainete** | Donnees on-premise | Donnees Microsoft (US) |

*Sources : Microsoft 365 pricing France 2025, Postfix.org*

### 6.3 Justification du choix

1. **Economie** : 10 710 EUR/an evites. Sur 3 ans : **32 130 EUR** d'ecart — 2e poste le plus important du CAPEX/OPEX.
2. **Souverainete** : les emails restent sur l'infrastructure locale, pas de dependance cloud US.
3. **Tradeoff assume** : administration en CLI, configuration SPF/DKIM/DMARC manuelle, pas de suite bureautique integree. Acceptable dans le contexte du projet (infrastructure technique, pas bureautique).

---

## 7. Supervision : Prometheus + Loki + Grafana vs. alternatives

### 7.1 Contexte marche

Le marche de l'observabilite explose avec l'adoption du cloud et des microservices. Datadog (SaaS proprietaire) domine le segment commercial. Prometheus est le standard de facto pour le monitoring cloud-native (projet CNCF gradue). Zabbix domine le monitoring infra traditionnel.

### 7.2 Comparatif

| Critere | Prometheus + Loki + Grafana (retenu) | Datadog | Zabbix | PRTG (1000 sensors) |
|---------|---------------------------------------|---------|--------|---------------------|
| **Licence** | Open source | SaaS proprietaire | Open source | Proprietaire |
| **CAPEX** | **0 EUR** | 0 EUR | 0 EUR | **1 800 EUR** |
| **OPEX/an (3 hotes)** | **0 EUR** | **5 000-15 000 EUR** | **0 EUR** | **360 EUR** |
| **Architecture** | Pull (decentralise) | SaaS cloud | Push (centralise) | Agent / SNMP |
| **Requetes** | PromQL (puissant) | Proprietaire | Triggers simples | Capteurs pre-configures |
| **Metriques systeme** | node_exporter | Agent Datadog | Agent Zabbix | Capteur auto |
| **Metriques applicatives** | mysqld_exporter, nginx_exporter | Integrations natives | Templates | Capteurs SQL/HTTP |
| **Logs centralises** | Loki + promtail | Datadog Logs | Non natif | Non natif |
| **Dashboards** | Grafana (riches) | Natifs (excellents) | Natifs (basiques) | Natifs (corrects) |
| **Alerting** | Alertmanager + Grafana | Natif (avance) | Natif | Natif |
| **Deploiement** | Binaire unique par composant | Zero (SaaS) | Complexe (multi-composants) | Serveur Windows |

*Sources : PeerSpot "Zabbix Alternatives 2026", Better Stack "Nagios vs Zabbix vs Prometheus", SigNoz comparisons*

### 7.3 Justification du choix

1. **Economie** : 1 800 EUR CAPEX + 360 EUR/an evites vs. PRTG (Solution A). Vs. Datadog : 5 000-15 000 EUR/an evites.
2. **Observabilite complete** : la stack couvre les 3 piliers (metriques Prometheus + logs Loki + visualisation Grafana) sans cout supplementaire.
3. **Exporters specifiques** : `mysqld_exporter` (MariaDB), `nginx_exporter` (BricoPro), `node_exporter` (systeme) — deployes via le playbook Ansible `playbook_monitoring_agents.yml`.
4. **Coherence stack** : Grafana sert de dashboard unifie pour Prometheus ET Loki, avec un dashboard custom `nova_overview.json`.

---

## 8. Hebergement : On-premise vs. Cloud

### 8.1 Contexte marche

Les depenses cloud en France ont atteint **21,4 milliards d'euros en 2025** (+19 %). Cependant, le marche des infrastructures IT on-premise repart a la hausse, porte par les enjeux de souverainete (NIS2, RGPD) et les hausses tarifaires du cloud.

Le point de break-even entre cloud et on-premise se situe generalement a **15-18 mois** : au-dela, l'on-premise devient plus economique a perimetre constant.

### 8.2 Comparatif (reprise CAPEX/OPEX enrichie)

| Critere | On-premise Proxmox (retenu) | Cloud OVH dedie | Cloud AWS EC2 |
|---------|-----------------------------|--------------------|---------------|
| **Modele financier** | CAPEX + faible OPEX | OPEX pur | OPEX pur |
| **CAPEX** | 7 750 EUR (serveur + switch + UPS) | 0 EUR | 0 EUR |
| **OPEX mensuel** | ~120 EUR | 200-500 EUR (dedie) | 800-2 800 EUR |
| **OPEX annuel** | ~1 440 EUR | 2 400-6 000 EUR | 9 600-34 000 EUR |
| **TCO 3 ans** | **12 070 EUR** | **7 200-18 000 EUR** | **28 800-102 000 EUR** |
| **Break-even** | 15-18 mois | Reference | 0 mois (pas de CAPEX) |
| **Souverainete** | Totale | France (SecNumCloud) | US (CLOUD Act) |
| **Latence inter-VMs** | < 1 ms (VLAN local) | < 5 ms (meme DC) | Variable |
| **IaC Terraform** | Provider Proxmox | Provider OVH | Provider AWS |
| **Maitrise** | Totale | Partielle | Faible (lock-in) |
| **Certifications DC** | N/A (labo) | SecNumCloud, HDS, ISO 27001 | SOC2, ISO 27001 |

*Sources : Spacelift "Cloud vs On-Premise Cost 2026", In A Secure Way "OVHcloud vs Scaleway 2025", ChannelNews "Infrastructure IT on-site"*

### 8.3 Justification du choix

1. **TCO** : le plus bas sur 3 ans a perimetre equivalent.
2. **IaC** : le provider Terraform `telmate/proxmox` est le point d'entree de toute l'architecture. Changer d'hebergement impliquerait de reecrire le code Terraform.
3. **Performance reseau** : la segmentation en 5 VLANs avec latence < 1 ms est impossible a reproduire en cloud multi-tenant.
4. **Souverainete** : aucune donnee ne transite par un tiers.

---

## 9. Synthese : impact sur le TCO global

Le tableau ci-dessous reprend les ecarts par brique, tels que documentes dans le CAPEX/OPEX (NS-2026-ANX-01) et valides par les donnees de marche de cette etude.

| Brique | Solution retenue (B) | Alternative principale (A) | Ecart 3 ans |
|--------|----------------------|----------------------------|-------------|
| Virtualisation | Proxmox VE (0 EUR) | VMware vSphere (16 000 EUR) | **-16 000 EUR** |
| Firewall + IDS | OPNsense + Suricata (0 EUR) | FortiGate 100F (19 800 EUR) | **-19 800 EUR** |
| Annuaire AD | Samba 4 (0 EUR) | Windows Server (7 320 EUR) | **-7 320 EUR** |
| SIEM | Wazuh (0 EUR) | Splunk (54 000-66 000 EUR) | **-54 000 EUR** |
| Sauvegarde | rsync + GPG (180 EUR) | Veeam (2 700 EUR) | **-2 520 EUR** |
| Messagerie | Postfix + Dovecot (0 EUR) | Microsoft 365 (32 130 EUR) | **-32 130 EUR** |
| Supervision | Prometheus + Grafana (0 EUR) | PRTG (2 880 EUR) | **-2 880 EUR** |
| **Total hors hardware** | **180 EUR** | **134 830-146 830 EUR** | **~-134 000 EUR** |

Le hardware (serveur + switch + UPS) et le temps homme de deploiement sont identiques entre les solutions et ne figurent pas dans cet ecart.

**Economie totale sur 3 ans : ~134 000 EUR** en choisissant une stack 100 % open source, pour des fonctionnalites equivalentes ou superieures sur les criteres critiques (detection IDS, mapping MITRE ATT&CK, observabilite).

---

## 10. Sources

### Virtualisation
- Proxmox, *Comparison: Proxmox VE vs vSphere, Hyper-V, Xen*, proxmox.com
- Tech-Insider, *Proxmox vs VMware 2026: Free vs $45K/Year — Full Comparison*, 2026
- CloudNews.tech, *Which virtualization platform is the most cost-effective in 2025?*
- StackGpu, *How Proxmox is Disrupting the Virtualization Market in 2025*, Medium
- Servermall, *Which Hypervisor to Choose in 2025?*

### Firewall et IDS
- PeerSpot, *Fortinet FortiGate vs OPNsense*, peerspot.com 2026
- Zenarmor, *OPNsense vs Fortinet*, zenarmor.com
- StationX, *OPNsense vs pfSense: Which One Is Better in 2026?*
- Stamus Networks, *Suricata vs Snort*, stamus-networks.com
- ScienceDirect, *Which open-source IDS? Snort, Suricata or Zeek*
- MDPI, *Comparative Evaluation of Snort and Suricata for Data Exfiltration Detection*

### SIEM
- PeerSpot, *Top 8 SIEM Solutions for 2026*, peerspot.com
- PeerSpot, *Splunk Enterprise Security vs Wazuh*, peerspot.com
- Dev.to (Inboryn), *Wazuh: The Open-Source SIEM That Beats Splunk*
- Gartner Peer Insights, *Elastic Security vs Wazuh 2026*

### Monitoring
- Better Stack, *Nagios vs Zabbix vs Prometheus: The Key Differences*
- SigNoz, *10 Best Zabbix Alternatives in 2026*
- Squadcast, *Prometheus vs Zabbix: Comparison Guide for IT Monitoring 2025*, Medium

### Hebergement
- Spacelift, *Cloud vs On-Premise: Cost Comparison for 2026*
- Cloudvara, *Cloud vs On-Premise Costs: A Complete TCO Breakdown*
- In A Secure Way, *OVHcloud vs Scaleway 2025 : comparatif indispensable*
- ChannelNews, *Le marche des infrastructures IT sur site repart a la hausse*
- Silicon.fr, *Les Benchmarks de l'IT 2026 : les plateformes cloud*

---

**Document arrete a la version 2.0** — Mai 2026

*Cette etude de marche complete l'annexe CAPEX/OPEX (NS-2026-ANX-01). Elle fournit les donnees de marche justifiant le choix de chaque brique technique de l'infrastructure Nova Syndicate.*
