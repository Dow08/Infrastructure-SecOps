#!/usr/bin/env bash
# Utility script for backup and restore of databases & volumes on the VPS.
# This script is meant to be run manually by the operator to backup the state
# of the services before a migration, or restore them.

set -euo pipefail

BACKUP_DIR="/root/vps-backups"
DATE_STR=$(date +%Y%m%d_%H%M%S)

show_help() {
    echo "Usage: $0 {backup|restore} [backup_tar_path]"
    echo ""
    echo "Actions:"
    echo "  backup              Backs up SQLite DBs, .env configurations, static hub root, and Docker volumes."
    echo "  restore [path]      Restores the specified backup archive."
}

do_backup() {
    echo "Starting backup process..."
    mkdir -p "${BACKUP_DIR}"
    
    local archive_name="${BACKUP_DIR}/vps_state_backup_${DATE_STR}.tar.gz"
    
    # Create temporary staging directory
    local staging="/tmp/vps_staging_${DATE_STR}"
    mkdir -p "${staging}"
    
    # 1. Backup system configurations and basic auth
    echo "Copying configuration files..."
    mkdir -p "${staging}/etc"
    cp /etc/nginx/.htpasswd_hermes "${staging}/etc/" || true
    cp /etc/nginx/sites-available/cyberstation "${staging}/etc/" || true
    
    # 2. Backup env files
    echo "Copying d'env variables (.env)..."
    mkdir -p "${staging}/envs"
    cp /root/.hermes/.env "${staging}/envs/hermes-agent.env" || true
    cp /root/.hermes/config.yaml "${staging}/envs/hermes-agent.config.yaml" || true
    cp /root/hermes-workspace/.env "${staging}/envs/hermes-workspace.env" || true
    cp /root/Shadowbroker/.env "${staging}/envs/shadowbroker.env" || true
    
    # 3. Backup active data state
    echo "Copying databases and active data..."
    mkdir -p "${staging}/data"
    cp /root/.hermes/state.db "${staging}/data/hermes-agent-state.db" || true
    cp -r /root/.hermes/skills "${staging}/data/hermes-skills" || true
    cp -r /root/.hermes/memories "${staging}/data/hermes-memories" || true
    
    # 4. Backup static hub files
    echo "Copying static hub root..."
    mkdir -p "${staging}/var"
    cp -r /var/www/hub "${staging}/var/hub" || true
    
    # 5. Backup Shadowbroker docker volume
    echo "Backing up Docker volume 'shadowbroker_backend_data'..."
    docker run --rm \
        -v shadowbroker_backend_data:/volume \
        -v "${staging}/data:/backup" \
        alpine tar -czf /backup/shadowbroker_backend_data.tar.gz -C /volume . || true
        
    # Compress the whole staging folder
    echo "Compressing everything into ${archive_name}..."
    tar -czf "${archive_name}" -C "${staging}" .
    
    # Clean up staging
    rm -rf "${staging}"
    
    echo "Backup completed successfully!"
    echo "Backup file located at: ${archive_name}"
}

do_restore() {
    local tar_path="${1:-}"
    if [[ -z "${tar_path}" ]]; then
        echo "Error: You must specify the path of the backup .tar.gz archive to restore."
        show_help
        exit 1
    fi
    
    if [[ ! -f "${tar_path}" ]]; then
        echo "Error: File ${tar_path} not found."
        exit 1
    fi
    
    echo "Starting restoration from ${tar_path}..."
    local staging="/tmp/vps_restore_staging"
    rm -rf "${staging}"
    mkdir -p "${staging}"
    
    # Extract
    tar -xzf "${tar_path}" -C "${staging}"
    
    # Stop active services to prevent write locks
    echo "Stopping active services before restore..."
    systemctl stop hermes-gateway hermes-dashboard hermes-ui nginx || true
    cd /root/Shadowbroker && docker compose down || true
    
    # Restore configs and basic auth
    echo "Restoring configurations..."
    cp "${staging}/etc/.htpasswd_hermes" /etc/nginx/.htpasswd_hermes || true
    cp "${staging}/etc/cyberstation" /etc/nginx/sites-available/cyberstation || true
    
    # Restore env files
    echo "Restoring d'env variables (.env)..."
    mkdir -p /root/.hermes
    cp "${staging}/envs/hermes-agent.env" /root/.hermes/.env || true
    cp "${staging}/envs/hermes-agent.config.yaml" /root/.hermes/config.yaml || true
    cp "${staging}/envs/hermes-workspace.env" /root/hermes-workspace/.env || true
    cp "${staging}/envs/shadowbroker.env" /root/Shadowbroker/.env || true
    
    # Restore active data state
    echo "Restoring database and user state..."
    cp "${staging}/data/hermes-agent-state.db" /root/.hermes/state.db || true
    cp -r "${staging}/data/hermes-skills"/* /root/.hermes/skills/ || true
    cp -r "${staging}/data/hermes-memories"/* /root/.hermes/memories/ || true
    
    # Restore static hub files
    echo "Restoring static hub root..."
    mkdir -p /var/www/hub
    cp -r "${staging}/var/hub"/* /var/www/hub/ || true
    
    # Restore Shadowbroker docker volume
    echo "Restoring Docker volume 'shadowbroker_backend_data'..."
    if [[ -f "${staging}/data/shadowbroker_backend_data.tar.gz" ]]; then
        docker volume create shadowbroker_backend_data || true
        docker run --rm \
            -v shadowbroker_backend_data:/volume \
            -v "${staging}/data:/backup" \
            alpine sh -c "rm -rf /volume/* && tar -xzf /backup/shadowbroker_backend_data.tar.gz -C /volume" || true
    fi
    
    # Clean up staging
    rm -rf "${staging}"
    
    # Restart services
    echo "Starting services back up..."
    systemctl start nginx hermes-gateway hermes-dashboard hermes-ui || true
    cd /root/Shadowbroker && docker compose up -d || true
    
    echo "Restoration completed successfully!"
}

# Parse argument
ACTION="${1:-}"
case "${ACTION}" in
    backup)
        do_backup
        ;;
    restore)
        do_restore "${2:-}"
        ;;
    *)
        show_help
        exit 1
        ;;
esac
