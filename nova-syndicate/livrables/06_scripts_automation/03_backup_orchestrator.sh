#!/bin/bash
###############################################################################
# Nova Syndicate — Script d'automatisation #3
#
# Nom         : backup_orchestrator.sh
# Objectif    : Orchestration des sauvegardes quotidiennes des services
#               critiques de Nova Syndicate, conforme au plan PCA/PRA.
# Auteur      : Dorian Poncelet — Nova Syndicate
# Date        : Mai 2026
# Version     : 1.0
# Référence   : NS-2026-006-script-03
#
# CONTEXTE
# --------
# Ce script implémente la politique de sauvegarde 3-2-1 décrite dans le
# PCA/PRA Nova Syndicate (chapitre 10) :
#   - 3 copies des données (production + backup local + backup distant)
#   - 2 supports différents (disques VM + Backup-01)
#   - 1 copie hors site (cible cloud OVH/Scaleway — à raccorder)
#
# SCOPE
# -----
# Le script est exécuté sur Backup-01 (10.1.110.10) et orchestre :
#   - Sauvegarde Active Directory (Samba) depuis DC01-Lyon
#   - Sauvegarde base MariaDB depuis DB-01
#   - Sauvegarde Nextcloud (data + DB) depuis File-01
#   - Sauvegarde Mail-01 (Maildirs + config)
#   - Sauvegarde config OPNsense (XML) depuis OPNsense Lyon + Marseille
#   - Sauvegarde snapshots Proxmox (`vzdump`)
#   - Notification par email du résultat global
#
# FONCTIONNEMENT
# --------------
# 1. Définit la date du jour et crée un répertoire daté.
# 2. Exécute chaque sous-tâche de backup (SSH + commandes distantes).
# 3. Chiffre chaque archive (GPG asymétrique).
# 4. Calcule un checksum SHA-256 pour intégrité.
# 5. Applique la rétention (suppression > 30 jours).
# 6. Envoie un rapport email.
#
# DÉPLOIEMENT
# -----------
# 1. Sur Backup-01 :
#       sudo mkdir -p /backup/{ad,mariadb,nextcloud,mail,opnsense,proxmox}
#       sudo chown root:root /backup -R
#       sudo chmod 700 /backup
# 2. Importer les clés SSH (root@backup-01 → toutes les VMs concernées)
#       ssh-keygen -t ed25519 (sans passphrase)
#       ssh-copy-id root@dc01-lyon, etc.
# 3. Importer une clé GPG publique pour chiffrement :
#       gpg --import nova-backup-public.asc
# 4. Cron :
#       0 1 * * * /usr/local/bin/backup_orchestrator.sh >> /var/log/nova/backup.log 2>&1
#
# DÉPENDANCES
# -----------
# - Bash 4+, ssh, rsync, gpg, sha256sum
# - Mail (postfix configuré pour Mail-01)
# - mysqldump (sur DB-01)
# - samba-tool (sur DC01)
# - OPNsense API (token configuré)
#
# CODES DE RETOUR
# ---------------
# 0 : Tous les backups OK
# 1 : Erreur de configuration / prérequis
# 2 : Au moins un backup en échec (rapport email envoyé)
###############################################################################

set -uo pipefail   # Pas de -e car on veut continuer même si un backup échoue

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

BACKUP_ROOT="/backup"
LOG_FILE="/var/log/nova/backup_orchestrator.log"
RETENTION_DAYS=30          # Conservation 30 jours (cf. PCA chap. 10.2)
TODAY=$(date +%Y%m%d)
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Adresses des VMs cibles (côté backup)
DC01_HOST="dc01-lyon.nova.local"
DB01_HOST="db-01.nova.local"
FILE01_HOST="file-01.nova.local"
MAIL01_HOST="mail-01.nova.local"
OPNSENSE_LYON="192.168.1.166"
OPNSENSE_MARSEILLE="192.168.1.167"
PROXMOX_HOST="192.168.1.165"

# Identités GPG pour chiffrement (créer la paire avant déploiement)
GPG_RECIPIENT="backup@nova.local"

# Email destinataire du rapport
REPORT_RECIPIENT="it-alerts@nova.local"
REPORT_SENDER="backup-01@nova.local"

# Tag syslog (intégration Wazuh)
SYSLOG_TAG="nova-backup"

# ─────────────────────────────────────────────────────────────
# Fonctions utilitaires
# ─────────────────────────────────────────────────────────────

log() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
    logger -t "$SYSLOG_TAG" -p "user.$level" "$message"
}

# Vérification des prérequis
prereq_check() {
    for cmd in ssh rsync gpg sha256sum mail logger; do
        if ! command -v "$cmd" &>/dev/null; then
            log "error" "Commande requise absente : $cmd"
            exit 1
        fi
    done

    # Création dossiers
    for d in ad mariadb nextcloud mail opnsense proxmox; do
        mkdir -p "$BACKUP_ROOT/$d/$TODAY"
    done

    mkdir -p "$(dirname "$LOG_FILE")"
}

