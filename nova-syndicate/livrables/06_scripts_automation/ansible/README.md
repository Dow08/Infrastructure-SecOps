# Ansible — Automation Nova Syndicate

> Stack complète d'automatisation : déploiement infrastructure + hardening + observabilité.
> Conformément au cahier des charges : Terraform pour l'infra, Ansible pour la config.

---

## Contenu

### Playbooks principaux

| Fichier | Rôle | Hosts ciblés | Durée |
|---------|------|--------------|-------|
| `quickstart.sh` | **Script tout-en-un** : test ping + lance playbooks selon mode | — | 30-45 min |
| `site.yml` | **Master playbook** — joue tout dans le bon ordre | tous | 30-45 min |
| `playbook_hardening.yml` | Fail2ban + auto-updates + SSH hardening + kernel hardening | lyon | 5-10 min |
| `playbook_monitoring_server.yml` | **Prometheus + Loki + Grafana** sur File-01 | observability_server | 10-15 min |
| `playbook_monitoring_agents.yml` | node_exporter + promtail + mysqld_exporter + nginx_exporter | monitored_hosts + mariadb/nginx_hosts | 5-10 min |
| `playbook_grafana_dashboards.yml` | Import dashboards communautaires (Node Exporter Full, MySQL, NGINX, Loki) | observability_server | 2-3 min |
| `prometheus_alerts.yml` | Règles alerting (host down, CPU/RAM/disk, services, sécurité) | observability_server | 2 min |

### Quickstart usage

```bash
cd /root/nova-ansible

bash quickstart.sh all          # Tout d'un coup (recommandé)
bash quickstart.sh hardening    # Juste le hardening
bash quickstart.sh monitoring   # Juste Prometheus + Loki + Grafana + agents
```

### Dashboards

| Fichier | Description |
|---------|-------------|
| `dashboards/nova_overview.json` | Dashboard custom Nova Syndicate (hôtes up, CPU, RAM, réseau, logs Loki) |

### Playbooks legacy (déjà déployés manuellement)

| Fichier | Note |
|---------|------|
| `playbook_wazuh_server.yml` | Wazuh SIEM — déjà installé sur File-01, conservé pour reproductibilité |
| `playbook_wazuh_agents.yml` | Agents Wazuh — déjà sur DC01 + DB-01, conservé |
| `playbook_web_proxy_db.yml` | Stack web — adapté à l'architecture initiale 7 VMs, partiellement obsolète |

### Inventaire

| Fichier | Description |
|---------|-------------|
| `inventory.ini` | Inventaire 3 VMs (Plan B), groupes : dc / siem_monitoring / servers / mariadb_hosts / nginx_hosts |

---

## Architecture observabilité

```
┌─────────────────────────────────────────────────────────────────┐
│                    File-01 (10.1.10.40 - 4GB)                   │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐  │
│  │  Prometheus │  │    Loki     │  │   Grafana   │  │ Wazuh  │  │
│  │   :9090     │  │   :3100     │  │    :3000    │  │ :443   │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └────────┘  │
│         │                │                 │                    │
└─────────┼────────────────┼─────────────────┼────────────────────┘
          │ scrape 15s     │ push logs       │ visualize
          │                │                 │
     ┌────┴────────────────┴─────────────────┴────┐
     │             VLAN 10 SERVERS                │
     └────┬───────────────────────────────┬───────┘
          │                               │
   ┌──────┴──────────┐         ┌──────────┴──────────┐
   │  DC01-Lyon      │         │  DB-01              │
   │  10.1.10.10     │         │  10.1.10.30         │
   │                 │         │                     │
   │  Samba AD       │         │  MariaDB + Nginx    │
   │  + node_exp:9100│         │  + node_exp:9100    │
   │  + promtail     │         │  + mysqld_exp:9104  │
   │                 │         │  + nginx_exp:9113   │
   │                 │         │  + promtail         │
   └─────────────────┘         └─────────────────────┘
```

### Métriques collectées

- **CPU, RAM, Disk, Network, Load** (node_exporter sur 3 hosts)
- **MariaDB** : connexions, queries/s, slow log, replication, innodb metrics
- **Nginx** : requêtes/s, status codes, connexions actives
- **Prometheus self-monitoring**

### Logs agrégés (Loki)

- `/var/log/*.log` (syslog, auth)
- Journald (systemd)
- Nginx access + error (DB-01)
- MariaDB error + slow query (DB-01)
- Wazuh OSSEC logs (File-01)

---

## Mise en route

### 1. Copier les fichiers sur Proxmox

```bash
# Si Z: monté
mkdir -p /root/nova-ansible
cp -r /mnt/z/NOVA\ SYNDICATE\ V2/livrables/06_scripts_automation/ansible/* /root/nova-ansible/

# Sinon depuis Windows
# scp -r Z:\NOVA SYNDICATE V2\livrables\06_scripts_automation\ansible\* root@192.168.1.165:/root/nova-ansible/
```

