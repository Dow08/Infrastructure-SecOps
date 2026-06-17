# DEMO LIVE — Feuille de route Nova Syndicate
> Durée estimée : **5 à 7 minutes**
> À utiliser comme cheat sheet pendant la soutenance — 7 points de démonstration

---

## AVANT DE COMMENCER

- OPNsense Lyon ouvert dans un onglet
- OPNsense Marseille ouvert dans un onglet
- Wazuh Dashboard ouvert dans un onglet
- Grafana Dashboard ouvert dans un onglet
- Terminal prêt (bastion ou VM interne)
- Site BricoPro ouvert dans un onglet

---

## POINT 1 — Site BricoPro en production *(~45 sec)*

**Ce que tu montres :**
- Naviguer sur le site vitrine BricoPro (HTTP/HTTPS)
- Montrer que le site répond depuis un poste client

**Ce que tu dis :**
> "Le site e-commerce BricoPro est déployé sur un serveur web Nginx, accessible depuis les deux sites.
> Il tourne sur un VLAN dédié, isolé du reste de l'infra par les règles de firewall OPNsense."

**Fichier de référence :** `SIte vitrine deployé.png`

---

## POINT 2 — Tunnel IPsec Lyon ↔ Marseille *(~60 sec)*

**Ce que tu montres :**
1. OPNsense Lyon → VPN → IPsec → Statut du tunnel : **ESTABLISHED**
2. Ping depuis une VM Lyon vers une VM Marseille (inter-VLAN cross-site)

**Ce que tu dis :**
> "Le tunnel IPsec AES-256 relie les deux sites en permanence.
> Je peux pinger depuis Lyon vers Marseille à travers le VPN — la communication inter-sites est chiffrée de bout en bout."

**Commande à taper dans le terminal :**
```bash
ping 10.10.20.X   # IP d'une VM Marseille
```

**Fichiers de référence :** `Connexion ipsec lyon marseille active.png` | `Test de ping établie POC ipsec.png`

---

## POINT 3 — Active Directory + Samba *(~45 sec)*

**Ce que tu montres :**
- Terminal sur le serveur AD : `samba-tool domain info` ou `samba-tool user list`
- Montrer qu'il y a des utilisateurs créés et joints au domaine

**Ce que tu dis :**
> "L'Active Directory est géré par Samba4 sur le site de Lyon.
> Les utilisateurs sont centralisés, la gestion des comptes et des droits est opérationnelle.
> C'est la brique d'authentification centrale de tout le SI."

**Commande à taper :**
```bash
samba-tool user list
samba-tool domain info
```

**Fichiers de référence :** `Samba status + user tool active.png` | `POC AD + DB.png`

---

## POINT 4 — Monitoring Prometheus + Grafana + Loki *(~60 sec)*

**Ce que tu montres :**
1. Grafana → Dashboard node-exporter : CPU, RAM, disque des VMs
2. Grafana → Dashboard MySQL ou Nginx (si disponible)
3. Loki → Logs temps réel (une requête rapide)

**Ce que tu dis :**
> "La stack d'observabilité collecte les métriques de toutes les VMs en temps réel.
> Grafana affiche les dashboards, Prometheus scrape les targets toutes les 15 secondes,
> et Loki centralise les logs. Un seul écran pour voir l'état de toute l'infrastructure."

**Fichiers de référence :** `POC PROMETHEUS+GRAFANA+LOKI.png` | `Grafana-node exporter.png` | `log loki query en live.png`

---

## POINT 5 — Wazuh SIEM + Suricata IDS *(~60 sec)*

**Ce que tu montres :**
1. Wazuh Dashboard → Agents connectés (montrer les VMs supervisées)
2. Wazuh → Events récents → 1 ou 2 alertes de sécurité
3. (Bonus si temps) : Suricata → journalisation d'une alerte réseau

