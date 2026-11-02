#!/bin/bash
# ============================================================================
# AeroByte Academy — Oracle Cloud (OCI) Setup Script
# Run on a fresh Ubuntu 22.04+ ARM or AMD instance (Always Free eligible)
# Usage: chmod +x setup.sh && sudo ./setup.sh
# ============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()   { echo -e "${GREEN}[OK]${NC}    $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail() { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

# ── 1. System updates ──────────────────────────────────────────────────────
log "Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq
ok "System updated"

# ── 2. Install Docker ──────────────────────────────────────────────────────
if command -v docker &>/dev/null; then
    ok "Docker already installed: $(docker --version)"
else
    log "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
    ok "Docker installed: $(docker --version)"
fi

# Add current user to docker group (if not root)
if [ "${SUDO_USER:-}" ]; then
    usermod -aG docker "$SUDO_USER"
    log "Added $SUDO_USER to docker group (re-login to take effect)"
fi

# ── 3. Install Docker Compose plugin ──────────────────────────────────────
if docker compose version &>/dev/null; then
    ok "Docker Compose already available: $(docker compose version --short)"
else
    log "Installing Docker Compose plugin..."
    apt-get install -y -qq docker-compose-plugin
    ok "Docker Compose installed: $(docker compose version --short)"
fi

# ── 4. Open firewall ports (iptables — OCI uses iptables, not ufw) ────────
log "Configuring iptables firewall rules..."
iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80  -j ACCEPT 2>/dev/null || true
iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT 2>/dev/null || true
# Persist rules
if command -v netfilter-persistent &>/dev/null; then
    netfilter-persistent save
elif [ -f /etc/iptables/rules.v4 ]; then
    iptables-save > /etc/iptables/rules.v4
fi
ok "Firewall: ports 80 and 443 opened"

# ── 5. Clone repository ───────────────────────────────────────────────────
APP_DIR="/opt/aerobyte-academy"
REPO_URL="https://github.com/Langhour/Aerobyte-Academy-2.git"

if [ -d "$APP_DIR" ]; then
    warn "$APP_DIR already exists — pulling latest changes"
    cd "$APP_DIR" && git pull
else
    log "Cloning repository..."
    git clone "$REPO_URL" "$APP_DIR"
fi
cd "$APP_DIR"
ok "Repository ready at $APP_DIR"

# ── 6. Set up environment ─────────────────────────────────────────────────
ENV_FILE="$APP_DIR/oracle-cloud/.env"
if [ ! -f "$ENV_FILE" ]; then
    cp "$APP_DIR/oracle-cloud/.env.example" "$ENV_FILE"
    warn "Created $ENV_FILE from template — edit it before deploying!"
    warn "  nano $ENV_FILE"
fi

# ── 7. Print next steps ───────────────────────────────────────────────────
PUBLIC_IP=$(curl -s -4 ifconfig.me 2>/dev/null || echo "UNKNOWN")

echo ""
echo "============================================================================"
echo -e "${GREEN}  ✅  Server setup complete!${NC}"
echo "============================================================================"
echo ""
echo "  Public IP:  $PUBLIC_IP"
echo "  App Dir:    $APP_DIR"
echo "  Compose:    $APP_DIR/oracle-cloud/docker-compose.yaml"
echo ""
echo "  ┌─────────────────────────────────────────────────────────────────────┐"
echo "  │  NEXT STEPS:                                                       │"
echo "  │                                                                    │"
echo "  │  1. Edit the .env file:                                            │"
echo "  │     nano $APP_DIR/oracle-cloud/.env                                │"
echo "  │                                                                    │"
echo "  │  2. Set FRONTEND_URL to your domain or use nip.io:                 │"
echo "  │     FRONTEND_URL=https://${PUBLIC_IP}.nip.io                       │"
echo "  │                                                                    │"
echo "  │  3. Update the Caddyfile domain:                                   │"
echo "  │     sed -i 's/\$DOMAIN/${PUBLIC_IP}.nip.io/' \\                     │"
echo "  │       $APP_DIR/oracle-cloud/Caddyfile                              │"
echo "  │                                                                    │"
echo "  │  4. Build and start:                                               │"
echo "  │     cd $APP_DIR                                                    │"
echo "  │     docker compose -f oracle-cloud/docker-compose.yaml \\           │"
echo "  │       --env-file oracle-cloud/.env up -d --build                   │"
echo "  │                                                                    │"
echo "  │  5. Check status:                                                  │"
echo "  │     docker compose -f oracle-cloud/docker-compose.yaml ps          │"
echo "  │     docker compose -f oracle-cloud/docker-compose.yaml logs -f     │"
echo "  │                                                                    │"
echo "  │  IMPORTANT — OCI Security List:                                    │"
echo "  │  In OCI Console → Networking → VCN → Security Lists,              │"
echo "  │  add Ingress Rules for ports 80 (HTTP) and 443 (HTTPS)            │"
echo "  │  from source 0.0.0.0/0.                                           │"
echo "  └─────────────────────────────────────────────────────────────────────┘"
echo ""
