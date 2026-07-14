#!/bin/bash
# toggle-remarkable.sh - Works on all platforms

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/keyboard.conf"

# Detect OS
OS="$(uname -s)"

case "$OS" in
    Linux*)  SCRIPT="${SCRIPT_DIR}/remarkable.sh" ;;
    Darwin*) SCRIPT="python3 ${SCRIPT_DIR}/remarkable_mac.py" ;;
    MINGW*|CYGWIN*|MSYS*) SCRIPT="python ${SCRIPT_DIR}/remarkable_windows.py" ;;
    *)       echo "❌ Unsupported OS: $OS"; exit 1 ;;
esac

PID=$(pgrep -f "$SCRIPT" 2>/dev/null || pgrep -f "remarkable" 2>/dev/null)

if [ -z "$PID" ]; then
    echo "🚀 Starting connection to reMarkable..."
    ${SCRIPT} &
else
    echo "🛑 Stopping connection..."
    pkill -f "remarkable" 2>/dev/null || true
    pkill -f "ssh.*${REMARKABLE_HOST}" 2>/dev/null || true
    notify-send -u normal -i computer "💻 PC Mode" "Connection closed!" 2>/dev/null || echo "✅ Disconnected"
fi
