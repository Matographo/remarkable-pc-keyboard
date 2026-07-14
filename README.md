# remarkable-pc-keyboard

Type on your reMarkable Paper Pro with any PC/Mac keyboard. No Typefolio needed.

## How it works

```
PC Keyboard → SSH Tunnel → reMarkable Kernel
```

1. **PC side**: Your keyboard is grabbed (exclusive access)
2. **Transfer**: Events sent via SSH to reMarkable  
3. **reMarkable side**: `rmiject` injects events into kernel

## Supported Platforms

| Platform | Script | Requirements |
|----------|--------|--------------|
| Linux | `scripts/remarkable.sh` | python3, ssh, libnotify |
| macOS | `scripts/remarkable_mac.py` | python3, pyobjc, ssh |
| Windows | `scripts/remarkable_windows.py` | python3, pynput, ssh |

## Quick Start

### 1. Configure keyboard

Edit `scripts/keyboard.conf`:

```bash
KEYBOARD_NAME="Moonlander"  # Your keyboard name (partial match)
REMARKABLE_HOST="remarkable"
HOTKEY_CODE=183             # Key code (183=F13, 184=F14, 185=F15)
HOTKEY_NAME="F13"           # Display name
```

**Common hotkey codes:**

| Code | Key |
|------|-----|
| 183 | F13 |
| 184 | F14 |
| 185 | F15 |
| 70 | ScrollLock |
| 119 | Pause |

### 2. Install on reMarkable

```bash
ssh remarkable
curl -L https://github.com/matographo/remarkable-pc-keyboard/releases/latest/download/install.sh | bash
```

### 3. Setup PC

**Linux:**
```bash
sudo dnf install python3 openssh-clients libnotify  # Fedora
sudo apt install python3 openssh-client libnotify-bin  # Ubuntu
```

**macOS:**
```bash
pip3 install pyobjc
```

**Windows:**
```bash
pip install pynput
```

### 4. Run

**Linux:**
```bash
./scripts/remarkable.sh
```

**macOS:**
```bash
python3 scripts/remarkable_mac.py
```

**Windows:**
```bash
python scripts/remarkable_windows.py
```

### 5. Switch back to PC

Press **F13** (or configured hotkey) on your keyboard.

## Keyboard Examples

Any keyboard that creates `/dev/input/by-id/*event-kbd` on Linux works:

- ZSA Moonlander
- ZSA Atreus  
- Corne/Crkbd
- Kinesis Advantage
- Planck
- Preonic
- Any USB keyboard

Set `KEYBOARD_NAME` in `scripts/keyboard.conf` to match your keyboard.

## SSH Setup

```bash
# Generate key
ssh-keygen -t ed25519

# Copy to reMarkable
ssh-copy-id remarkable

# Test
ssh remarkable
```

## Project Structure

```
├── src/
│   └── rmiject.c              # Kernel injector (ARM64, runs on reMarkable)
├── scripts/
│   ├── keyboard.conf           # Configuration
│   ├── remarkable.sh           # Linux script
│   ├── remarkable_mac.py       # macOS script
│   ├── remarkable_windows.py   # Windows script
│   ├── toggle-remarkable.sh    # Quick toggle
│   ├── install.sh              # reMarkable installer
│   └── setup.sh                # PC setup checker
├── .github/
│   └── workflows/
│       └── build.yml           # CI/CD pipeline
└── README.md
```

## Troubleshooting

### "Keyboard not found"

Check available keyboards:
```bash
ls /dev/input/by-id/ | grep -i kbd
```

Update `KEYBOARD_NAME` in `scripts/keyboard.conf` to match.

### macOS: "Failed to create event tap"

Grant accessibility permissions:
System Settings → Privacy & Security → Accessibility → Add your terminal

### Windows: "Access denied"

Run terminal as administrator.

## License

MIT
