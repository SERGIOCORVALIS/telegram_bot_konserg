#!/bin/bash
# Quick Railway env setup. Reads secrets from the environment or a local .env file.
# Usage: export TELEGRAM_BOT_TOKEN=... OPENROUTER_API_KEY=... && ./railway-setup.sh
#    or: set -a && source .env && set +a && ./railway-setup.sh

set -euo pipefail

echo "Setting Railway environment variables..."
echo ""

if ! command -v railway &> /dev/null; then
    echo "Railway CLI is not installed."
    echo "Install: npm i -g @railway/cli"
    echo "See RAILWAY_QUICK_FIX_RU.md for details."
    exit 1
fi

if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

: "${TELEGRAM_BOT_TOKEN:?Set TELEGRAM_BOT_TOKEN in the environment or .env}"
: "${OPENROUTER_API_KEY:?Set OPENROUTER_API_KEY in the environment or .env}"

echo "Railway CLI found"
echo ""
echo "Adding required variables..."

railway variables set TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
railway variables set OPENROUTER_API_KEY="$OPENROUTER_API_KEY"

echo ""
echo "Adding optional additional OpenRouter keys (if present)..."

for i in 1 2 3 4 5 6 7 8 9; do
    var="OPENROUTER_API_KEY_$i"
    if [[ -n "${!var:-}" ]]; then
        railway variables set "$var=${!var}"
    fi
done

echo ""
echo "Adding optional app settings..."

railway variables set APP_NAME="${APP_NAME:-AI Assistant Bot}"
if [[ -n "${APP_PUBLIC_URL:-}" ]]; then
    railway variables set APP_PUBLIC_URL="$APP_PUBLIC_URL"
fi

echo ""
echo "Variables submitted. Railway should restart the service shortly."
echo "Check Railway Dashboard → Logs."
echo ""
