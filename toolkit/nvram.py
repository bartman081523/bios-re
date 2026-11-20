"""
toolkit/nvram.py - Multi-Vendor UEFI NVRAM Variable Manager & Offset Resolver
Supports:
- Live sysfs efivars (/sys/firmware/efi/efivars)
- Canonical AM4 Setup GUIDs (AMI Aptio V standard & vendor-specific)
- Dynamic HII Question Database Integration (setup_full_db.json)
- Offline & dump file fallbacks
"""

import os
import sys
import struct
import json
from pathlib import Path

# Well-known AM4 / AMI Aptio V GUIDs
SETUP_GUID_AMI = "ec87d643-eba4-4bb5-a1e5-3f3e36b20da9"
SETUP_GUID_ALT = "80e1202e-2697-4264-9cc9-80762c3e5863"
AMD_SETUP_GUID = "3a997502-647a-4c82-998e-52ef9486a247"
AMD_PBS_GUID   = "a339d746-f678-49b3-9fc7-54ce0f9df226"

class NvramManager:
    def __init__(self, db_path=None, dump_path=None):
        self.db = {}
        self.raw_setup = None
        self.guid = SETUP_GUID_AMI
        self.attr = 0

        # Load HII Database if available
        if db_path and Path(db_path).exists():
            try:
                self.db = json.loads(Path(db_path).read_text())
            except Exception:
                pass
        elif Path("/run/media/julian/ML6/bios-re/findings/setup_full_db.json").exists():
            try:
                self.db = json.loads(Path("/run/media/julian/ML6/bios-re/findings/setup_full_db.json").read_text())
            except Exception:
                pass

        # Load raw setup payload
        if dump_path and Path(dump_path).exists():
            self.raw_setup = Path(dump_path).read_bytes()
        else:
            self._load_live()

    def _load_live(self):
        efivars = Path("/sys/firmware/efi/efivars")
        target = efivars / f"Setup-{self.guid}"
        if target.exists():
            try:
                raw = target.read_bytes()
                if len(raw) >= 4:
                    self.attr = struct.unpack("<I", raw[:4])[0]
                    self.raw_setup = raw[4:]
                    return
            except Exception:
                pass

        # Fallback to local dump
        local_dump = Path("/run/media/julian/ML6/bios-re/findings/live_setup_var.bin")
        if local_dump.exists():
            self.raw_setup = local_dump.read_bytes()

    def get_byte(self, offset):
        if self.raw_setup and len(self.raw_setup) > offset:
            return self.raw_setup[offset]
        return None

    def find_question(self, search_text):
        matches = []
        for off_str, item in self.db.items():
            prompt = item.get("prompt", "")
            if search_text.lower() in prompt.lower():
                matches.append(item)
        return matches
