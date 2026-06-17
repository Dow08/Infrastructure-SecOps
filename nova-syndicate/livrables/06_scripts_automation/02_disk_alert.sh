#!/bin/bash
###############################################################################
# Nova Syndicate — Script d'automatisation #2
#
# Nom         : disk_alert.sh
# Objectif    : Surveillance de l'occupation disque des VMs critiques
#               avec alerte email automatique en cas de seuil dépassé.
# Auteur      : Dorian Poncelet — Nova Syndicate
# Date        : Mai 2026
# Version     : 1.0
# Référence   : NS-2026-006-script-02
#
# CONTEXTE
# --------
# Le saturation disque est l'une des causes majeures d'incidents évitables.
# Les VMs critiques (DC01, DB-01, Wazuh-01, File-01) doivent être surveillées
# en permanence. Le risque "R-13" du PCA/PRA documenté (disque plein sur
# VM hôte Proxmox) est mitigé par ce script.
#
# FONCTIONNEMENT
# --------------
# 1. Le script s'exécute toutes les 10 minutes via cron sur chaque VM
#    (déployé via Ansible / scp).
# 2. Il interroge `df -h` pour les partitions critiques.
# 3. Si l'occupation dépasse un seuil (par défaut 85%), il envoie :
#       a) Un email d'alerte à l'équipe IT.
#       b) Un log local + un événement vers Wazuh (via syslog).
# 4. Il garde une trace de la dernière alerte pour éviter le spam
#    (anti-flapping : on n'alerte qu'une fois par heure pour un même seuil).
#
# DÉPLOIEMENT
# -----------
# Copier le script sur chaque VM à surveiller :
#   scp disk_alert.sh user@vm:/usr/local/bin/
#   ssh user@vm 'chmod +x /usr/local/bin/disk_alert.sh'
#
# Ajouter au cron (root) :
#   crontab -e
#   */10 * * * * /usr/local/bin/disk_alert.sh >/dev/null 2>&1
#
# DÉPENDANCES
# -----------
# - mailutils (ou postfix configuré pour envoyer via Mail-01)
# - logger (présent par défaut sur Debian)
# - df, awk, grep (utilitaires standards)
#
# CODES DE RETOUR
# ---------------
# 0 : OK, tous les seuils respectés
# 1 : Erreur (configuration ou exécution)
# 2 : Alerte déclenchée (au moins une partition au-dessus du seuil)
###############################################################################

set -euo pipefail

# ─────────────────────────────────────────────────────────────
# Configuration (à adapter selon le contexte)
# ─────────────────────────────────────────────────────────────

# Seuil de déclenchement en pourcentage
WARN_THRESHOLD=80    # Avertissement
CRIT_THRESHOLD=90    # Critique (alerte immédiate)

# Email destinataire (équipe IT Nova Syndicate)
ALERT_RECIPIENT="it-alerts@nova.local"

# Identifiant SMTP (par défaut nom de l'hôte)
ALERT_SENDER="$(hostname -f)@nova.local"

# Fichier de tracking pour anti-spam (mémorise dernière alerte)
STATE_FILE="/var/lib/nova/disk_alert.state"
STATE_DIR=$(dirname "$STATE_FILE")

# Anti-spam : intervalle minimum entre 2 alertes (en secondes)
ALERT_COOLDOWN=3600   # 1 heure

# Partitions à surveiller (vide = toutes les partitions locales)
# Format : "/", "/var", "/home", etc.
# Si vide, toutes les partitions de type ext4/xfs/btrfs sont surveillées.
MONITORED_PATHS=()

# Tag syslog (pour intégration Wazuh)
SYSLOG_TAG="nova-disk-alert"

# ─────────────────────────────────────────────────────────────
# Fonctions utilitaires
# ─────────────────────────────────────────────────────────────

# Log local + syslog (Wazuh)
log() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
    logger -t "$SYSLOG_TAG" -p "user.$level" "$message"
}

# Vérification préalable
prereq_check() {
    # Vérification commandes nécessaires
    for cmd in df awk grep mail logger; do
        if ! command -v "$cmd" &>/dev/null; then
            log "error" "Commande requise absente : $cmd"
            exit 1
        fi
    done

    # Création répertoire state si absent
    if [[ ! -d "$STATE_DIR" ]]; then
        mkdir -p "$STATE_DIR"
        chmod 700 "$STATE_DIR"
    fi

    # Initialiser state file si absent
    if [[ ! -f "$STATE_FILE" ]]; then
        touch "$STATE_FILE"
        chmod 600 "$STATE_FILE"
    fi
}