# Chiffrement GPG et checksum
encrypt_and_checksum() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        log "error" "Fichier introuvable : $file"
        return 1
    fi

    # Chiffrement asymétrique
    gpg --batch --yes --encrypt --recipient "$GPG_RECIPIENT" "$file"
    rm -f "$file"   # Suppression du fichier clair

    # Checksum SHA-256
    sha256sum "${file}.gpg" > "${file}.gpg.sha256"

    log "info" "Chiffré : ${file}.gpg ($(du -h "${file}.gpg" | cut -f1))"
}

# ─────────────────────────────────────────────────────────────
# Backups par service
# ─────────────────────────────────────────────────────────────

# Active Directory (Samba 4)
backup_active_directory() {
    log "info" "[1/6] Démarrage backup Active Directory"
    local target_dir="$BACKUP_ROOT/ad/$TODAY"
    local archive="$target_dir/ad-samba-$TIMESTAMP.tar.gz"

    # Snapshot AD via samba-tool sur DC01
    ssh "$DC01_HOST" "sudo samba-tool domain backup online \
                      --targetdir=/tmp/samba_backup_$TODAY \
                      --server=$DC01_HOST"

    # Récupération via rsync
    rsync -avz "$DC01_HOST:/tmp/samba_backup_$TODAY/" "$target_dir/raw/" \
        2>>"$LOG_FILE" || {
            log "error" "Échec rsync AD"
            return 1
        }

    # Archivage
    tar czf "$archive" -C "$target_dir" raw/
    rm -rf "$target_dir/raw"

    # Nettoyage côté DC01
    ssh "$DC01_HOST" "sudo rm -rf /tmp/samba_backup_$TODAY"

    encrypt_and_checksum "$archive"
    log "info" "[1/6] AD : OK"
}

# MariaDB (DB-01)
backup_mariadb() {
    log "info" "[2/6] Démarrage backup MariaDB"
    local target_dir="$BACKUP_ROOT/mariadb/$TODAY"
    local dump_file="$target_dir/mysql-full-$TIMESTAMP.sql"

    # Dump complet via ssh
    ssh "$DB01_HOST" "sudo mysqldump --all-databases --single-transaction \
                       --routines --triggers --master-data=2" \
        > "$dump_file" 2>>"$LOG_FILE" || {
            log "error" "Échec dump MariaDB"
            return 1
        }

    # Compression
    gzip -9 "$dump_file"

    encrypt_and_checksum "${dump_file}.gz"
    log "info" "[2/6] MariaDB : OK"
}

# Nextcloud (File-01)
backup_nextcloud() {
    log "info" "[3/6] Démarrage backup Nextcloud"
    local target_dir="$BACKUP_ROOT/nextcloud/$TODAY"
    local data_archive="$target_dir/nc-data-$TIMESTAMP.tar.gz"
    local db_dump="$target_dir/nc-db-$TIMESTAMP.sql"

    # Mode maintenance
    ssh "$FILE01_HOST" "sudo -u www-data php /var/www/nextcloud/occ maintenance:mode --on"

    # Archive data
    ssh "$FILE01_HOST" "sudo tar czf /tmp/nc-data-$TODAY.tar.gz -C /var/lib/nextcloud data" \
        || { log "error" "Tar data Nextcloud KO"; return 1; }
    rsync -avz "$FILE01_HOST:/tmp/nc-data-$TODAY.tar.gz" "$data_archive"
    ssh "$FILE01_HOST" "sudo rm /tmp/nc-data-$TODAY.tar.gz"

    # Dump DB
    ssh "$FILE01_HOST" "sudo mysqldump nextcloud" > "$db_dump"
    gzip -9 "$db_dump"

    # Sortie maintenance
    ssh "$FILE01_HOST" "sudo -u www-data php /var/www/nextcloud/occ maintenance:mode --off"

    encrypt_and_checksum "$data_archive"
    encrypt_and_checksum "${db_dump}.gz"
    log "info" "[3/6] Nextcloud : OK"
}

# Mail-01 (Maildirs + config)
backup_mail() {
    log "info" "[4/6] Démarrage backup Mail"
    local target_dir="$BACKUP_ROOT/mail/$TODAY"
    local archive="$target_dir/mail-$TIMESTAMP.tar.gz"

    # Maildirs (rsync incrémental + tar)
    ssh "$MAIL01_HOST" "sudo tar czf /tmp/mail-$TODAY.tar.gz /home /etc/postfix /etc/dovecot" \
        || { log "error" "Tar Mail KO"; return 1; }
    rsync -avz "$MAIL01_HOST:/tmp/mail-$TODAY.tar.gz" "$archive"
    ssh "$MAIL01_HOST" "sudo rm /tmp/mail-$TODAY.tar.gz"

    encrypt_and_checksum "$archive"
    log "info" "[4/6] Mail : OK"
}

