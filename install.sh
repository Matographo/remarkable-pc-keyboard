#!/bin/bash
# install.sh - Install rmiject on reMarkable
set -e

REPO="matographo/remarkable-pc-keyboard"
INSTALL_DIR="/home/root"
BINARY="rmiject"

echo "🚀 Installing remarkable-pc-keyboard on reMarkable..."

# Check if we're on the reMarkable
if ! grep -q "remarkable" /etc/hostname 2>/dev/null; then
    echo "❌ This script must run on the reMarkable Paper Pro!"
    echo "   Use: ssh remarkable './install.sh'"
    exit 1
fi

# Download latest release
echo "📥 Downloading latest version..."
RELEASE_URL="https://github.com/${REPO}/releases/latest/download/${BINARY}"
curl -L -o "/tmp/${BINARY}" "${RELEASE_URL}"
chmod +x "/tmp/${BINARY}"

# Move to install directory
echo "📦 Installing to ${INSTALL_DIR}/..."
mv "/tmp/${BINARY}" "${INSTALL_DIR}/${BINARY}"

echo "✅ Installation complete!"
echo "   Binary: ${INSTALL_DIR}/${BINARY}"
echo ""
echo "Next steps:"
echo "  1. On PC: Run ./remarkable.sh (Linux) or python3 remarkable_mac.py (macOS)"
echo "  2. Press F13 to return to PC"
