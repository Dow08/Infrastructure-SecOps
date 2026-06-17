# 02 — Cahier des Charges & Exigences Techniques

---

## Contexte du projet

**Entreprise fictive :** Nova Syndicate (secteur médical/défense)
**Effectif :** 85 collaborateurs
- 40 employés à Lyon (HQ)
- 25 employés à Marseille (agence)
- 20 agents itinérants (PC portables + VPN OpenVPN TLS)

**Objectif :** Infrastructure réseau sécurisée "Security by Design" avec IaC complète.

---

## Exigences techniques — Toutes couvertes ✅

| Exigence | Solution retenue | VM |
|----------|-----------------|-----|
| Serveur Web public | Web-01 (Apache/Nginx) + Proxy-01 (reverse proxy) | DMZ VLAN 5 |
| Base de données | DB-01 (MySQL) isolée en SERVERS | VLAN 10 |
| Serveur de fichiers | File-01 (Nextcloud) authentification AD | VLAN 10 |
| Active Directory | DC01-Lyon (Samba4) centralisé | VLAN 10 |
| Supervision/SIEM | Wazuh-01 (SIEM + IDS + Dashboard) | VLAN 10 + vmbr5 |
| Sauvegarde isolée | Backup-01 (VLAN dédié, SERVERS only) | VLAN 110 |
| Firewall périmétrique | OPNsense Lyon (NAT, PF, IDS Suricata) | WAN + vmbr1 |
| Sécurité hôte | UFW + Fail2ban + Suricata sur OPNsense | Toutes VMs |
| Accès distant agents | OpenVPN TLS (20 agents) → OPNsense Lyon | Via WAN |
| Site distant | IPsec IKEv2 AES-256 Lyon ↔ Marseille | Via vmbr0 |
| IaC | Terraform (Proxmox) + Ansible (config) + Git | — |
| Continuité DNS Marseille | bind9 DNS cache (forward DC01 si UP, cache si DOWN) | VLAN 50 |
| Honeypot | Honeypot-01 (leurre messagerie, isolé en DMZ) | VLAN 5 |

---

## Matrice des flux Firewall — Deny All by Default

### Flux autorisés (whitelist)

| Source | Destination | Port/Proto | Justification |
|--------|------------|-----------|---------------|
| WAN | DMZ (Proxy-01) | TCP 80/443 | Accès public portail Nova |
| DMZ (Web-01) | SERVERS (DB-01) | TCP 3306 | Backend MySQL |
| DMZ | Collecte vmbr5 (Wazuh) | TCP 1514 | Logs IDS |
| QUARANTAINE | Collecte vmbr5 (Wazuh) | TCP 1514 | Monitoring postes compromis |
| MGMT (Bastion) | SERVERS | TCP 22 | Administration SSH |
| USERS | Internet | NAT | Navigation web |
| USERS | SERVERS (DC01) | TCP 389/636/88 | Auth LDAP/Kerberos AD |
| USERS | SERVERS (File-01) | TCP 443 | Accès fichiers Nextcloud |
| USERS | PRINTS | TCP 9100/631 | Impression |
| BACKUP | SERVERS | rsync/SMB | Push sauvegardes |
| VPN agents | USERS VLAN 30 | Via OPNsense | Après auth AD |
| Marseille IPsec | SERVERS (DC01) | TCP 389/88 | Auth AD |
| Marseille IPsec | SERVERS (File-01) | TCP 443 | Fichiers |
| Marseille IPsec | Internet | NAT via Lyon | Transit Hub & Spoke |

### Flux bloqués (exemples clés)

| Source | Destination | Raison |
|--------|------------|--------|
| DMZ | Internet (egress) | Anti-exfiltration |
| DMZ | SERVERS (sauf DB+Wazuh) | Isolation DMZ |
| USERS | DMZ | Least privilege |
| USERS | MGMT | Isolation admin |
| QUARANTAINE | Tout sauf Wazuh collecte | Cul-de-sac |
| SERVERS | MGMT | Least privilege inversé |
| WAN | Interne direct | Deny all WAN→LAN |

---

## Principes de sécurité appliqués

### Security by Design
- Chaque VLAN est isolé par défaut
- Les exceptions sont explicitement déclarées dans OPNsense
- Pas de règle "allow any"

### Defense in Depth
- Périmètre externe : OPNsense + Suricata IDS
- Périmètre DMZ : règles strictes, egress bloqué
- Périmètre interne : inter-VLAN deny all
- Hôte : UFW + Fail2ban sur chaque VM

### Least Privilege
- MGMT → SSH uniquement vers SERVERS
- BACKUP → push uniquement, pas d'accès en lecture des autres VLANs
- USERS → ressources métier uniquement, pas d'accès infra

### Isolation physique (bridges dédiés)
- Bastion : vmbr2 — pas de VLAN hopping possible
- Quarantaine : vmbr4 — aucun segment commun avec la production

---

## Critères de validation PoC (pour la soutenance)

| Test | Méthode | Attendu |
|------|---------|---------|
| Connexion internet Lyon | ping 8.8.8.8 depuis USERS | ✅ |
| Connexion internet Marseille | ping 8.8.8.8 depuis USERS Marseille | ✅ via Lyon |
| Tunnel IPsec | ping DC01-Lyon depuis Marseille | ✅ |
| Auth AD depuis Marseille | kinit user@novasyndicate.local | ✅ |
| Portail Web accessible | curl https://portail-nova depuis WAN | ✅ |
| DMZ ne peut pas pinguer internet | ping 8.8.8.8 depuis Web-01 | ❌ bloqué |
| Quarantaine isolée | ping depuis VM quarantaine | ❌ tout bloqué |
| Wazuh reçoit les logs | Dashboard Wazuh → agents actifs | ✅ |
| Bastion SSH vers DC01 | ssh depuis Bastion → DC01 | ✅ |
| Pas de SSH direct vers DC01 depuis USERS | ssh depuis poste user | ❌ bloqué |
| Démo quarantaine | Migrer VM vers vmbr4 → plus d'accès | ✅ |