# Détermine si on doit envoyer une alerte (anti-spam)
should_alert() {
    local partition="$1"
    local level="$2"
    local now
    now=$(date +%s)

    # Recherche de la dernière alerte pour cette partition/niveau
    local last_alert
    last_alert=$(grep "^${partition}|${level}|" "$STATE_FILE" 2>/dev/null | cut -d'|' -f3 || echo "0")

    if [[ -z "$last_alert" ]] || [[ "$last_alert" == "0" ]]; then
        return 0   # Première alerte = envoyer
    fi

    local elapsed=$((now - last_alert))
    if [[ "$elapsed" -ge "$ALERT_COOLDOWN" ]]; then
        return 0   # Cooldown passé = ré-envoyer
    fi

    return 1   # Sous cooldown = ne pas spammer
}

# Met à jour le state après envoi d'alerte
update_alert_state() {
    local partition="$1"
    local level="$2"
    local now
    now=$(date +%s)

    # Supprimer ancien enregistrement pour cette partition/niveau
    grep -v "^${partition}|${level}|" "$STATE_FILE" > "$STATE_FILE.tmp" 2>/dev/null || true
    echo "${partition}|${level}|${now}" >> "$STATE_FILE.tmp"
    mv "$STATE_FILE.tmp" "$STATE_FILE"
}

# Envoie un email d'alerte
send_alert_email() {
    local partition="$1"
    local usage="$2"
    local level="$3"

    local subject="[Nova Syndicate] [${level^^}] Disque saturé sur $(hostname) — ${partition}"
    local body
    body=$(cat <<EOF
ALERTE SATURATION DISQUE — Nova Syndicate

Hôte         : $(hostname -f)
Partition    : ${partition}
Occupation   : ${usage}%
Seuil franchi: ${level} (${WARN_THRESHOLD}% / ${CRIT_THRESHOLD}%)
Date         : $(date '+%Y-%m-%d %H:%M:%S %Z')

Détail des partitions :
$(df -h | head -20)

Top 10 plus gros dossiers de la partition :
$(du -hx --max-depth=3 "${partition}" 2>/dev/null | sort -rh | head -10)

Actions recommandées :
- Identifier la cause de la croissance (logs ? backup ? base de données ?)
- Nettoyer les fichiers temporaires : sudo apt clean
- Vérifier journaux : journalctl --vacuum-time=30d
- Vérifier core dumps : ls /var/crash
- Étendre la partition (LVM) si besoin durable

Cet email est généré automatiquement par disk_alert.sh.
Documenté dans le PCA Nova Syndicate — risque R-13.
EOF
)

    echo "$body" | mail -s "$subject" -a "From: $ALERT_SENDER" "$ALERT_RECIPIENT"
    log "warning" "Email d'alerte envoyé pour $partition ($usage%, niveau $level)"
}

# ─────────────────────────────────────────────────────────────
# Programme principal
# ─────────────────────────────────────────────────────────────

main() {
    prereq_check

    local exit_code=0
    local alerts_sent=0

    # Récupération des partitions à surveiller
    local partitions_list
    if [[ ${#MONITORED_PATHS[@]} -eq 0 ]]; then
        # Toutes les partitions locales (filtre les pseudo-FS)
        partitions_list=$(df -P -x tmpfs -x devtmpfs -x squashfs -x overlay \
                          | awk 'NR>1 {print $6}')
    else
        partitions_list=$(printf '%s\n' "${MONITORED_PATHS[@]}")
    fi

    # Parcours des partitions
    while IFS= read -r partition; do
        [[ -z "$partition" ]] && continue

        # Récupération du taux d'occupation
        local usage
        usage=$(df -P "$partition" | awk 'NR==2 {gsub(/%/,"",$5); print $5}')

        if ! [[ "$usage" =~ ^[0-9]+$ ]]; then
            log "warning" "Impossible de lire l'occupation de $partition"
            continue
        fi

        # Évaluation du niveau d'alerte
        if [[ "$usage" -ge "$CRIT_THRESHOLD" ]]; then
            log "error" "CRITIQUE : $partition est à $usage%"
            if should_alert "$partition" "critical"; then
                send_alert_email "$partition" "$usage" "critical"
                update_alert_state "$partition" "critical"
                ((alerts_sent++))
            fi
            exit_code=2
        elif [[ "$usage" -ge "$WARN_THRESHOLD" ]]; then
            log "warning" "AVERTISSEMENT : $partition est à $usage%"
            if should_alert "$partition" "warning"; then
                send_alert_email "$partition" "$usage" "warning"
                update_alert_state "$partition" "warning"
                ((alerts_sent++))
            fi
            exit_code=2
        else
            log "info" "OK : $partition à $usage%"
        fi
    done <<< "$partitions_list"

    log "info" "Exécution terminée. Alertes envoyées : $alerts_sent"
    exit "$exit_code"
}

# Point d'entrée
main "$@"
