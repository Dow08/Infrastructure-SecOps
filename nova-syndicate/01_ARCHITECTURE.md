# 01 — Architecture Réseau Sécurisée v3

Topologie validée le 2026-05-06.
Fichier Excalidraw source : `Dossier_final_nova/nova_syndicate_topology_v3_proxmox.excalidraw`

---

## Vue d'ensemble

```
Internet (WAN — vmbr0)
        │
        ├── OPNsense Lyon (HQ)          ◄──── IPsec IKEv2 ────► OPNsense Marseille
        │   WAN: vmbr0                         AES-256                WAN: vmbr0
        │   LAN: vmbr1 (trunk VLAN)            SHA-512                LAN: vmbr3 (trunk)
        │   MGMT: vmbr2 (isolé)                PFS G20
        │   QUAR: vmbr4 (isolé)
        │   COLLECTE: vmbr5 (Wazuh eth1)
        │
        │── DMZ VLAN 5 (172.16.5.0/24)
        │── SERVERS VLAN 10 (172.16.10.0/24)
        │── USERS VLAN 30 (172.16.30.0/24)
        │── PRINTS VLAN 40 (172.16.40.0/24)
        │── MGMT VLAN 100 (172.16.100.0/24)     ← vmbr2 ISOLÉ
        │── BACKUP VLAN 110 (172.16.110.0/24)
        └── QUARANTAINE VLAN 999 (10.99.0.0/24) ← vmbr4 ISOLÉ
```

---

## Proxmox — 6 Bridges Réseau

| Bridge | VLAN-aware | Rôle | Sécurité |
|--------|-----------|------|----------|
| vmbr0 | Non | WAN → internet réel (bridge VMware Bridged) | IPsec transite ici |
| vmbr1 | **Oui** | LAN Lyon (VLANs 5, 10, 30, 40, 110) | Production segmentée |
| vmbr2 | Non | MGMT isolé — Bastion uniquement | VLAN hopping impossible |
| vmbr3 | **Oui** | LAN Marseille (VLANs 50, 60) | Site distant isolé |
| vmbr4 | Non | Quarantaine cul-de-sac | Aucune route, sauf logs Wazuh |
| vmbr5 | Non | Collecte logs Wazuh (eth1) | DMZ/Quar → Wazuh sans toucher SERVERS |

---

## Inventaire VMs — 12 machines (~16 GB RAM total)

### Site Lyon

| VM | VLAN | IP | Bridge(s) | RAM | Rôle |
|----|------|-----|-----------|-----|------|
| OPNsense-Lyon | WAN + trunk | DHCP WAN | vmbr0+vmbr1+vmbr2+vmbr4+vmbr5 | 2 GB | Firewall HQ, IPsec, OpenVPN, Suricata |
| Proxy-01 | 5 DMZ | 172.16.5.10 | vmbr1 | 1 GB | Nginx reverse proxy HTTPS |
| Web-01 | 5 DMZ | 172.16.5.30 | vmbr1 | 1 GB | Portail Web Nova / Frontend |
| Honeypot-01 | 5 DMZ | 172.16.5.40 | vmbr1 | 512 MB | Leurre messagerie, serveur isolé |
| DC01-Lyon | 10 SERVERS | 172.16.10.10 | vmbr1 | 2 GB | Samba4 AD + DNS (novasyndicate.local) |
| Wazuh-01 | 10 SERVERS + collecte | 172.16.10.20 + 172.16.200.1 | vmbr1 + vmbr5 | 4 GB | SIEM + IDS + Dashboard |
| DB-01 | 10 SERVERS | 172.16.10.30 | vmbr1 | 1 GB | MySQL backend portal Web |
| File-01 | 10 SERVERS | 172.16.10.40 | vmbr1 | 1 GB | Nextcloud, auth via AD |
| Bastion-01 | 100 MGMT | 172.16.100.20 | **vmbr2** | 512 MB | SSH Jump Host — accès VPN only |
| Backup-01 | 110 BACKUP | 172.16.110.10 | vmbr1 | 1 GB | Sauvegardes AD, DB, configs, OPNsense XML |

### Site Marseille

| VM | VLAN | IP | Bridge(s) | RAM | Rôle |
|----|------|-----|-----------|-----|------|
| OPNsense-Marseille | WAN + trunk | DHCP WAN | vmbr0 + vmbr3 | 1 GB | Firewall agence, IPsec → Lyon, transit internet |
| DNS-Marseille (bind9) | 50 USERS | 172.16.50.5 | vmbr3 | 512 MB | DNS cache local (forward → DC01 si tunnel UP, cache si DOWN) |

### Zones sans VM dédiée (routées par OPNsense)

| VLAN | Réseau | Contenu |
|------|--------|---------|
| 30 USERS Lyon | 172.16.30.0/24 | 40 postes, GW 172.16.30.1 |
| 40 PRINTS Lyon | 172.16.40.0/24 | Imprimantes réseau |
| 60 PRINTS Marseille | 172.16.60.0/24 | Imprimantes réseau |
| 999 QUARANTAINE | 10.99.0.0/24 | vmbr4 — postes compromis |

---

## IPsec Lyon ↔ Marseille

| Paramètre | Valeur |
|-----------|--------|
| Protocole | IKEv2 |
| Chiffrement | AES-256 |
| Intégrité | SHA-512 |
| DH/PFS | Group 20 |
| Transport | Via vmbr0 (WAN) — pas de trunk direct |
| Modèle | Hub & Spoke — tout l'internet Marseille transite via Lyon |

### Fallback si tunnel tombe

- Internet Marseille : **coupé** (acceptable pour le PoC, produirait une liaison secondaire)
- DNS : servi depuis le cache bind9 local (résolutions récentes disponibles)
- Sessions Kerberos actives : restent valides jusqu'à expiration du ticket
- Nouveaux logins AD : **bloqués** — documenté comme limitation PoC

---

## Wazuh — Architecture double interface

```
eth0 : 172.16.10.20 (vmbr1, VLAN 10 SERVERS)
   → Management, dashboard, API, collecte depuis SERVERS

eth1 : 172.16.200.1 (vmbr5, réseau collecte dédié)
   → Reçoit les logs DMZ (Proxy-01, Web-01, Honeypot-01)
   → Reçoit les logs Quarantaine
   → Aucun chemin retour vers SERVERS via ce bridge
```

---

## Allocation RAM Proxmox

| Composant | RAM |
|-----------|-----|
| Windows 11 (hôte) | 8 GB |
| VMware overhead | 2 GB |
| Proxmox VM | 20 GB |
| — VMs Lyon + Marseille | ~16 GB |
| — Proxmox OS lui-même | ~4 GB |
| **Total machine** | **30 GB / 32 GB** |
