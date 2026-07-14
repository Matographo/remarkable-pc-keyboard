#!/usr/bin/env python3
"""
remarkable_mac.py - macOS version
Requires: pip install pyobjc
"""

import sys
import struct
import subprocess
import signal
from Foundation import NSObject
from AppKit import NSEvent, NSApplication
from Quartz import (
    CGEventTapCreate,
    kCGEventTapLocationAtHead,
    kCGHeadInsertEventTap,
    kCGEventTapOptionDefault,
    kCGEventMaskKeyDown,
    kCGEventMaskKeyUp,
    CGEventTapEnable,
    CGEventTapGetEvent,
)
import CoreFoundation
import threading

import os

# Load config
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
config = {}
with open(os.path.join(SCRIPT_DIR, "keyboard.conf")) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            key, val = line.strip().split("=", 1)
            config[key] = val.strip('"')

KEYBOARD_NAME = config.get("KEYBOARD_NAME", "Moonlander")
HOTKEY = int(config.get("HOTKEY_CODE", "183"))
REMARKABLE_HOST = config.get("REMARKABLE_HOST", "remarkable")

hotkey_pressed = False
ssh_process = None


class KeyInterceptor(NSObject):
    def intercept(self, proxy, event_type, event, refcon):
        global hotkey_pressed

        keycode = CoreFoundation.CGEventGetIntegerValueField(event, 42)

        if keycode == HOTKEY:
            if event_type == kCGEventMaskKeyDown:
                hotkey_pressed = True
            elif event_type == kCGEventMaskKeyUp and hotkey_pressed:
                # Exit on hotkey release
                CGEventTapEnable(proxy, False)
                ssh_process.stdin.close()
                sys.exit(0)
            return None  # Don't forward hotkey

        # Forward to reMarkable
        key_down = 1 if event_type == kCGEventMaskKeyDown else 0
        ev_type = 1  # EV_KEY
        ev_code = keycode
        ev_val = key_down

        # Linux input_event format: timeval(16 bytes) + type(2) + code(2) + value(4)
        data = b'\x00' * 16 + struct.pack('<HHi', ev_type, ev_code, ev_val)
        try:
            ssh_process.stdin.write(data)
            ssh_process.stdin.flush()
        except:
            pass

        return event


def main():
    global ssh_process

    print(f"🔍 Looking for keyboard: {KEYBOARD_NAME}")
    print(f"🎯 Hotkey: {config.get('HOTKEY_NAME', 'F13')} to return to PC")
    print(f"📱 Connecting to {REMARKABLE_HOST}...")
    print(f"   Press {config.get('HOTKEY_NAME', 'F13')} to disconnect")

    ssh_process = subprocess.Popen(
        ["ssh", "-T", REMARKABLE_HOST, "/home/root/rmiject"],
        stdin=subprocess.PIPE
    )

    interceptor = KeyInterceptor.alloc().init()

    tap = CGEventTapCreate(
        kCGEventTapLocationAtHead,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        kCGEventMaskKeyDown | kCGEventMaskKeyUp,
        interceptor.intercept,
        None,
    )

    if tap is None:
        print("❌ Failed to create event tap. Check accessibility permissions!")
        print("   System Settings → Privacy & Security → Accessibility")
        sys.exit(1)

    CGEventTapEnable(tap, True)
    print("✅ Keyboard intercepted! Writing to reMarkable...")

    loop = CoreFoundation.CFRunLoopGetCurrent()
    source = CoreFoundation.CFMachPortCreateRunLoopSource(None, tap, 0)
    CoreFoundation.CFRunLoopAddSource(loop, source, CoreFoundation.kCFRunLoopCommonModes)
    CoreFoundation.CFRunLoopRun()


if __name__ == "__main__":
    main()