### 2. Vérifier connectivité

```bash
cd /root/nova-ansible
ansible -i inventory.ini all -m ping
```

Sortie attendue :
```
dc01    | SUCCESS => { "ping": "pong" }
file01  | SUCCESS => { "ping": "pong" }
db01    | SUCCESS => { "ping": "pong" }
```

### 3. Déploiement complet (recommandé)

```bash
ansible-playbook -i inventory.ini site.yml
```

OU étape par étape :

```bash
# Hardening de base
ansible-playbook -i inventory.ini playbook_hardening.yml

# Stack monitoring serveur (Prometheus + Loki + Grafana)
ansible-playbook -i inventory.ini playbook_monitoring_server.yml

# Agents observabilité
ansible-playbook -i inventory.ini playbook_monitoring_agents.yml

# Import dashboards Grafana
ansible-playbook -i inventory.ini playbook_grafana_dashboards.yml
```

---

## Validation post-déploiement

### Tests connectivité Prometheus

```bash
# Targets up
curl -s http://10.1.10.40:9090/api/v1/targets | jq '.data.activeTargets[].health'

# Doit retourner "up" pour chaque target
```

### Tests Loki

```bash
curl -s http://10.1.10.40:3100/ready
# → "ready"

curl -s http://10.1.10.40:3100/loki/api/v1/labels | jq
# → liste des labels de logs ingérés
```

### Tests Grafana

```bash
curl -s http://10.1.10.40:3000/api/health
# → {"database":"ok","version":"...","commit":"..."}
```

---

## Accès depuis Windows (via tunnel SSH)

```powershell
# Tunnel multi-port (Prometheus + Loki + Grafana)
ssh -i C:\Users\Dow\.ssh\bastion_key `
  -L 9090:10.1.10.40:9090 `
  -L 3100:10.1.10.40:3100 `
  -L 3000:10.1.10.40:3000 `
  root@192.168.1.165
```

Puis Chrome :
- Prometheus : http://localhost:9090
- Loki API : http://localhost:3100/ready
- Grafana : http://localhost:3000 (admin/admin)

---

## POCs à capturer

| # | Description |
|---|-------------|
| Prometheus | Status > Targets (tous up) |
| Prometheus | Query `up` avec graphe |
| Grafana | Home avec liste dashboards importés |
| Grafana | Dashboard Node Exporter Full (CPU/RAM par host) |
| Grafana | Dashboard MySQL Overview |
| Grafana | Explore Loki avec logs nginx |
| Loki | Curl `/loki/api/v1/labels` retournant les jobs |

---

## Variables modifiables (inventory.ini)

```ini
prometheus_version=2.51.2
loki_version=2.9.7
grafana_version=10.4.2
node_exporter_version=1.7.0
promtail_version=2.9.7
mysqld_exporter_version=0.15.1
nginx_exporter_version=1.1.0

monitoring_server_ip=10.1.10.40
loki_port=3100
prometheus_port=9090
grafana_port=3000
```

Modifie ces valeurs dans `inventory.ini` pour adapter sans toucher aux playbooks.

---

## Pour la soutenance

Le pitch IaC en 3 piliers :

1. **Provisionnement infra** → Terraform (12 VMs + 6 bridges + 5 VLANs)
2. **Configuration services** → Ansible (8 playbooks idempotents)
3. **Observabilité 4 plans** :
   - **Wazuh** (sécurité — événements, MITRE ATT&CK, FIM, compliance)
   - **Prometheus** (métriques — CPU/RAM/Disk/services)
   - **Loki** (logs centralisés — syslog, app logs, nginx, MariaDB)
   - **Grafana** (visualisation unifiée — dashboards + alertes)

Cette séparation est conforme à l'état de l'art DevOps moderne (Site Reliability Engineering — Google SRE Book). Elle permet la reproductibilité (Git), l'auditabilité (logs centralisés), et la résilience (un crash = redéploiement automatique).

---

## Pré-requis hardware

| VM | RAM minimum | Pourquoi |
|----|-------------|----------|
| File-01 | **4 GB** (déjà bumpé) | Wazuh (~2 GB) + Prometheus (~200 MB) + Loki (~300 MB) + Grafana (~150 MB) + OS |
| DC01-Lyon | 2 GB | Samba AD + agents (~150 MB) |
| DB-01 | 2 GB | MariaDB + Nginx + PHP + agents (~150 MB) |

Si File-01 manque de RAM (lag dashboards), bump à 6 GB :
```bash
qm stop 108 && qm set 108 --memory 6144 && qm start 108
```

---

**Production : 12/05/2026** | **Nova Syndicate** | **Plan B — 3 VMs working**
