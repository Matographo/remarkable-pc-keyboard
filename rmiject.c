#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <linux/uinput.h>

int main() {
    // Öffne die virtuelle Eingabeschnittstelle des reMarkable
    int fd = open("/dev/uinput", O_WRONLY);
    if (fd < 0) {
        perror("❌ Fehler beim Öffnen von /dev/uinput auf dem reMarkable");
        return 1;
    }

    // Aktiviere Tastatur-Events und alle Linux-Keycodes (0 bis 511 für QMK-Layer)
    ioctl(fd, UI_SET_EVBIT, EV_KEY);
    ioctl(fd, UI_SET_EVBIT, EV_SYN);
    for (int i = 0; i < 512; i++) {
        ioctl(fd, UI_SET_KEYBIT, i);
    }

    // Registriere die virtuelle Moonlander im System
    struct uinput_user_dev uidev;
    memset(&uidev, 0, sizeof(uidev));
    snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, "Moonlander-SSH-Bridge");
    uidev.id.bustype = BUS_USB;
    uidev.id.vendor  = 0x3297; // ZSA Vendor ID
    uidev.id.product = 0x4975; // Moonlander Product ID
    uidev.id.version = 1;

    write(fd, &uidev, sizeof(uidev));
    if (ioctl(fd, UI_DEV_CREATE) < 0) {
        perror("❌ Fehler beim Erstellen der Tastatur");
        close(fd);
        return 1;
    }

    fprintf(stderr, "✅ Virtuelle Tastatur auf reMarkable aktiv! Warte auf SSH-Datenstrom...\n");

    // Lese Daten aus dem SSH-Tunnel (stdin) und spritze sie direkt in den Kernel ein
    struct input_event ev;
    while (read(STDIN_FILENO, &ev, sizeof(ev)) > 0) {
        write(fd, &ev, sizeof(ev));
    }

    // Wird ausgeführt, sobald du den SSH-Tunnel am PC (mit Strg+C) beendest
    ioctl(fd, UI_DEV_DESTROY);
    close(fd);
    return 0;
}