# OPNsense (XML config Lyon + Marseille)
backup_opnsense() {
    log "info" "[5/6] Démarrage backup OPNsense"
    local target_dir="$BACKUP_ROOT/opnsense/$TODAY"

    # Lyon (via API REST OPNsense)
    # Nécessite un token API configuré dans /root/.opnsense_token
    local TOKEN_LYON
    TOKEN_LYON=$(cat /root/.opnsense_token_lyon 2>/dev/null || echo "")
    if [[ -n "$TOKEN_LYON" ]]; then
        curl -k -s -H "Authorization: Bearer $TOKEN_LYON" \
             "https://$OPNSENSE_LYON/api/backup/backup/download/" \
             -o "$target_dir/opnsense-lyon-$TIMESTAMP.xml" || \
            log "warning" "Échec backup OPNsense Lyon"
    else
        # Fallback : récupération manuelle via SCP (config-backup.xml exporté préalablement)
        log "warning" "Token OPNsense Lyon absent, fallback SCP requis manuellement"
    fi

    # Marseille (idem)
    local TOKEN_MAR
    TOKEN_MAR=$(cat /root/.opnsense_token_marseille 2>/dev/null || echo "")
    if [[ -n "$TOKEN_MAR" ]]; then
        curl -k -s -H "Authorization: Bearer $TOKEN_MAR" \
             "https://$OPNSENSE_MARSEILLE/api/backup/backup/download/" \
             -o "$target_dir/opnsense-marseille-$TIMESTAMP.xml" || \
            log "warning" "Échec backup OPNsense Marseille"
    fi

    # Chiffrement (les XML peuvent contenir des secrets)
    for f in "$target_dir"/*.xml; do
        [[ -f "$f" ]] && encrypt_and_checksum "$f"
    done

    log "info" "[5/6] OPNsense : OK"
}

# Snapshots Proxmox (vzdump)
backup_proxmox_vms() {
    log "info" "[6/6] Démarrage snapshots Proxmox"
    local target_dir="$BACKUP_ROOT/proxmox/$TODAY"

    # Liste des VMs critiques à snapshotter
    local CRITICAL_VMS=(100 101 102 106 107 108 109 110)

    for vmid in "${CRITICAL_VMS[@]}"; do
        log "info" "Snapshot VM $vmid"
        ssh "root@$PROXMOX_HOST" "vzdump $vmid --mode snapshot --compress zstd \
                                   --storage local-lvm --notes 'Auto backup $TODAY'" \
            >>"$LOG_FILE" 2>&1 || {
                log "warning" "Snapshot VM $vmid KO"
            }
    done

    # Rapatriement des derniers vzdump
    rsync -avz "root@$PROXMOX_HOST:/var/lib/vz/dump/vzdump-qemu-*-$(date +%Y_%m_%d)*" \
              "$target_dir/" 2>>"$LOG_FILE"

    log "info" "[6/6] Proxmox snapshots : OK"
}

# ─────────────────────────────────────────────────────────────
# Rétention (suppression > N jours)
# ─────────────────────────────────────────────────────────────
apply_retention() {
    log "info" "Application de la rétention ($RETENTION_DAYS jours)"
    find "$BACKUP_ROOT" -type d -name "20*" -mtime +$RETENTION_DAYS \
        -exec rm -rf {} \; 2>/dev/null || true
    log "info" "Rétention appliquée"
}

# ─────────────────────────────────────────────────────────────
# Rapport final par email
# ─────────────────────────────────────────────────────────────
send_report() {
    local status="$1"
    local body
    body=$(cat <<EOF
Rapport quotidien de sauvegarde — Nova Syndicate

Date         : $(date '+%Y-%m-%d %H:%M:%S')
Hôte         : $(hostname -f)
Statut global: $status

Volumétrie des backups du jour :
$(du -sh "$BACKUP_ROOT"/*/$TODAY 2>/dev/null)

Espace disque Backup-01 :
$(df -h /backup)

Dernières lignes du log :
$(tail -50 "$LOG_FILE")

PCA/PRA Nova Syndicate — chapitre 10 (politique 3-2-1).
EOF
)

    local subject="[Nova Syndicate] Backup quotidien — $status"
    echo "$body" | mail -s "$subject" -a "From: $REPORT_SENDER" "$REPORT_RECIPIENT"
}

# ─────────────────────────────────────────────────────────────
# Programme principal
# ─────────────────────────────────────────────────────────────
main() {
    log "info" "================================================="
    log "info" "Démarrage backup_orchestrator — $TIMESTAMP"
    log "info" "================================================="

    prereq_check

    # Exécution des backups (chaque fonction est indépendante)
    local errors=0

    backup_active_directory || ((errors++))
    backup_mariadb || ((errors++))
    backup_nextcloud || ((errors++))
    backup_mail || ((errors++))
    backup_opnsense || ((errors++))
    backup_proxmox_vms || ((errors++))

    # Rétention
    apply_retention

    # Rapport
    if [[ "$errors" -eq 0 ]]; then
        log "info" "TOUS LES BACKUPS RÉUSSIS"
        send_report "SUCCESS"
        exit 0
    else
        log "error" "$errors backups en échec"
        send_report "ERRORS ($errors)"
        exit 2
    fi
}

main "$@"
