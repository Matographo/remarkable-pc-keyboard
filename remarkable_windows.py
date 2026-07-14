"""
remarkable_windows.py - Windows version
Requires: pip install pynput
"""

import os
import struct
import subprocess
import sys
from pynput import keyboard

# Load config
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
config = {}
with open(os.path.join(SCRIPT_DIR, "keyboard.conf")) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            key, val = line.strip().split("=", 1)
            config[key] = val.strip('"')

KEYBOARD_NAME = config.get("KEYBOARD_NAME", "Moonlander")
HOTKEY_CODE = int(config.get("HOTKEY_CODE", "183"))
HOTKEY_NAME = config.get("HOTKEY_NAME", "F13")
REMARKABLE_HOST = config.get("REMARKABLE_HOST", "remarkable")

# Map common hotkeys
HOTKEY_MAP = {
    183: keyboard.Key.f13,
    184: keyboard.Key.f14,
    185: keyboard.Key.f15,
}

HOTKEY = HOTKEY_MAP.get(HOTKEY_CODE)

ssh_process = None
hotkey_pressed = False


def on_press(key):
    global hotkey_pressed, ssh_process

    if key == HOTKEY:
        hotkey_pressed = True
        return

    try:
        keycode = key.vk
    except AttributeError:
        keycode = 0

    ev_type = 1  # EV_KEY
    ev_val = 1  # down

    data = b'\x00' * 16 + struct.pack('<HHi', ev_type, keycode, ev_val)
    try:
        ssh_process.stdin.write(data)
        ssh_process.stdin.flush()
    except:
        pass


def on_release(key):
    global hotkey_pressed, ssh_process

    if key == HOTKEY and hotkey_pressed:
        ssh_process.stdin.close()
        return False  # Stop listener

    try:
        keycode = key.vk
    except AttributeError:
        keycode = 0

    ev_type = 1
    ev_val = 0  # up

    data = b'\x00' * 16 + struct.pack('<HHi', ev_type, keycode, ev_val)
    try:
        ssh_process.stdin.write(data)
        ssh_process.stdin.flush()
    except:
        pass


def main():
    global ssh_process

    print(f"🔍 Looking for keyboard: {KEYBOARD_NAME}")
    print(f"🎯 Hotkey: {HOTKEY_NAME} to return to PC")
    print(f"📱 Connecting to {REMARKABLE_HOST}...")

    ssh_process = subprocess.Popen(
        ["ssh", "-T", REMARKABLE_HOST, "/home/root/rmiject"],
        stdin=subprocess.PIPE
    )

    print("✅ Keyboard intercepted! Writing to reMarkable...")
    print(f"   Press {HOTKEY_NAME} to disconnect")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("💻 PC Mode - Keyboard reconnected")


if __name__ == "__main__":
    main()
