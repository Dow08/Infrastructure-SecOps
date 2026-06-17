#!/bin/bash
# Quickstart Ansible Nova Syndicate
# A executer depuis Proxmox shell (root@pve)
# Usage : bash quickstart.sh [hardening|monitoring|all]
#   hardening  : juste le hardening (5 min)
#   monitoring : Prometheus + Loki + Grafana + agents + dashboards (25 min)
#   all        : tout (defaut, 30-45 min)

set -e

MODE=${1:-all}
ANSIBLE_DIR=/root/nova-ansible

# Couleurs
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"; }
warn() { echo -e "${ORANGE}[$(date +%H:%M:%S)] WARN${NC} $1"; }
err() { echo -e "${RED}[$(date +%H:%M:%S)] ERR${NC} $1"; exit 1; }

# === PRE-FLIGHT ===
log "===== Nova Syndicate Ansible Quickstart ====="
log "Mode demande : $MODE"

# Verifier qu'on est sur Proxmox
[ "$(hostname)" = "pve" ] || warn "Hostname different de 'pve', s'assurer qu'on est sur Proxmox host"

# Verifier Ansible installe
command -v ansible-playbook >/dev/null || err "Ansible non installe. Run: apt install -y ansible"

# Verifier dossier
[ -d "$ANSIBLE_DIR" ] || err "Dossier $ANSIBLE_DIR introuvable. Copie d'abord les fichiers Ansible depuis Z:"

cd "$ANSIBLE_DIR"

# Verifier inventory
[ -f inventory.ini ] || err "inventory.ini introuvable dans $ANSIBLE_DIR"

# === TEST CONNECTIVITE ===
log "Test connectivite Ansible (ping)..."
if ! ansible -i inventory.ini all -m ping > /tmp/ansible_ping.log 2>&1; then
  err "Ping Ansible echoue. Voir /tmp/ansible_ping.log. Verifier SSH key et VMs allumees."
fi
log "Tous les hosts repondent. OK."

# === EXECUTION ===
case "$MODE" in
  hardening)
    log "Lancement hardening (fail2ban + auto-updates + SSH/kernel)..."
    ansible-playbook -i inventory.ini playbook_hardening.yml
    ;;

  monitoring)
    log "Lancement stack monitoring..."
    log "  1/3 Serveur (Prometheus + Loki + Grafana)..."
    ansible-playbook -i inventory.ini playbook_monitoring_server.yml
    log "  2/3 Agents (node_exporter + promtail + mysqld_exporter + nginx_exporter)..."
    ansible-playbook -i inventory.ini playbook_monitoring_agents.yml
    log "  3/3 Import dashboards Grafana..."
    ansible-playbook -i inventory.ini playbook_grafana_dashboards.yml
    ;;

  all)
    log "Deploiement complet (site.yml)..."
    ansible-playbook -i inventory.ini site.yml
    ;;

  *)
    err "Mode inconnu : $MODE (options : hardening | monitoring | all)"
    ;;
esac

# === VALIDATION ===
log "===== Validation post-deploiement ====="

if [[ "$MODE" == "monitoring" || "$MODE" == "all" ]]; then
  log "Verification Prometheus targets..."
  TARGETS=$(curl -s --max-time 5 http://10.1.10.40:9090/api/v1/targets 2>/dev/null | grep -oE '"health":"up"' | wc -l)
  log "Targets up : $TARGETS"

  log "Verification Loki..."
  LOKI=$(curl -s --max-time 5 http://10.1.10.40:3100/ready 2>/dev/null || echo "fail")
  log "Loki status : $LOKI"

  log "Verification Grafana..."
  GRAFANA=$(curl -s --max-time 5 http://10.1.10.40:3000/api/health 2>/dev/null | grep -oE '"database":"ok"' || echo "fail")
  log "Grafana status : $GRAFANA"

  echo ""
  echo "===== Acces aux interfaces ====="
  echo "Depuis Windows, ouvre un tunnel SSH multi-port :"
  echo ""
  echo "  ssh -i C:\\Users\\Dow\\.ssh\\bastion_key \\"
  echo "      -L 9090:10.1.10.40:9090 \\"
  echo "      -L 3000:10.1.10.40:3000 \\"
  echo "      -L 3100:10.1.10.40:3100 \\"
  echo "      root@192.168.1.165"
  echo ""
  echo "Puis Chrome :"
  echo "  Prometheus : http://localhost:9090"
  echo "  Grafana    : http://localhost:3000 (admin/admin)"
  echo "  Loki API   : http://localhost:3100/ready"
fi

log "===== Deploiement termine avec succes ====="
