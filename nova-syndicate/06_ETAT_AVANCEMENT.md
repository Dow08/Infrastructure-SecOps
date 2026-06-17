# 06 — État d'Avancement

Mis à jour : 2026-05-06

---

## Statut global : PRÊT À BUILDER ✅

La topologie est validée. Les décisions techniques sont prises. On peut commencer Phase 1.

---

## Phases

| Phase | Statut | Notes |
|-------|--------|-------|
| Topologie v3 | ✅ VALIDÉE | Excalidraw nova_syndicate_topology_v3_proxmox.excalidraw |
| Cahier des charges | ✅ VALIDÉ | 02_CAHIER_DES_CHARGES.md |
| Décisions techniques | ✅ PRISES | OPNsense, Proxmox, Terraform bpg, bind9 Marseille |
| Plan de build | ✅ ÉCRIT | 04_PLAN_BUILD.md |
| Points de friction | ✅ IDENTIFIÉS | 05_POINTS_DE_FRICTION.md |
| Phase 1 — Proxmox | ⏸ À FAIRE | — |
| Phase 2 — Terraform | ⏸ À FAIRE | — |
| Phase 3 — OPNsense Lyon | ⏸ À FAIRE | — |
| Phase 4 — Ansible base | ⏸ À FAIRE | — |
| Phase 5 — Services | ⏸ À FAIRE | — |
| Phase 6 — Marseille + IPsec | ⏸ À FAIRE | — |
| Phase 7 — Tests sécurité | ⏸ À FAIRE | — |
| Phase 8 — Documentation | ⏸ À FAIRE | — |

---

## Prochaine session — Actions immédiates

1. Télécharger ISO Proxmox VE 8
2. Créer la VM Proxmox dans VMware (paramètres dans 04_PLAN_BUILD.md)
3. Installer Proxmox + accéder à l'interface web
4. Créer les 6 bridges (vmbr0 à vmbr5)

---

## Repo GitHub

- Repo : Projet_Nova_syndicate_Jedha
- Branche principale : main
- À créer : dossiers `terraform/` et `ansible/` from scratch

---

## Mot de passe standard du projet

- Proxmox root : `Nova2026!`
- VMs root : `Nova2026!`
- AD Samba4 : `Nova2024Pass` (sans caractères spéciaux pour les consoles AZERTY)
- OPNsense admin : `Nova2026!`

---

## Questions ouvertes

- [ ] IP statique ou DHCP pour l'interface WAN des OPNsense sur vmbr0 ?
  → Probablement DHCP depuis ta box pour le PoC
- [ ] Quel certificat SSL pour Proxy-01 ? Auto-signé pour le PoC.
- [ ] Honeypot-01 : quel logiciel ? cowrie (SSH honeypot) ou opencanary ?
