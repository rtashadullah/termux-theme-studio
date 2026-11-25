#!/data/data/com.termux/files/usr/bin/bash
# Termux Theme Studio — one-command install (Termux-e chalao)
#   bash install.sh neon-modern
#   bash install.sh minimal-dark
#   bash install.sh hacker-green

set -e
THEME="${1:-neon-modern}"
cd "$(dirname "$0")"

pkg install python -y 2>/dev/null || true
mkdir -p ~/.termux

python termux_theme.py apply "$THEME"

echo ""
echo "Done! Theme: $THEME"
echo "Change korte: python termux_theme.py list"
