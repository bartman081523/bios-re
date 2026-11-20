#!/usr/bin/env python3
"""
patch_nvram_setup.py - Epistemic UEFI NVRAM Setup Variable Generator & Patch Engine
Target: Gigabyte B550 AORUS Elite V2 (AMD AM4 / Zen 3)
Variable: Setup-ec87d643-eba4-4bb5-a1e5-3f3e36b20da9
"""

import sys
import os
import struct
import argparse
from pathlib import Path

SETUP_GUID = "ec87d643-eba4-4bb5-a1e5-3f3e36b20da9"
EFIVARS_SETUP_PATH = Path(f"/sys/firmware/efi/efivars/Setup-{SETUP_GUID}")
BACKUP_PATH = Path("/run/media/julian/ML6/bios-re/findings/live_setup_backup.bin")
PATCHED_PATH = Path("/run/media/julian/ML6/bios-re/findings/patched_setup_balanced.bin")

# Target Delta offsets and values for Balanced Profile
BALANCED_DELTAS = {
    0x157: (0x01, "Extreme Memory Profile (X.M.P.)", "Disabled -> Profile 1"),
    0x146: (0x01, "Core Performance Boost (CPB)", "Disabled -> Auto (Unlock 4.65 GHz Boost)"),
    0x27E: (0x01, "Above 4G Decoding", "Disabled -> Enabled"),
    0x27F: (0x01, "Re-Size BAR Support", "Disabled -> Auto"),
    0x14F: (0x00, "Power Supply Idle Control", "Auto -> Typical Current Idle"),
    0x264: (0x00, "APP Center Download & Install", "Enabled -> Disabled (Kill WPBT Dropper)"),
    0x155: (0x01, "CPPC", "Auto -> Enabled"),
    0x156: (0x01, "CPPC Preferred Cores", "Auto -> Enabled"),
    0x166: (0x01, "Gear Down Mode", "Auto -> Enabled"),
    0x25F: (0x01, "IOMMU", "Auto -> Enabled")
}

def inspect_and_patch(raw_data):
    if len(raw_data) != 642:
        raise ValueError(f"Ungültige Setup-Größe: {len(raw_data)} Bytes (erwartet: 642 Bytes / 0x282)")
    
    patched = bytearray(raw_data)
    print("=" * 90)
    print(" [NVRAM SETUP PATCH-PLAN: DELTA ZU BALANCED]")
    print("=" * 90)
    print(f"{'Offset':8s} | {'Parameter':42s} | {'Vorher':10s} | {'Nachher (Gepatcht)':18s}")
    print("-" * 90)

    for off, (new_val, name, desc) in sorted(BALANCED_DELTAS.items()):
        old_val = raw_data[off]
        patched[off] = new_val
        print(f"0x{off:03X}    | {name:42s} | 0x{old_val:02X} ({old_val:3d}) | 0x{new_val:02X} ({new_val:3d}) -> {desc}")
    print("=" * 90)
    return bytes(patched)

def main():
    parser = argparse.ArgumentParser(description="UEFI NVRAM Setup Patch Engine")
    parser.add_argument("--generate", action="store_true", default=True,
                        help="Erzeugt die gepatchte Binärdatei und legt ein Backup an")
    args = parser.parse_args()

    # Load from findings or efivars
    live_dump = Path("/run/media/julian/ML6/bios-re/findings/live_setup_var.bin")
    if not live_dump.exists():
        print("[-] Fehler: findings/live_setup_var.bin nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    raw_payload = live_dump.read_bytes()
    # Save backup
    BACKUP_PATH.write_bytes(raw_payload)
    print(f"[+] Backup der aktuellen Live-Werte gesichert: {BACKUP_PATH} ({len(raw_payload)} Bytes)")

    patched_payload = inspect_and_patch(raw_payload)
    PATCHED_PATH.write_bytes(patched_payload)
    print(f"[+] Gepatchte Setup-Payload erfolgreich erzeugt: {PATCHED_PATH} ({len(patched_payload)} Bytes)")

if __name__ == "__main__":
    main()
