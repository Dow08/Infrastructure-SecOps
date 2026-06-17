#!/usr/bin/env bash
# Automated script to backup Hermes Agent's "soul" (memories, config, and state.db)
# and push it to the GitHub repository. Includes pre-commit secure redaction.

set -euo pipefail

REPO_DIR="/root/VPS_Jarod_AI_et_OSINT"
SOUL_DIR="${REPO_DIR}/soul"
LOG_FILE="/root/vps-backups/backup-soul.log"

mkdir -p "$(dirname "${LOG_FILE}")"
exec > >(tee -ia "${LOG_FILE}") 2>&1

echo "===================================================="
echo "Starting Hermes Soul Backup: $(date +'%Y-%m-%d %H:%M:%S')"
echo "===================================================="

# 1. Staging and copying soul components
echo "Creating soul directory..."
mkdir -p "${SOUL_DIR}"
mkdir -p "${SOUL_DIR}/memories"

echo "Copying memories (USER.md & MEMORY.md)..."
cp /root/.hermes/memories/USER.md "${SOUL_DIR}/memories/USER.md" || true
cp /root/.hermes/memories/MEMORY.md "${SOUL_DIR}/memories/MEMORY.md" || true

echo "Copying configuration (config.yaml)..."
cp /root/.hermes/config.yaml "${SOUL_DIR}/config.yaml" || true

echo "Copying conversation history (state.db)..."
# Using sqlite3 backup command to prevent database lock issues
if command -v sqlite3 &> /dev/null; then
    sqlite3 /root/.hermes/state.db ".backup '${SOUL_DIR}/state.db'"
else
    cp /root/.hermes/state.db "${SOUL_DIR}/state.db" || true
fi

# 2. RUN SECURE SCANNER (SOUL SHIELD)
echo "Executing security scan (Soul Shield) to prevent credential leaks..."
if [[ -f "${REPO_DIR}/soul-shield.py" ]]; then
    python3 "${REPO_DIR}/soul-shield.py"
else
    echo "Warning: soul-shield.py not found in ${REPO_DIR}. Skipping secret redaction scan."
fi

# 3. Check git remote configuration
cd "${REPO_DIR}"
REMOTE_URL=$(git remote get-url origin || echo "")

if [[ -z "${REMOTE_URL}" ]]; then
    echo "Error: No git remote 'origin' configured in ${REPO_DIR}."
    exit 1
fi

if [[ "${REMOTE_URL}" =~ ^https:// ]]; then
    echo "Warning: Git remote is configured over HTTPS."
    echo "To automate git push seamlessly without being prompted for credentials,"
    echo "please switch the remote to SSH:"
    echo "  git remote set-url origin git@github.com:Dow08/VPS_Jarod_AI_et_OSINT.git"
    echo "And ensure your SSH public key (~/.ssh/id_ed25519.pub) is added to GitHub."
fi

# 4. Commit and push
echo "Staging files in Git..."
git add soul/

if git diff-index --quiet HEAD --; then
    echo "No changes in soul state. Nothing to push."
else
    echo "Committing soul state..."
    # Set local git identity for this repository if not set globally
    git config user.name "Jarod AI"
    git config user.email "jarod@crfdow08.tech"
    
    git commit -m "Auto-backup soul: $(date +'%Y-%m-%d %H:%M:%S')"
    
    echo "Pushing changes to GitHub..."
    if git push origin main; then
        echo "Soul backup pushed successfully!"
    else
        echo "Error: Failed to push to GitHub. Check SSH keys / permissions."
        exit 1
    fi
fi

echo "Backup finished at: $(date +'%Y-%m-%d %H:%M:%S')"
