#!/usr/bin/env python3
"""
Grabs the ASUS Xonar U5 volume knob's HID input exclusively and routes
volume up/down/mute to the Xonar's Digital (IEC958) PipeWire sink only,
so it no longer acts as a global multimedia key that changes whichever
sink happens to be default (e.g. your USB sound card).
"""
import re
import subprocess
import sys
import time

import evdev
from evdev import ecodes

DEVICE_PATH = "/dev/xonar-knob-event"  # stable symlink, created by the udev rule
VOLUME_STEP = "3%"


def find_target_sink():
    """Find the Xonar U5's IEC958 (digital) sink name via pactl.

    Some generic USB-audio dongles also label their profile
    '...iec958-stereo' even though they're not the intended device, so
    match on both 'xonar' and 'iec958' to disambiguate.
    """
    try:
        out = subprocess.check_output(["pactl", "list", "sinks", "short"], text=True)
    except subprocess.CalledProcessError:
        return None
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            name_lower = parts[1].lower()
            if "xonar" in name_lower and "iec958" in name_lower:
                return parts[1]
    return None


def get_volume_percent(sink):
    try:
        out = subprocess.check_output(["pactl", "get-sink-volume", sink], text=True)
    except subprocess.CalledProcessError:
        return None
    match = re.search(r"(\d+)%", out)
    return int(match.group(1)) if match else None


def is_muted(sink):
    try:
        out = subprocess.check_output(["pactl", "get-sink-mute", sink], text=True)
    except subprocess.CalledProcessError:
        return False
    return "yes" in out.lower()


def show_kde_osd(vol, muted):
    """Trigger Plasma's own OSD widget over DBus — the same one used for
    the physical multimedia keys, so it updates in place instead of
    stacking. Returns True if it succeeded (i.e. we're under Plasma)."""
    for qdbus_bin in ("qdbus6", "qdbus"):
        try:
            if muted:
                subprocess.run(
                    [qdbus_bin, "org.kde.plasmashell", "/org/kde/osdService",
                     "org.kde.osdService.mutedChanged", "true"],
                    check=True, capture_output=True,
                )
            else:
                subprocess.run(
                    [qdbus_bin, "org.kde.plasmashell", "/org/kde/osdService",
                     "org.kde.osdService.volumeChanged", str(vol)],
                    check=True, capture_output=True,
                )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


def show_osd(sink):
    """Pop a volume-style notification, since grabbing the knob means the
    desktop's own OSD no longer sees the keypress that would normally
    trigger it. Prefers Plasma's native OSD; falls back to a generic
    desktop notification for other desktops."""
    vol = get_volume_percent(sink)
    if vol is None:
        return
    muted = is_muted(sink)

    if show_kde_osd(vol, muted):
        return

    icon = "audio-volume-muted" if muted else (
        "audio-volume-high" if vol > 66 else
        "audio-volume-medium" if vol > 33 else
        "audio-volume-low" if vol > 0 else
        "audio-volume-muted"
    )
    text = "Muted" if muted else f"Xonar U5: {vol}%"
    subprocess.run(
        [
            "notify-send",
            "-a", "xonar-knob",
            "-i", icon,
            "-h", f"int:value:{vol}",
            "-h", "string:x-canonical-private-synchronous:xonar-knob-osd",
            "-t", "1500",
            text,
        ],
        check=False,
    )


def wait_for_device(path, retries=20, delay=1.0):
    for _ in range(retries):
        try:
            return evdev.InputDevice(path)
        except FileNotFoundError:
            time.sleep(delay)
    return None


def wait_for_sink(retries=20, delay=1.0):
    for _ in range(retries):
        sink = find_target_sink()
        if sink is not None:
            return sink
        time.sleep(delay)
    return None


def main():
    dev = wait_for_device(DEVICE_PATH)
    if dev is None:
        print(
            f"Could not open {DEVICE_PATH} — is the udev rule installed "
            f"and the Xonar U5 plugged in?",
            file=sys.stderr,
        )
        sys.exit(1)

    sink = wait_for_sink()
    if sink is None:
        print(
            "Could not find the Xonar U5's IEC958/digital sink via pactl "
            "— is PipeWire running and the Xonar set to digital output?",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Controlling sink: {sink}")
    dev.grab()  # exclusive: desktop/compositor no longer sees these keys at all

    for event in dev.read_loop():
        if event.type != ecodes.EV_KEY or event.value not in (1, 2):  # press/repeat only
            continue
        if event.code == ecodes.KEY_VOLUMEUP:
            subprocess.run(["pactl", "set-sink-volume", sink, f"+{VOLUME_STEP}"])
            show_osd(sink)
        elif event.code == ecodes.KEY_VOLUMEDOWN:
            subprocess.run(["pactl", "set-sink-volume", sink, f"-{VOLUME_STEP}"])
            show_osd(sink)
        elif event.code == ecodes.KEY_MUTE:
            subprocess.run(["pactl", "set-sink-mute", sink, "toggle"])
            show_osd(sink)


if __name__ == "__main__":
    main()
