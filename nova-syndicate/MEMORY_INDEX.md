# NOVA SYNDICATE V2 — Index Mémoire Projet

> Lire ce fichier en premier à chaque nouvelle session.
> Il contient les pointeurs vers tous les contextes nécessaires pour reprendre sans perdre le fil.

## Résumé en une phrase
Infrastructure réseau sécurisée "Security by Design" pour entreprise fictive 85 employés (Lyon HQ + Marseille agence), déployée sur Proxmox via Terraform + Ansible + OPNsense.

## Fichiers mémoire disponibles

| Fichier | Contenu |
|---------|---------|
| [01_ARCHITECTURE.md](01_ARCHITECTURE.md) | Topologie complète, bridges Proxmox, plan d'adressage IP, inventaire VMs |
| [02_CAHIER_DES_CHARGES.md](02_CAHIER_DES_CHARGES.md) | Exigences techniques, matrice des flux firewall, décisions de sécurité |
| [03_DECISIONS_TECHNIQUES.md](03_DECISIONS_TECHNIQUES.md) | Choix technologiques et pourquoi (OPNsense, Proxmox, etc.) |
| [04_PLAN_BUILD.md](04_PLAN_BUILD.md) | Ordre de déploiement, phases, estimation temps |
| [05_POINTS_DE_FRICTION.md](05_POINTS_DE_FRICTION.md) | Problèmes anticipés et solutions retenues |
| [06_ETAT_AVANCEMENT.md](06_ETAT_AVANCEMENT.md) | Où on en est, ce qui est fait, ce qui reste |

## Stack technique en un coup d'œil

```
VMware Workstation (Windows 11, 32 GB RAM)
    └── Proxmox VE 8 (VM, 20 GB RAM, 150 GB disque)
            ├── Terraform (provider bpg/proxmox) — crée l'infra
            ├── Ansible — configure les VMs
            └── OPNsense — firewall, VLANs, IPsec, OpenVPN
```

## Commandes de départ (quand l'infra sera prête)

```bash
cd terraform/
terraform init && terraform apply

cd ../ansible/
ansible-playbook -i inventory.ini playbooks/deploy_all.yml
ansible-playbook -i inventory.ini playbooks/configure_firewalls.yml
```

## Repo GitHub
Projet_Nova_syndicate_Jedha (branche main)
