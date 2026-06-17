# 03 — Décisions Techniques & Justifications

---

## OPNsense et non pfSense

**Décision :** OPNsense pour les deux firewalls (Lyon et Marseille).

**Pourquoi :**
- API REST native et documentée (pfSense n'a pas d'API officielle)
- Collection Ansible `ansibleguy.opnsense` couvre VLANs, rules, IPsec
- Licence BSD, 100% open source (pfSense a des restrictions depuis 2023)
- Suricata IDS intégré et configurable via API
- Plus adapté à l'automatisation IaC

**Limitation :** La configuration IPsec et OpenVPN restera partiellement manuelle sur OPNsense.
**Mitigation :** Export XML versionné dans Git après configuration initiale.

---

## Proxmox et non GNS3

**Décision :** Abandon de GNS3, migration vers Proxmox VE 8.

**Pourquoi :**
- GNS3 trop fragile : persistance réseau, DNS, apt instables
- Proxmox = hyperviseur de production, plus réaliste pour une soutenance
- Les bridges Linux VLAN-aware remplacent les switches GNS3 (plus simple, plus stable)
- Terraform provider natif (bpg/proxmox) vs aucun provider GNS3
- Ansible fonctionne directement sur les VMs Proxmox via SSH

**Pas besoin de GNS3** : les "switches" sont remplacés par vmbr1 (Lyon) et vmbr3 (Marseille) en mode VLAN-aware. OPNsense fait le routage inter-VLAN.

---

## Terraform pour la couche infra

**Décision :** Provider `bpg/proxmox` (communautaire, bien maintenu).

**Ce que Terraform gère :**
- Création des 6 bridges (vmbr0-5)
- Création des 12 VMs avec cloud-init
- Tags VLAN sur chaque interface VM
- Outputs : IPs des VMs → utilisés par Ansible inventory

**Limitation connue :** Provider communautaire, possible bugs sur certaines ressources.
**Mitigation :** Tester chaque ressource unitairement.

---

## Ansible pour la couche configuration

**Décision :** Inventory dynamique depuis les outputs Terraform.

**Roles prévus :**
- `common_hardening` : UFW, Fail2ban, SSH hardening, updates
- `samba_ad` : Samba4 AD + DNS sur DC01-Lyon
- `wazuh_server` : Installation Wazuh manager + dashboard
- `wazuh_agent` : Agent sur toutes les VMs
- `nginx_proxy` : Reverse proxy + SSL sur Proxy-01
- `mysql_db` : MySQL sur DB-01
- `nextcloud` : Nextcloud + auth AD sur File-01
- `bind9_dns` : DNS cache sur DNS-Marseille
- `network_persist` : IPs statiques persistantes

---

## DNS Marseille — Option B (cache bind9)

**Décision :** Pas de RODC Samba4 (non supporté), mais un serveur DNS cache bind9.

**Pourquoi pas RODC :**
- Samba4 ne supporte pas vraiment le mode RODC (expérimental/incomplet)
- Un vrai RODC nécessiterait Windows Server AD

**Ce que bind9 offre :**
- Tunnel UP : forward toutes les requêtes DNS vers DC01-Lyon (172.16.10.10)
- Tunnel DOWN : sert le cache des résolutions précédentes (TTL)
- Les sessions Kerberos actives restent valides
- Nouveaux logins AD bloqués (documenté comme limitation PoC)

**Pour la soutenance :** Expliquer que la production nécessiterait un DC replica complet (Windows Server ou Samba4 DC secondaire).

---

## Bastion sur bridge physiquement isolé (vmbr2)

**Décision :** Bastion-01 sur vmbr2 dédié, pas sur vmbr1 avec les autres VLANs.

**Pourquoi :** Si vmbr1 est compromis (VLAN hopping, ARP spoofing), le Bastion reste inaccessible car sur un bridge physiquement séparé. Le Bastion est la clé de voûte de l'administration — le protéger physiquement au niveau L2 est non négociable.

**Accès au Bastion :** Uniquement via VPN (OpenVPN) → OPNsense → vmbr2. Pas d'accès depuis le réseau interne direct.

---

## Quarantaine sur bridge physiquement isolé (vmbr4)

**Décision :** VLAN 999 sur vmbr4 dédié, pas sur vmbr1.

**Pourquoi :** Une machine compromise en quarantaine ne doit avoir aucun vecteur d'attaque vers le reste de l'infra. Sur un bridge dédié : pas de VLAN hopping, pas d'ARP spoofing, pas d'écoute passive possible.

**Seul flux autorisé :** Logs vers Wazuh via vmbr5 (collecte).

---

## VMware Workstation en mode Bridged (obligatoire)

**Décision :** VMware en mode Bridged, pas NAT.

**Pourquoi :** En mode NAT, les deux OPNsense seraient derrière le même NAT VMware. L'IPsec entre eux passerait par un double NAT ce qui peut poser des problèmes de traversée NAT. En mode Bridged, vmbr0 est directement sur le réseau physique et les deux OPNsense ont chacun une IP routable.

**Conséquence :** Activer "Virtualize Intel VT-x/EPT" dans VMware pour le nested KVM Proxmox.
