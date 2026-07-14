#!/bin/bash
# setup.sh - Check dependencies for all platforms

OS="$(uname -s)"

echo "🚀 Checking dependencies for $OS..."

check_cmd() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ $1 not found. Install with:"
        echo "   $2"
        exit 1
    fi
}

check_file() {
    if [ ! -f "$1" ]; then
        echo "❌ $1 not found in current directory"
        exit 1
    fi
}

# Check SSH
check_cmd ssh "Install openssh-client"

# Check Python
case "$OS" in
    Linux*)
        check_cmd python3 "sudo dnf install python3 / sudo apt install python3"
        check_cmd notify-send "sudo dnf install libnotify / sudo apt install libnotify-bin"
        check_file "remarkable.sh"
        ;;
    Darwin*)
        check_cmd python3 "brew install python3"
        check_file "remarkable_mac.py"
        
        # Check pyobjc
        python3 -c "import Quartz" 2>/dev/null || {
            echo "❌ pyobjc not found. Install with:"
            echo "   pip3 install pyobjc"
            exit 1
        }
        ;;
    MINGW*|CYGWIN*|MSYS*)
        check_cmd python "Install Python from python.org"
        check_file "remarkable_windows.py"
        
        # Check pynput
        python -c "import pynput" 2>/dev/null || {
            echo "❌ pynput not found. Install with:"
            echo "   pip install pynput"
            exit 1
        }
        ;;
    *)
        echo "❌ Unsupported OS: $OS"
        exit 1
        ;;
esac

# Check keyboard.conf
check_file "keyboard.conf"

echo "✅ All dependencies found!"
echo ""
echo "Next steps:"
echo "  1. Edit keyboard.conf with your keyboard name"
echo "  2. Install on reMarkable: ssh remarkable './install.sh'"
echo "  3. Run: ./remarkable.sh (Linux) or python3 remarkable_mac.py (macOS)"
