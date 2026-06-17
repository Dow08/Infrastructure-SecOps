#!/bin/bash
# check_status.sh — Diagnostic rapide infra Nova Syndicate
# À copier sur Proxmox host et exécuter : bash check_status.sh
# Affiche l'état réseau + SSH + service de chaque VM en une seule passe

set -u
KEY=/root/.ssh/bastion_key

declare -A VMS=(
  [102]="DC01-Lyon:10.1.10.10"
  [103]="Proxy-01:10.1.5.10"
  [104]="Web-01:10.1.5.30"
  [106]="Wazuh-01:10.1.10.20"
  [107]="DB-01:10.1.10.30"
  [108]="File-01:10.1.10.40"
  [109]="Bastion-01:172.16.100.20"
)

echo "============================================="
echo "  Nova Syndicate — Diagnostic infra"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="
echo ""

# 1. Bridge VLAN config Proxmox
echo "--- Bridge VLAN host (Proxmox) ---"
ip -4 addr show vmbr1.5 2>/dev/null | grep inet || echo "vmbr1.5 MANQUANT"
ip -4 addr show vmbr1.10 2>/dev/null | grep inet || echo "vmbr1.10 MANQUANT"
echo ""

# 2. Status par VM
echo "--- État des VMs ---"
printf "%-6s %-15s %-18s %-10s %-10s %-15s\n" "VMID" "Nom" "IP" "PVE" "Ping" "SSH"
echo "-----------------------------------------------------------------------------"

for vmid in "${!VMS[@]}"; do
  IFS=':' read -r name ip <<< "${VMS[$vmid]}"

  pve_status=$(qm status "$vmid" 2>/dev/null | awk '{print $2}')

  if ping -c 1 -W 1 "$ip" > /dev/null 2>&1; then
    ping_status="OK"
  else
    ping_status="KO"
  fi

  if ssh -i "$KEY" -o ConnectTimeout=3 -o StrictHostKeyChecking=no -o BatchMode=yes \
       "novaadmin@$ip" "true" > /dev/null 2>&1; then
    ssh_status="OK"
  else
    ssh_status="KO"
  fi

  printf "%-6s %-15s %-18s %-10s %-10s %-15s\n" "$vmid" "$name" "$ip" "$pve_status" "$ping_status" "$ssh_status"
done

echo ""
echo "--- Service status (via SSH si OK) ---"

# DC01 — Samba
if ssh -i "$KEY" -o ConnectTimeout=3 -o BatchMode=yes -o StrictHostKeyChecking=no \
     novaadmin@10.1.10.10 "systemctl is-active samba-ad-dc" 2>/dev/null | grep -q active; then
  echo "  DC01    samba-ad-dc    ACTIVE"
else
  echo "  DC01    samba-ad-dc    inaccessible ou inactif"
fi

# Wazuh-01 — Manager
if ssh -i "$KEY" -o ConnectTimeout=3 -o BatchMode=yes -o StrictHostKeyChecking=no \
     novaadmin@10.1.10.20 "systemctl is-active wazuh-manager" 2>/dev/null | grep -q active; then
  echo "  Wazuh   wazuh-manager  ACTIVE"
else
  echo "  Wazuh   wazuh-manager  inaccessible ou non installé"
fi

# DB-01 — MariaDB
if ssh -i "$KEY" -o ConnectTimeout=3 -o BatchMode=yes -o StrictHostKeyChecking=no \
     novaadmin@10.1.10.30 "systemctl is-active mariadb" 2>/dev/null | grep -q active; then
  echo "  DB-01   mariadb        ACTIVE"
else
  echo "  DB-01   mariadb        inaccessible ou non installé"
fi

# Web-01 — Nginx
if ssh -i "$KEY" -o ConnectTimeout=3 -o BatchMode=yes -o StrictHostKeyChecking=no \
     novaadmin@10.1.5.30 "systemctl is-active nginx" 2>/dev/null | grep -q active; then
  echo "  Web-01  nginx          ACTIVE"
else
  echo "  Web-01  nginx          inaccessible ou non installé"
fi

# Proxy-01 — Nginx
if ssh -i "$KEY" -o ConnectTimeout=3 -o BatchMode=yes -o StrictHostKeyChecking=no \
     novaadmin@10.1.5.10 "systemctl is-active nginx" 2>/dev/null | grep -q active; then
  echo "  Proxy   nginx          ACTIVE"
else
  echo "  Proxy   nginx          inaccessible ou non installé"
fi

echo ""
echo "============================================="
echo "  Fin diagnostic"
echo "============================================="
