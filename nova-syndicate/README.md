# Nova Syndicate — Projet d'Infrastructure Réseau Sécurisée

> Infrastructure réseau complète déployée pour un site e-commerce — architecture multi-sites, sécurité Defense in Depth, observabilité temps réel, pipeline DevSecOps intégré.

[![Security Scan](https://github.com/Dow08/Projet_Nova_syndicate_Jedha/actions/workflows/security-scan.yml/badge.svg)](https://github.com/Dow08/Projet_Nova_syndicate_Jedha/actions/workflows/security-scan.yml)
[![Code Quality](https://github.com/Dow08/Projet_Nova_syndicate_Jedha/actions/workflows/lint.yml/badge.svg)](https://github.com/Dow08/Projet_Nova_syndicate_Jedha/actions/workflows/lint.yml)
[![Status](https://img.shields.io/badge/status-PoC%20Validé-success)]()
[![Conformité](https://img.shields.io/badge/conformité-ISO%2027001%20%7C%20ANSSI%20%7C%20NIST-blue)]()
[![Stack](https://img.shields.io/badge/stack-Terraform%20%7C%20Ansible%20%7C%20Wazuh%20%7C%20Prometheus%20%7C%20Loki-orange)]()
[![Sites](https://img.shields.io/badge/sites-Lyon%20%2B%20Marseille-green)]()
[![DevSecOps](https://img.shields.io/badge/DevSecOps-Trivy%20%7C%20Checkov%20%7C%20Gitleaks%20%7C%20Dependabot-red)]()

---

## Contexte du projet

**Nova Syndicate** opère un site e-commerce (**BricoPro**) déployé sur une infrastructure multi-sites : Lyon (site principal) et Marseille (site de repli PRA).

Le projet consiste à concevoir, déployer et sécuriser l'infrastructure réseau complète : segmentation VLAN, pare-feu périmétrique, Active Directory, SIEM, IDS, monitoring temps réel, et une stack applicative 3-tiers — le tout en Infrastructure-as-Code (Terraform + Ansible), reproductible et conforme aux référentiels normatifs (ISO 27001, ISO 22301, ANSSI, NIST, MITRE ATT&CK).

---

## Architecture cible

**Hub & Spoke** chiffré IPsec + **Defense in Depth** sur 5 couches :

```
                          ┌──────────────┐
                          │   Internet   │
                          └──────┬───────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │  OPNsense Lyon (Pare-feu)   │
                  │  + Suricata IDS (ET Open)   │
                  └──────────────┬──────────────┘
                                 │
       ┌──────────┬──────────────┼──────────────┬───────────┐
       │          │              │              │           │
   ┌───┴───┐  ┌───┴───┐    ┌─────┴─────┐   ┌────┴───┐  ┌────┴───┐
   │  DMZ  │  │ USERS │    │  SERVERS  │   │  MGMT  │  │ BACKUP │
   │ VLAN5 │  │VLAN30 │    │  VLAN10   │   │VLAN100 │  │VLAN110 │
   └───────┘  └───────┘    └───────────┘   └────────┘  └────────┘
       │                         │              │
   ┌───┴────┐               ┌────┴────┐    ┌────┴────┐
   │ Web    │               │ DC01    │    │ Bastion │
   │ Proxy  │               │ Wazuh   │    │  SSH    │
   │ Honey  │               │ DB-01   │    └─────────┘
   └────────┘               │ Files   │
                            └─────────┘

                  ⟷ IPsec AES-256 / SHA-512 / DH G20 ⟷

                          ┌──────────────┐
                          │  Marseille   │
                          │  (Site PRA)  │
                          │  RODC + USR  │
                          └──────────────┘
```

**5 couches de défense** : Pare-feu périmétrique → Segmentation VLAN → Hardening hôte → Détection (SIEM + IDS) → Audit logs centralisés.

[Topologie complète](Topologie_Final.excalidraw) | [Architecture détaillée](livrables/02_phase_II_conception/Document_Technique_Phase_II.md)

---

## Stack technique

### Infrastructure-as-Code

- **Terraform** — provisionnement (12 VMs, 6 bridges, 5 VLANs sur Proxmox)
- **Ansible** — configuration (10 playbooks idempotents)
- **Git** — versioning + auditabilité

### Hyperviseur & réseau

- **Proxmox VE 9.1.1** (KVM/QEMU)
- **OPNsense** (pare-feu + IDS Suricata)
- **IPsec IKEv2** (tunnel Lyon ↔ Marseille)

### Services

- **Samba 4** — Active Directory `nova.local`
- **MariaDB 10.11** + **Nginx** + **PHP-FPM** — Stack e-commerce **BricoPro** (22 produits, 5 catégories)
- **OpenVPN** — accès distant (auth AD)

### Sécurité — SIEM & IDS

- **Wazuh 4.7** (manager + indexer + dashboard + 3 agents)
- **Suricata** (5 865 règles ET Open + cron update + EVE JSON)
- **Fail2ban** + **UFW** + kernel sysctl hardening

### Observabilité — Stack LGTM

- **Prometheus** (métriques, 30j rétention)
- **Loki** (logs centralisés via Promtail)
- **Grafana** (visualisation + alerting, 5 dashboards)
- 4 exporters : node_exporter, mysqld_exporter, nginx_exporter, promtail

### DevSecOps — Pipeline CI/CD

- **Trivy** — scan CVE, secrets, misconfigurations IaC (format SARIF → GitHub Security tab)
- **Checkov** — audit IaC Terraform + Ansible, mappé CIS Benchmarks / NIST 800-53
- **Gitleaks** — détection de secrets dans l'historique Git complet
- **Ansible-lint** — validation best practices playbooks
- **Dependabot** — mises à jour automatiques des dépendances vulnérables
- **GitHub Advanced Security** — Code scanning, Secret scanning, Push protection
- Code quality : yamllint, markdownlint, ShellCheck, terraform fmt

---

## Les 10 livrables

| # | Livrable | Format |
|---|----------|--------|
| 1 | [Rapport Phase I — Analyse besoins](livrables/01_phase_I_analyse/Rapport_Phase_I_Analyse_Besoins.md) | Markdown (20p) |
| 2 | [Document Phase II — Conception & déploiement](livrables/02_phase_II_conception/Document_Technique_Phase_II.md) | Markdown (25p, 25 incidents) |
| 3 | [Rapport Phase III — Amélioration & résilience](livrables/03_phase_III_amelioration/Rapport_Amelioration_Phase_III.md) | Markdown (15p) |
| 4 | [PCA + PRA](livrables/04_pca_pra/PCA_PRA_Nova_Syndicate.md) | Markdown (17 risques cotés, 5 procédures) |
| 5 | [Veille techno EN — Wazuh 2025-2026](livrables/05_veille_techno_EN/Technology_Watch_Wazuh_SIEM_2025-2026.md) | Markdown (anglais) |
| 6 | [Scripts d'automatisation (3 + 8 playbooks Ansible)](livrables/06_scripts_automation/) | Python + Bash + YAML |
| 7 | [Plan self-pentest](livrables/07_pentest_report/Plan_Self_Pentest_Nova_Syndicate.md) | Markdown (10 scénarios PTES) |
| 8 | [CAPEX/OPEX détaillé](livrables/annexes_capex_opex/CAPEX_OPEX_Detaille.md) | Markdown + tableaux |
| 9 | Gestion projet | [Notion (Kanban 19 tâches)](https://www.notion.so/35ddae11bf0d81b69be1d152bacf14fd) |
| 10 | Présentation soutenance | À venir (vendredi 15/05) |

[Pitches soutenance — réponses préparées par thème](pitches_soutenance.md)

---

## Étude économique

Comparatif 3 solutions sur 3 ans (38 730 € TCO retenu) :

| Solution | TCO 3 ans | Souveraineté | Décision |
|----------|-----------|--------------|----------|
| A — Propriétaire (VMware + Microsoft) | 173 042 € | Faible | ❌ |
| **B — Open-source on-premise** | **38 730 €** | **Forte** | ✅ **Retenue** |
| C — Cloud public | 95 200 € | Moyenne | ❌ |

→ **-78 % d'économie vs propriétaire**, souveraineté française, zéro vendor lock-in.

[Détail CAPEX/OPEX](livrables/annexes_capex_opex/CAPEX_OPEX_Detaille.md)

---

## Déploiement reproductible

L'infra entière redéployable depuis **0** en **30-45 minutes** :

```bash
# 1. Provisionner les VMs (Terraform)
cd Build/terraform
terraform init
terraform apply

# 2. Configurer les services (Ansible)
cd livrables/06_scripts_automation/ansible
bash quickstart.sh all
```

Le `quickstart.sh` déploie :

- Hardening (Fail2ban + auto-updates + SSH/kernel)
- **Prometheus + Loki + Grafana** sur File-01
- 4 exporters + promtail sur tous les hosts
- Import auto des dashboards Grafana
- 8 règles d'alerting Prometheus

[Documentation Ansible complète](livrables/06_scripts_automation/ansible/README.md)

---

## Preuves de fonctionnement (POC)

35+ screenshots dans [`Documents/POC_Screen/`](Documents/POC_Screen/) — couvrant :

- **Infrastructure** : Proxmox, VM deploy, Terraform 12 VMs
- **Réseau** : OPNsense Lyon/Marseille, IPsec tunnel, VLANs, règles firewall
- **AD** : Samba install + user-tool actif
- **Web** : BricoPro 5 pages (Accueil, Catalogue, Espace pro, Infrastructure, Contact)
- **DB** : MariaDB connexion + données live
- **SIEM** : Wazuh dashboard + 3 agents + events MITRE
- **Observabilité** : Prometheus targets + Grafana (node/mysql/nginx) + Loki logs + alertes
- **IDS** : Suricata configuration + règles ET Open + journalisation
- **Automation** : Ansible deploy + ouverture ports auto

---

## Conformité multi-référentiels

Le projet s'inscrit dans un cadre normatif strict :

- **ISO 27001** — système de management de la sécurité
- **ISO 22301** — continuité d'activité (PCA)
- **ISO 27031** — préparation TIC (PRA)
- **ANSSI** — guide d'hygiène informatique + Defense in Depth
- **NIST SP 800-53** — contrôles sécurité
- **NIST SP 800-207** — Zero Trust Architecture
- **MITRE ATT&CK** — mapping détections Wazuh
- **OWASP Top 10** — sécurité applicative web
- **RGPD** — données personnelles
- **PCI-DSS** — anticipation phase paiement BricoPro

---

## Retour d'expérience opérationnel

**25 incidents techniques documentés** pendant le déploiement avec pour chacun : symptôme → cause racine → fix → apprentissage. Quelques exemples :

- Mismatch version Wazuh agent/manager → pinning + `apt-mark hold`
- TCG vs KVM (nested virt VirtualBox) → désactivation Hyper-V Windows
- MariaDB charset latin1 vs emojis UTF-8 → migration `utf8mb4`
- Bridge VLAN host non-persistant Proxmox → procédure documentée
- Cloud-init sshkeys non ré-injectables → workaround via mount disk

→ Démarche d'amélioration continue, preuve d'une infrastructure éprouvée et non purement théorique.

[Détail dans Document Phase II](livrables/02_phase_II_conception/Document_Technique_Phase_II.md)

---

## Contexte de réalisation

Projet réalisé dans le cadre du **titre RNCP Niveau 6 — Administrateur d'Infrastructures Sécurisées (AIS)** à **[Jedha Bootcamp](https://www.jedha.co/)**, soutenance orale devant jury.

---

## Contact

**Auteur** : Dow08 — RNCP 6 AIS — Promotion Jedha 2026
**Repo** : [github.com/Dow08/Projet_Nova_syndicate_Jedha](https://github.com/Dow08/Projet_Nova_syndicate_Jedha)

---

*Dernière mise à jour : mercredi 14/05/2026*
