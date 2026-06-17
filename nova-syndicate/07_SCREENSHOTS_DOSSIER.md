# 07 — Screenshots à capturer pour le Dossier Final

> Ce fichier liste tous les screenshots à prendre pendant le build.
> Chaque capture est une preuve de fonctionnement pour la soutenance.
> Cocher au fur et à mesure.

---

## Phase 1 — Proxmox

- [ ] Interface web Proxmox accessible (https://IP:8006) — login root
- [ ] Vue des 6 bridges créés (vmbr0 à vmbr5) dans Network
- [ ] Vue de l'espace disque disponible (150 GB)

## Phase 2 — Terraform

- [ ] `terraform plan` — liste des ressources à créer
- [ ] `terraform apply` — output final avec les IPs des 12 VMs
- [ ] Vue Proxmox : liste des VMs créées dans le datacenter

## Phase 3 — OPNsense Lyon

- [ ] Dashboard OPNsense Lyon — interfaces actives (WAN + VLANs)
- [ ] Liste des interfaces VLAN (5, 10, 30, 40, 100, 110, 999)
- [ ] Règles firewall inter-VLAN dans OPNsense (Deny All visible)
- [ ] Suricata IDS actif sur l'interface WAN
- [ ] Serveur OpenVPN configuré (status actif)

## Phase 4 — Ansible base

- [ ] `ansible -m ping all` → 12/12 SUCCESS (toutes les VMs répondent)
- [ ] `ansible-playbook deploy_all.yml` — play recap final (0 failed)
- [ ] `samba-tool domain info novasyndicate.local` — AD opérationnel
- [ ] Wazuh Dashboard — liste des agents actifs (toutes les VMs)

## Phase 5 — Services applicatifs

- [ ] Portail Web Nova accessible depuis navigateur (https://IP_PROXY)
- [ ] Page Nextcloud accessible + login AD fonctionnel
- [ ] MySQL connecté (db nova_portal existe)
- [ ] Wazuh alerte visible sur un événement réel

## Phase 6 — Marseille + IPsec

- [ ] OPNsense Marseille dashboard — interfaces actives
- [ ] Tunnel IPsec Status = **Established** (dans OPNsense Lyon ET Marseille)
- [ ] `ping 172.16.10.10` depuis une VM Marseille → SUCCESS (via IPsec)
- [ ] `traceroute 8.8.8.8` depuis Marseille → transit via Lyon visible
- [ ] `nslookup dc01.novasyndicate.local` depuis Marseille → résolu

## Phase 7 — Tests de sécurité (preuves de blocage = aussi importantes)

- [ ] `ping 8.8.8.8` depuis Web-01 (DMZ) → **TIMEOUT** (egress bloqué ✅)
- [ ] `ssh 172.16.10.10` depuis USERS VLAN 30 → **REFUSED** (accès bloqué ✅)
- [ ] `ssh 172.16.100.20` depuis USERS → **REFUSED** (Bastion inaccessible ✅)
- [ ] VM en quarantaine : `ping 172.16.10.10` → **TIMEOUT** (isolée ✅)
- [ ] VM en quarantaine : Wazuh reçoit toujours ses logs → visible dashboard
- [ ] Connexion VPN OpenVPN depuis poste externe → IP dans VLAN 30 assignée
- [ ] `ssh bastion → DC01` via jump host → **SUCCESS** (seul chemin autorisé)

## Phase 8 — Démo soutenance

- [ ] Schéma Excalidraw v3 affiché (nova_syndicate_topology_v3_proxmox.excalidraw)
- [ ] Scénario d'attaque simulé → Wazuh alerte déclenchée → screenshot alerte
- [ ] Migration VM vers quarantaine (avant/après dans Proxmox)
- [ ] Repo GitHub — structure Terraform + Ansible visible
- [ ] `git log --oneline` — historique de commits propre

---

## Convention de nommage des fichiers

```
PHASE1_proxmox_interface_web.png
PHASE2_terraform_apply_output.png
PHASE3_opnsense_ipsec_established.png
PHASE4_ansible_ping_12_success.png
PHASE5_portail_nova_web.png
PHASE6_marseille_ping_dc01.png
PHASE7_dmz_egress_bloque.png
PHASE7_quarantaine_isolee.png
PHASE8_wazuh_alerte_demo.png
```

Stocker dans : `NOVA SYNDICATE V2/screenshots/`