**Ce que tu dis :**
> "Wazuh supervise l'ensemble des endpoints. Les agents remontent les événements de sécurité en temps réel.
> Suricata analyse le trafic réseau en mode IDS — toute anomalie est journalisée et corrélée avec Wazuh.
> C'est le pattern SOC : corrélation SIEM + IDS pour la détection d'intrusion."

**Fichiers de référence :** `Dashboard Wazuh.png` | `Wazuh event.png` | `IDS SURICATA JOURNALISATION.png`

---

## POINT 6 — Infrastructure-as-Code : Terraform + Ansible *(~45 sec)*

**Ce que tu montres :**
- Terminal : montrer les fichiers Terraform (main.tf ou une sortie `terraform state list`)
- Terminal : montrer un playbook Ansible ou la sortie du `quickstart.sh`
- (Bonus) : Screenshot du déploiement des 12 VMs déjà fait

**Ce que tu dis :**
> "L'intégralité de l'infrastructure est codée : Terraform provisionne les 12 VMs, les 6 bridges et les 5 VLANs.
> Ansible configure chaque service via 10 playbooks.
> En cas de sinistre ou de reboot complet, l'infrastructure se redéploie en 30 à 45 minutes via un seul script."

**Commande à montrer :**
```bash
terraform state list
# ou
cat quickstart.sh
```

**Fichiers de référence :** `Création des 12 VMs automatiquement via terraform.png` | `DEploiement ansible terminé .png`

---

## POINT 7 — Pipeline CI/CD DevSecOps *(~45 sec)*

**Ce que tu montres :**
- GitHub → onglet Actions → dernier workflow security-scan.yml exécuté
- Montrer les 4 scanners passés : Trivy + Checkov + Gitleaks + Ansible-lint
- (Bonus) : Dependabot alerts ou Security tab

**Ce que tu dis :**
> "Le code est protégé par un pipeline de sécurité automatique.
> À chaque push, 4 scanners s'exécutent : vulnérabilités container, mauvaises configs IaC, secrets exposés, qualité des playbooks.
> C'est le principe Shift Left — la sécurité est intégrée dès l'écriture du code, pas après déploiement."

**Fichiers de référence :** `CICD Scan de sécurité.png` | `CICD GITHUB ACTION.png`

---

## CONCLUSION DE LA DÉMO *(~15 sec)*

**Ce que tu dis :**
> "Vous venez de voir l'infrastructure Nova Syndicate complète en conditions réelles :
> deux sites interconnectés, un SI applicatif opérationnel, une supervision 360°, et une sécurité en profondeur.
> Tout est documenté, versionné, et redéployable."

---

## EN CAS DE PROBLÈME TECHNIQUE

| Problème | Solution de secours |
|----------|-------------------|
| VM éteinte | Utiliser les screenshots POC dans `Z:\NOVA SYNDICATE V2\Documents\POC_Screen\` |
| Réseau coupé | Passer directement au point suivant, mentionner "comme visible sur ce screenshot" |
| Tunnel IPsec down | Montrer `Connexion ipsec lyon marseille active.png` et expliquer la procédure de rétablissement |
| Grafana inaccessible | Montrer `POC PROMETHEUS+GRAFANA+LOKI.png` comme fallback |

---

## ORDRE DE PRIORITÉ (si tu dois couper)

Si tu manques de temps, dans cet ordre :

| Priorité | Point | Pourquoi |
|----------|-------|----------|
| 🔴 Must show | 1 - BricoPro | Contexte métier immédiat |
| 🔴 Must show | 2 - IPsec | Architecture différenciante |
| 🔴 Must show | 5 - Wazuh + Suricata | Sécurité = cœur du projet |
| 🟠 Should show | 4 - Grafana + Loki | Observabilité = maturité |
| 🟠 Should show | 6 - Terraform + Ansible | IaC = valeur ajoutée |
| 🟡 Nice to have | 3 - AD + Samba | Complétude technique |
| 🟡 Nice to have | 7 - CI/CD | DevSecOps = bonus |

---

*Script rédigé le 28/05/2026 — Nova Syndicate Soutenance*
