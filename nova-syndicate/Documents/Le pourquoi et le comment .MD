Tu dois présenter cela à un jury. Faisons-le proprement. Je vais structurer comme une vraie présentation professionnelle.

DÉCISIONS ARCHITECTURALES — Nova Syndicate
PARTIE 1 : HYPERVISEUR (Proxmox)
❓ Question : Pourquoi Proxmox et pas GNS3 / ESXi / Hyper-V ?
1. GNS3 (ce qu'on a rejeté)
GNS3 = Simulateur réseau, pas vrai hyperviseur

Aspect	GNS3	Proxmox
Architecture	Simulation logicielle des routeurs/switches	Hyperviseur production-grade
Persistance réseau	⚠️ Fragile (bugs DNS, DHCP)	✅ Linux native, stable
Images VMs	Images Cisco/Juniper (limitées)	N'importe quelle distro Linux/Windows
Scalabilité	Max 50-100 VMs (limité CPU host)	Jusqu'à 1000+ VMs (limité RAM)
IaC support	❌ Aucun provider Terraform	✅ Provider bpg/proxmox
Réalisme soutenance	"J'ai simulé une infra"	"J'ai déployé une vraie infra"
Decision impact :

✅ Terraform peut provisioner directement Proxmox
✅ Chaque VM est un vrai système Debian (pas simulé)
✅ Possible d'ajouter Kubernetes, Docker, etc. plus tard (contrairement à GNS3)
2. ESXi / Hyper-V (pourquoi pas non plus)
Critère	ESXi	Hyper-V	Proxmox
Licence	Propriétaire VMware ($)	Inclus Windows Server	Open Source ✅
Sur Windows 11	Faut VM imbriquée	Faut VM imbriquée	Faut VM imbriquée
Terraform provider	✅ vmware/vsphere	✅ hashicorp/hyperv	✅ bpg/proxmox
Courbe d'apprentissage	Très abrupte (ESXI)	Moyenne (Hyper-V)	Douce (KVM + Linux)
Justifiable étudiant	"Je ne paye pas la licence"	"C'est pour mes prods Microsoft"	"C'est libre, stable, production-ready"
Decision impact :

✅ Réalisme : Proxmox est vraiment utilisé en production (Hetzner, OVH, etc.)
✅ Pédagogie : Tu apprendras KVM + Linux = plus transférable que "how to click in vSphere"
✅ Coût : Zéro (open source)
→ CONCLUSION : Proxmox = meilleur compromis réalisme + apprentissage + automatisation

📐 Architecture Proxmox pour Nova Syndicate
┌─────────────────────────────────────────────────────────┐
│        Windows 11 (Host) — 32 GB RAM                    │
├─────────────────────────────────────────────────────────┤
│  VirtualBox (Hyperviseur L1 — nested virt)              │
│  ┌───────────────────────────────────────────────┐      │
│  │ Proxmox VE 8 (20 GB RAM + 150 GB disk)        │      │
│  │ ┌─────────────────────────────────────────┐   │      │
│  │ │ 6 Linux Bridges (vmbr0-5) — pas de      │   │      │
│  │ │ switches physiques                      │   │      │
│  │ │                                         │   │      │
│  │ │ vmbr0 (WAN) → OPNsense-Lyon eth0       │   │      │
│  │ │ vmbr1 (LAN-aware) → Lyon VLANs 5,10… │   │      │
│  │ │ vmbr2 (isolé) → Bastion-01             │   │      │
│  │ │ vmbr3 (LAN-aware) → Marseille VLAN     │   │      │
│  │ │ vmbr4 (isolé) → Quarantaine            │   │      │
│  │ │ vmbr5 (collecte) → Wazuh-01 logs       │   │      │
│  │ │                                         │   │      │
│  │ │ [12 VMs Linux]                          │   │      │
│  │ └─────────────────────────────────────────┘   │      │
│  └───────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
Avantage du design :

Pas de switch physique = tout est logiciel (VLAN-aware bridges)
Deterministic = même setup peut être reproduit sur n'importe quel Proxmox
Scalable = ajouter une VM = 10 lignes Terraform
PARTIE 2 : IaC — Terraform
❓ Question : Pourquoi Terraform et pas Ansible seul ?
Analogie :

Terraform = "comment créer l'infrastructure (VMs, disques, bridges)"
Ansible = "comment configurer ce qui existe déjà (OS, services)"
Sequence logique :

1. Terraform : "crée-moi 12 VMs avec ces interfaces réseau"
   ↓
2. Ansible  : "configure ces 12 VMs avec ces services"
Tu ne peux pas faire step 2 avant step 1.

Outil	Scope	État
Terraform	Infrastructure (VMs, disques, réseau, tags)	Vérifié (idempotent)
Ansible	Configuration (OS, services, users, packages)	Vérifié (idempotent)
Helm (optionnel)	Applications (Kubernetes, charts)	Non applicable ici
Decision : Utiliser les deux en séquence

terraform apply → create infra
           ↓
ansible-playbook → configure services
           ↓
manual testing → verify matrice firewall
Provider Terraform : bpg/proxmox (communautaire, pas officiel)
❓ Pourquoi pas le provider officiel Proxmox ?
Truth : Il n'existe pas officiellement. Les options :

bpg/proxmox (communautaire) ✅ NOTRE CHOIX
Maintenu activement
Supporte VMs, disques, bridges, VLANs
Utilisé par beaucoup d'entreprises
Créer à la main (pas d'IaC)
Via UI Proxmox web
Aucune reproductibilité
Cauchemar pour soutenance ("montre le code, pas des clicks")
Decision impact :

✅ Tout est versionné dans Git
✅ "J'ai créé 12 VMs en exécutant un fichier .tf"
✅ Possible de tout détruire et recréer en 10 min
PARTIE 3 : Configuration — Ansible
❓ Question : Pourquoi Ansible et pas Puppet / Chef / SaltStack ?
Aspect	Ansible	Puppet	Chef	SaltStack
Agent requis	❌ Non (SSH)	✅ Oui	✅ Oui	✅ Oui
Language	YAML simple	Ruby DSL	Ruby DSL	Python YAML
Courbe apprentissage	⭐ Douce	⭐⭐⭐ Raide	⭐⭐⭐ Raide	⭐⭐ Moyenne
Scalabilité	<100 hosts (OK)	1000+	1000+	1000+
Idempotence	✅ Par défaut	✅	✅	✅
Communauté Linux	Très large	Déclinante	Entreprises	Petite
Decision : Ansible

Tu apprendras YAML (universel, pas spécifique à Ansible)
SSH existe partout = zéro agent à installer
Perfect pour <100 nodes (on a 12)
Communauté super active
Collections Ansible requises
# Collection 1: ansibleguy.opnsense
# ├─ Configure OPNsense via API REST
# ├─ VLANs, firewall rules, IPsec
# └─ Pourquoi ? : Terraform crée OPNsense, mais pas ses configs → Ansible

# Collection 2: community.general
# ├─ Rôles transversaux (sudo, users, cron)
# └─ Utilisé par 90% des playbooks Ansible

# Collection 3: ansible.posix
# ├─ Linux-specific (firewall UFW, systemd)
# └─ Standard pour Debian/RHEL
Sequence :

terraform apply
    ↓
ansible -m ping all       # Test connectivité
    ↓
ansible-playbook hardening.yml     # Common security
    ↓
ansible-playbook samba_ad.yml      # Active Directory
    ↓
ansible-playbook services.yml      # Web, DB, Nextcloud
    ↓
ansible-playbook opnsense.yml      # Firewall rules
PARTIE 4 : Firewall — OPNsense (pas pfSense)
❓ Question : OPNsense vs pfSense ?
Aspect	OPNsense	pfSense
Origine	Fork open source de pfSense (2015)	Propriétaire (Netgate inc.)
Licence	BSD 2-clause ✅	Propriétaire + restrictions
API REST	Native + docs ✅	Undocumented (reverse-engineered)
Ansible support	ansibleguy.opnsense ✅	Aucune collection officielle
Suricata IDS	Intégré + configurable ✅	Intégré mais limité
Cost	Libre	Libre (but restrictions sur mises à jour)
Production use	OVH, Hetzner, etc.	Petites infras, fournisseurs ISP
Decision : OPNsense

✅ API REST documentée = idéal pour Ansible
✅ Vraiment open source (pas de restrictions de licence)
✅ Suricata intégré = IDS out-of-the-box
✅ "OPNsense est plus moderne que pfSense"
Architecture Firewall — Security by Design
                    ┌──────────────┐
                    │   Internet   │
                    └──────────────┘
                          ↓ (vmbr0)
                    ┌──────────────┐
            DENY    │ OPNsense-    │      ALLOW TCP 80/443
            ALL ←──→│ Lyon (Hub)   │←──→  to DMZ only
            by      │              │
            default │ ┌─ vmbr1     │
                    │ ├─ vmbr2     │
                    │ ├─ vmbr4     │
                    │ └─ vmbr5     │
                    └──────────────┘
                        ↓↓↓↓↓↓
    ┌───────────┬───────────┬───────────┬──────────┐
    ↓           ↓           ↓           ↓          ↓
[DMZ]      [SERVERS]   [MGMT]      [BACKUP]   [QUARANTINE]
Pub web    AD, DB       Bastion      Backup      Honeypot
Proxy      Nextcloud                            (cul-de-sac)
Honeypot   Wazuh
Principes appliqués :

Deny All by Default : chaque flux doit être explicitement autorisé
Least Privilege : DMZ ne peut pas accéder USERS VLAN
Segmentation : 5 zones isolées avec des regles strictes
Zero Trust : même intra-réseau, tout est filtré
Why matrice firewall = proof of security :

✅ WAN → DMZ 80/443 : clients externes peuvent accéder au web
❌ WAN → SERVERS : personne de l'internet ne peut atteindre AD/DB
❌ DMZ → Internet : pas d'exfiltration de data depuis la DMZ
❌ USERS → MGMT : utilisateurs ne peuvent pas SSH au Bastion
❌ QUARANTINE → * : machine compromise est totalement isolée
PARTIE 5 : Architecture Multi-Site — IPsec
❓ Question : Pourquoi IPsec et pas OpenVPN / Wireguard ?
Aspect	IPsec	OpenVPN	Wireguard
Standard	RFC 7539 (30 ans) ✅	OpenVPN Inc. (propriétaire)	Crypto-focused (nouveau)
Routing Site-to-Site	Native L3 ✅	Via plugins	Native L3 ✅
OPNsense support	API ✅	GUI manual	Partial
Performance	Hardware acceleration possible	Software only	Ultra-fast but new
Production firewall	Standard de l'industrie ✅	Remote access VPN	Edges/clouds
Decision : IPsec

✅ C'est LE standard pour firewall-to-firewall (site-to-site)
✅ OPNsense supporte nativement (IKEv2)
✅ Conforme RFC = "c'est un standard, pas une bidouille"
Hub & Spoke topology :

                OPNsense-Lyon (Hub)
                      ↑
                      │ IPsec IKEv2
                      │ Tunnel UP
                      ↓
              OPNsense-Marseille (Spoke)
              
Conséquence :
- Marseille : tout trafic internet via Lyon (Hub)
- Lyon : point d'entrée unique sécurisé
- Continuité : si Lyon↔Marseille tunnel DOWN, Marseille perd internet
  (acceptable en PoC, production = replica DC à Marseille)
PARTIE 6 : AD — Samba4 (pas RODC Windows Server)
❓ Question : Pourquoi Samba4 centralisé + bind9 cache à Marseille ?
Approche	Cost	Effort	Limitations
Samba4 + bind9 cache ✅	Libre	Moyen	Nouveaux logins bloqués si tunnel DOWN
Windows Server DC	$$$$	Moyen	Compliqué à automatiser
Samba4 RODC	Libre	Haut	Samba4 ne supporte pas vraiment le RODC
Decision : Samba4 + bind9

✅ Libre (coût dossier = 0€)
✅ Automatisable entièrement via Ansible
⚠️ Limitation acceptée : nouveaux logins à Marseille bloqués si tunnel DOWN
Justification : "En production, on aurait un DC secondaire Windows Server"
Pour la soutenance : "C'est une limitation acceptée du PoC"
PARTIE 7 : Sécurité — Wazuh (SIEM/IDS)
❓ Question : Pourquoi Wazuh et pas ELK / Splunk ?
Outil	Wazuh	ELK Stack	Splunk
Type	SIEM + IDS natif	Logs aggregation	Enterprise SIEM
Cost	Libre ✅	Libre mais gros	Très cher
Agent	Lightweight ✅	Logstash/Filebeat	Splunk UF
CPU footprint	~50MB RAM/agent	~200MB	~300MB
Detection rules	5000+ MITRE ATT&CK	Créer custom	Pre-built enterprise
For students	Perfect ✅	Overkill	Trop cher
Decision : Wazuh

✅ Lightweight = pas étouffant sur 12 VMs
✅ Pre-built rules = détection de compromission out-of-box
✅ Dashboard intuitif = proof-of-concept facile à montrer au jury
Deployment :

Wazuh-01 (Manager + Dashboard)
  ↑
  └─ Agents sur : DC01, Web-01, DB-01, File-01, Proxy-01, Honeypot-01...
  └─ Double interface : eth0 (management) + eth1 (collecte logs de quarantine)
RÉSUMÉ PRÉSENTÉ AU JURY
Décision	Choix	Justification clé
Hyperviseur	Proxmox KVM	Open source, production-grade, Terraform-capable
IaC Infra	Terraform bpg/proxmox	Versionning, reproductibilité, git history
Config OS	Ansible	Pas d'agent, YAML simple, collections communauté
Firewall	OPNsense	API REST native, Ansible-supporté, Suricata IDS
Tunnel site-to-site	IPsec IKEv2	Standard RFC, hardware-acc possible, sécurisé
Directory	Samba4	Open source, automatisable, compatible Linux
SIEM/IDS	Wazuh	Lightweight, pre-built rules, dashboard visuel
📝 COMMENT PRÉSENTER CELA AU JURY ?
Structure orale (10 min) :

Slide 1 — Context (1 min)
"On doit déployer une infrastructure multi-site sécurisée"
"Cahier des charges : 12 VMs, 2 sites, firewall, SIEM"
Slide 2 — Why Proxmox (2 min)
"Pas GNS3 car simulateur, pas réaliste"
"Proxmox = hyperviseur production-grade open source"
"Terraform provider existe → full IaC"
Slide 3 — IaC Stack (2 min)
"Terraform crée l'infrastructure (VMs, bridges, VLANs)"
"Ansible configure les services (AD, web, SIEM)"
"Tout versionné dans Git → reproductibilité"
Slide 4 — Security by Design (2 min)
Montrer matrice firewall
"Deny All by Default"
"Wazuh détecte les anomalies"
Slide 5 — Multi-site Architecture (2 min)
Montrer diagramme Lyon ↔ Marseille
"IPsec IKEv2 (standard RFC)"
"Hub & Spoke : Lyon = point d'entrée unique"