#!/bin/bash
# remarkable.sh - Linux version
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/keyboard.conf"

# Find keyboard
EVENT_DEV=$(ls -l /dev/input/by-id/ 2>/dev/null | grep -i "$KEYBOARD_NAME" | grep -- "-event-kbd" | awk '{print $NF}' | sed 's#.*/##' | head -n 1)

if [ -z "$EVENT_DEV" ]; then
    notify-send -u critical -i dialog-error "❌ Keyboard Error" "Keyboard '${KEYBOARD_NAME}' not found!"
    echo "Available keyboards:"
    ls /dev/input/by-id/ | grep -i kbd
    exit 1
fi

notify-send -u normal -i input-keyboard "📱 reMarkable active" "Keyboard disconnected. (Press ${HOTKEY_NAME} to return)"

python3 -c "
import os, sys, fcntl, struct

dev_path = f'/dev/input/${EVENT_DEV}'
try:
    fd = os.open(dev_path, os.O_RDONLY)
    fcntl.ioctl(fd, 1074021776, 1)
except Exception as e:
    sys.stderr.write(f'Grab failed: {e}\n')
    sys.exit(1)

hotkey = ${HOTKEY_CODE}
hotkey_pressed = False

while True:
    try:
        data = os.read(fd, 24)
        if not data or len(data) < 24:
            break

        _, _, ev_type, ev_code, ev_val = struct.unpack('<QQHHi', data[:24])

        if ev_type == 1 and ev_code == hotkey:
            if ev_val == 1:
                hotkey_pressed = True
            elif ev_val == 0 and hotkey_pressed:
                break
            continue

        sys.stdout.buffer.write(data)
        sys.stdout.flush()
    except Exception:
        break
" | ssh -T "${REMARKABLE_HOST}" "/home/root/rmiject"

notify-send -u normal -i computer "💻 PC Mode" "Keyboard reconnected to PC."
