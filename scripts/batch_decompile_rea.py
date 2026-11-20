#!/usr/bin/env python3
"""
batch_decompile_rea.py - Automated Batch Decompilation of UEFI Firmware Modules
Uses REA CLI with Ghidra provider and --filter-output normalized_result.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

GHIDRA_INSTALL_DIR = "/run/media/julian/ML3/ghidra/ghidra_12.1.4_PUBLIC"
JAVA_HOME = "/usr/lib/jvm/java-27-openjdk"
REA_SCRIPT = "/run/media/julian/ML6/rea/scripts/rea.mjs"

MODULE_TARGETS = [
    {
        "name": "SecSMIFlash",
        "guid": "3370a4bd-8c23-4565-a2a2-065feede6080",
        "path": "/run/media/julian/ML6/bios-re/extracted/fid_rea/flash/FV@0x92f000/FFS-9e21fd93-9c72-4c15-8c4b-e77f1db2d792@0xa1ee78/section-0/section-1/FV@0x10/FFS-3370a4bd-8c23-4565-a2a2-065feede6080@0x859020/section-1.payload.bin",
        "procedures": ["0x1300", "0x2cd8", "0x2024", "0x2900"]
    },
    {
        "name": "WpbtDxe",
        "guid": "0996199f-2ce2-4d97-830b-077a7b28588a",
        "path": "/run/media/julian/ML6/bios-re/extracted/fid_rea/flash/FV@0x92f000/FFS-9e21fd93-9c72-4c15-8c4b-e77f1db2d792@0xa1ee78/section-0/section-1/FV@0x10/FFS-0996199f-2ce2-4d97-830b-077a7b28588a@0x525508/section-1.payload.bin",
        "procedures": ["0x2e0", "0x478", "0x688"]
    },
    {
        "name": "WpbtDropper",
        "guid": "aeb1671d-019c-4b3b-ba00-35a2e6280436",
        "path": "/run/media/julian/ML6/bios-re/extracted/fid_rea/flash/FV@0x92f000/FFS-9e21fd93-9c72-4c15-8c4b-e77f1db2d792@0xa1ee78/section-0/section-1/FV@0x10/FFS-aeb1671d-019c-4b3b-ba00-35a2e6280436@0xbc0698/section-0/section-0.payload.bin",
        "procedures": ["0x140001580", "0x140001300"]
    }
]

def decompile_procedure(bin_path, address):
    env = os.environ.copy()
    env["GHIDRA_INSTALL_DIR"] = GHIDRA_INSTALL_DIR
    env["JAVA_HOME"] = JAVA_HOME

    cmd = [
        "node",
        REA_SCRIPT,
        "decompile",
        bin_path,
        address,
        "--filter-output",
        "normalized_result"
    ]
    try:
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=120)
        if res.returncode == 0:
            return res.stdout
        else:
            print(f"[-] Decompile {address} failed: {res.stderr.strip()}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"[-] Exception decompiling {address}: {e}", file=sys.stderr)
        return None

def main():
    catalog_dir = Path("/run/media/julian/ML6/bios-re/findings/decompile_catalog")
    catalog_dir.mkdir(parents=True, exist_ok=True)

    for mod in MODULE_TARGETS:
        print(f"[+] Processing module: {mod['name']} ({mod['guid']})")
        out_file = catalog_dir / f"{mod['name']}_{mod['guid']}.c"
        decompiled_blocks = []

        header = f"/*\n * Module: {mod['name']}\n * GUID: {mod['guid']}\n * Source: {mod['path']}\n */\n\n"
        decompiled_blocks.append(header)

        for proc in mod["procedures"]:
            print(f"    --> Decompiling procedure {proc}...")
            code = decompile_procedure(mod["path"], proc)
            if code:
                decompiled_blocks.append(f"// --- Procedure: {proc} ---\n{code}\n")
            else:
                decompiled_blocks.append(f"// --- Procedure: {proc} (FAILED) ---\n")

        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(decompiled_blocks))
        print(f"[+] Wrote {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()
