#!/usr/bin/env bash
# Automated replication and deployment script for the VPS environment.
# Run this on a clean Ubuntu 24.04 VPS as root to automatically set up
# all services, dependencies, repositories, services, and Nginx.

set -euo pipefail

# Invariants
HUB_REPO="https://github.com/Dow08/Projet_G.R.C_Syntaris_LABS.git"
WORK_REPO="https://github.com/outsourc-e/hermes-workspace.git"
SHADOW_REPO="https://github.com/BigBodyCobain/Shadowbroker.git"

echo "===================================================="
echo "    VPS Automated Replication & Setup Installer     "
echo "===================================================="

# 1. Check root
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root." 
   exit 1
fi

# 2. Prompt for user variables
echo "Please enter the configuration details for this node:"
read -p "Hub/Main Domain (e.g. crfdow08.tech): " HUB_DOMAIN
read -p "Hermes Subdomain (e.g. hermes.crfdow08.tech): " HERMES_DOMAIN
read -p "Shadowbroker Subdomain (e.g. shadowbroker.crfdow08.tech): " SHADOWBROKER_DOMAIN
read -p "Set username for Nginx Basic Auth: " AUTH_USER
read -sp "Set password for Nginx Basic Auth: " AUTH_PASS
echo ""

# 3. Update & Install system packages
echo "Updating package lists and upgrading packages..."
apt-get update && apt-get upgrade -y
apt-get install -y curl git tmux ufw nginx apache2-utils python3-certbot-nginx python3-pip python3-venv build-essential

# 4. Install Docker & Docker Compose
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# 5. Install Node.js & pnpm
if ! command -v node &> /dev/null; then
    echo "Installing Node.js (via NodeSource LTS)..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm..."
    npm install -g pnpm
fi

# 6. Clone Repositories
echo "Cloning repositories to target folders..."
mkdir -p /workspace
if [[ ! -d "/workspace/.git" ]]; then
    git clone "${HUB_REPO}" /workspace
fi

if [[ ! -d "/root/hermes-workspace/.git" ]]; then
    git clone "${WORK_REPO}" /root/hermes-workspace
fi

if [[ ! -d "/root/Shadowbroker/.git" ]]; then
    git clone "${SHADOW_REPO}" /root/Shadowbroker
fi

# 7. Create static hub files
echo "Setting up static hub folder..."
mkdir -p /var/www/hub
if [[ ! -f "/var/www/hub/index.html" ]]; then
    if [[ -f "/workspace/index.html" ]]; then
        cp /workspace/index.html /var/www/hub/
    else
        echo "<h1>Portal Hub {{HUB_DOMAIN}}</h1>" > /var/www/hub/index.html
    fi
fi
chown -R www-data:www-data /var/www/hub

# 8. Install Hermes Agent
echo "Installing Hermes Agent..."
if ! command -v hermes &> /dev/null; then
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
fi

# 9. Copy and register Systemd units
echo "Installing Systemd service files..."
cp systemd/hermes-gateway.service.template /etc/systemd/system/hermes-gateway.service
cp systemd/hermes-dashboard.service.template /etc/systemd/system/hermes-dashboard.service

# Render hermes-ui template
sed "s/{{HERMES_DOMAIN}}/${HERMES_DOMAIN}/g" systemd/hermes-ui.service.template > /etc/systemd/system/hermes-ui.service

systemctl daemon-reload
systemctl enable hermes-gateway hermes-dashboard hermes-ui
systemctl start hermes-gateway

# 10. Install packages in hermes-workspace
echo "Installing dependencies for hermes-workspace..."
cd /root/hermes-workspace
pnpm install
systemctl start hermes-ui

# 11. Configure Nginx and basic auth
echo "Configuring Nginx reverse proxy..."
# Create Basic Auth htpasswd file
htpasswd -b -c /etc/nginx/.htpasswd_hermes "${AUTH_USER}" "${AUTH_PASS}"

# Render Nginx configuration template
sed -e "s/{{HUB_DOMAIN}}/${HUB_DOMAIN}/g" \
    -e "s/{{HERMES_DOMAIN}}/${HERMES_DOMAIN}/g" \
    -e "s/{{SHADOWBROKER_DOMAIN}}/${SHADOWBROKER_DOMAIN}/g" \
    nginx/cyberstation.template > /etc/nginx/sites-available/cyberstation

ln -sf /etc/nginx/sites-available/cyberstation /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx

# 12. Create .env examples
echo "Preparing environment variable file templates..."
mkdir -p /root/.hermes
if [[ ! -f "/root/.hermes/.env" ]]; then
    cat <<EOT > /root/.hermes/.env
# Hermes Agent Global Configuration Secrets
# Choose your active model provider and input your API keys below.
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
EOT
    echo "Created /root/.hermes/.env template"
fi

if [[ ! -f "/root/hermes-workspace/.env" ]]; then
    cat <<EOT > /root/hermes-workspace/.env
# Hermes Workspace Web UI Env File
HERMES_HOME=/root/.hermes
HERMES_WORKSPACE_DIR=/workspace
HERMES_API_URL=http://127.0.0.1:8642
HERMES_DASHBOARD_URL=http://127.0.0.1:9119
# Set a unique session password for the web interface
HERMES_PASSWORD=some_secure_password
EOT
    echo "Created /root/hermes-workspace/.env template"
fi

if [[ ! -f "/root/Shadowbroker/.env" ]]; then
    cp /root/Shadowbroker/.env.example /root/Shadowbroker/.env || true
    echo "Created /root/Shadowbroker/.env from example"
fi

# 13. Start Shadowbroker containers
echo "Launching Shadowbroker Docker containers..."
cd /root/Shadowbroker
docker compose up -d

# 14. Configure Let's Encrypt SSL
echo "----------------------------------------------------"
echo "Setup is almost complete! "
echo "To obtain Let's Encrypt certificates, please execute:"
echo "  certbot --nginx -d ${HUB_DOMAIN} -d www.${HUB_DOMAIN} -d ${HERMES_DOMAIN} -d www.${HERMES_DOMAIN} -d ${SHADOWBROKER_DOMAIN} -d www.${SHADOWBROKER_DOMAIN}"
echo "----------------------------------------------------"
echo ""
echo "Installation complete! All systemd services are enabled and active."
echo "Please don't forget to fill in your API keys in:"
echo "  /root/.hermes/.env"
echo "  /root/hermes-workspace/.env"
echo "  /root/Shadowbroker/.env"
echo ""
echo "Use the backup-restore.sh utility script to restore any existing state backups."
