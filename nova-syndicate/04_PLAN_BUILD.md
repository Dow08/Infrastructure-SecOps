# 04 — Plan de Build & Estimation

---

## Ordre de déploiement (à respecter — dépendances critiques)

```
PHASE 1 — Proxmox (fondation)
    ↓
PHASE 2 — Terraform (infra VMs)
    ↓
PHASE 3 — OPNsense Lyon (firewall + réseau)
    ↓
PHASE 4 — Ansible base (hardening + AD)
    ↓
PHASE 5 — Services applicatifs
    ↓
PHASE 6 — Marseille + IPsec
    ↓
PHASE 7 — Sécurité finale + tests
    ↓
PHASE 8 — Documentation + démo soutenance
```

---

## Phase 1 — Installation Proxmox (2-3h)

- [ ] Télécharger ISO Proxmox VE 8 sur proxmox.com
- [ ] Créer VM VMware avec paramètres corrects :
  - Guest OS : Debian 12 x64
  - CPU : 4 cores + **"Virtualize Intel VT-x/EPT" ACTIVÉ**
  - RAM : 20 GB
  - Disque : 150 GB thin provisioned
  - Réseau : **Bridged** (pas NAT)
- [ ] Installer Proxmox (hostname: pve.nova.local)
- [ ] Désactiver le message d'abonnement
- [ ] Accéder à https://IP_PROXMOX:8006
- [ ] Créer les 6 bridges : vmbr0 à vmbr5
  - vmbr0 : bridge physique (pas VLAN-aware)
  - vmbr1 : VLAN-aware, pas de bridge physique
  - vmbr2 : pas de bridge physique (isolé)
  - vmbr3 : VLAN-aware, pas de bridge physique
  - vmbr4 : pas de bridge physique (isolé)
  - vmbr5 : pas de bridge physique (collecte)
- [ ] Uploader les ISOs (OPNsense, Debian 12 cloud)

---

## Phase 2 — Terraform (3-5h)

- [ ] Initialiser le repo Terraform (`terraform/`)
- [ ] Configurer le provider bpg/proxmox
- [ ] Écrire `main.tf` : ressources VMs + réseau
- [ ] Écrire `variables.tf` : IPs, passwords, VLAN IDs
- [ ] Écrire `outputs.tf` : IPs pour l'inventory Ansible
- [ ] `terraform init` + `terraform plan`
- [ ] `terraform apply` — créer les VMs
- [ ] Vérifier que toutes les VMs démarrent

---

## Phase 3 — OPNsense Lyon (4-6h)

- [ ] Installer OPNsense-Lyon (2 interfaces : vmbr0 WAN + vmbr1 LAN)
- [ ] Ajouter les interfaces vmbr2, vmbr4, vmbr5
- [ ] Configurer les VLANs sur vmbr1 (5, 10, 30, 40, 110)
- [ ] Configurer les interfaces VLAN (adresses GW)
- [ ] Activer le serveur DHCP sur USERS VLAN 30
- [ ] Configurer NAT (USERS → Internet)
- [ ] Ajouter les règles firewall inter-VLAN (matrice des flux)
- [ ] Activer Suricata IDS sur WAN
- [ ] Installer le plugin OpenVPN → configurer le serveur VPN

---

## Phase 4 — Ansible base (4-5h)

- [ ] Créer `ansible/inventory.ini` depuis les outputs Terraform
- [ ] Rôle `common_hardening` : UFW, Fail2ban, SSH, updates
- [ ] Rôle `network_persist` : IPs statiques via /etc/network/interfaces
- [ ] Tester `ansible -m ping all` → 10/10 VMs répondent
- [ ] Rôle `samba_ad` : Samba4 AD + DNS sur DC01-Lyon
- [ ] Vérifier `samba-tool domain info novasyndicate.local`
- [ ] Rôle `wazuh_server` : installation Wazuh manager sur Wazuh-01
- [ ] Rôle `wazuh_agent` : agents sur toutes les VMs

---

## Phase 5 — Services applicatifs (4-5h)

- [ ] Rôle `nginx_proxy` : Nginx + SSL auto-signé sur Proxy-01
- [ ] Rôle `mysql_db` : MySQL sur DB-01, base nova_portal
- [ ] Rôle `nextcloud` : Nextcloud sur File-01, auth LDAP vers DC01
- [ ] Web-01 : page de portail simple (HTML/Nginx)
- [ ] Honeypot-01 : serveur SMTP factice (cowrie ou postfix minimal)
- [ ] Backup-01 : rsync + cron vers DC01 et DB-01
- [ ] Tester l'accès Nextcloud depuis USERS VLAN 30

---

## Phase 6 — Marseille + IPsec (3-4h)

- [ ] Installer OPNsense-Marseille (vmbr0 WAN + vmbr3 LAN)
- [ ] Configurer VLANs Marseille (50, 60) sur vmbr3
- [ ] Créer VM DNS-Marseille, déployer rôle `bind9_dns`
  - Forward vers 172.16.10.10 quand tunnel UP
- [ ] Configurer IPsec IKEv2 sur OPNsense Lyon
  - Phase 1 : AES-256, SHA-512, DH Group 20
  - Phase 2 : ESP AES-256-GCM, PFS Group 20
- [ ] Configurer IPsec IKEv2 sur OPNsense Marseille
- [ ] Tester : ping DC01-Lyon depuis Marseille
- [ ] Configurer route par défaut Marseille via tunnel (Hub & Spoke)
- [ ] Tester : internet depuis Marseille transite via Lyon

---

## Phase 7 — Sécurité finale + tests (3-4h)

- [ ] Exécuter tous les tests du cahier des charges (02_CAHIER_DES_CHARGES.md)
- [ ] Vérifier Wazuh Dashboard : tous les agents actifs
- [ ] Tester la quarantaine : migrer une VM vers vmbr4, vérifier isolation
- [ ] Vérifier que la DMZ ne peut pas pinguer internet
- [ ] Vérifier que USERS ne peut pas SSH directement vers SERVERS
- [ ] Exporter configs OPNsense en XML → versionner dans Git
- [ ] `git push origin main` — état final du repo

---

## Phase 8 — Documentation soutenance (2-3h)

- [ ] Mettre à jour le README du repo GitHub
- [ ] Préparer la démo : scénario d'attaque → quarantaine → Wazuh alerte
- [ ] Préparer les slides architecture (schéma Excalidraw v3)
- [ ] Répétition de la démo

---

## Estimation temps total

| Phase | Estimation | Cumulé |
|-------|-----------|--------|
| 1 — Proxmox | 2-3h | 3h |
| 2 — Terraform | 3-5h | 8h |
| 3 — OPNsense Lyon | 4-6h | 14h |
| 4 — Ansible base | 4-5h | 19h |
| 5 — Services | 4-5h | 24h |
| 6 — Marseille + IPsec | 3-4h | 28h |
| 7 — Tests sécurité | 3-4h | 32h |
| 8 — Documentation | 2-3h | 35h |
| **Buffer imprévus (+30%)** | **~10h** | **~45h** |

## En termes de sessions de travail

| Rythme | Durée estimée |
|--------|--------------|
| Tous les soirs 2-3h | 3 semaines |
| Weekends intensifs (6-8h/j) | 10-12 jours |
| Sessions régulières 3-4h, 3x/semaine | 2 semaines |

**Estimation réaliste : 2 à 3 semaines** en travaillant régulièrement.

> Les phases 3 (OPNsense) et 6 (IPsec) sont les plus imprévisibles car partiellement manuelles.
> Le reste est très automatisable via Terraform + Ansible.
