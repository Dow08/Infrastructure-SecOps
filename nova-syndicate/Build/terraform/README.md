# Terraform — Provisionnement des 12 VMs Nova Syndicate sur Proxmox

Provider : `bpg/proxmox`. Crée les 12 VMs de l'architecture cible (2 OPNsense depuis ISO, 10 Debian clonées depuis le template cloud-init `9000`) avec leurs interfaces, VLAN et adresses IP.

## Prérequis

- Proxmox VE 9 avec les 6 bridges `vmbr0`…`vmbr5` créés (voir `../../04_PLAN_BUILD.md`).
- Template Debian 12 cloud-init en `vm_id = 9000`, ISO OPNsense dans `local:iso/`.
- Un token API Proxmox dédié (`Datacenter > Permissions > API Tokens`).

## Secrets

Aucun secret n'est versionné. Copier `terraform.tfvars.example` en `terraform.tfvars` (ignoré par git) ou exporter `TF_VAR_proxmox_api_token` et `TF_VAR_vm_password`. Le `terraform.tfstate` contient ces valeurs en clair : il est ignoré par git et doit rester local (en production : backend distant chiffré).

## Utilisation

```bash
terraform init
terraform plan
terraform apply
terraform output   # IPs → inventory Ansible
```

## Limites connues (PoC)

- `started = false` : les VMs sont créées éteintes, le démarrage ordonné (OPNsense d'abord) est manuel.
- Les deux OPNsense s'installent à la main depuis l'ISO, puis leur configuration XML est exportée et versionnée.
- Le PoC final a été consolidé sur 3 VMs (plan B) : voir `../../pitches_soutenance.md`.
