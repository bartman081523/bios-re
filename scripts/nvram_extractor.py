#!/usr/bin/env python3
"""
nvram_extractor.py - Multi-Source UEFI NVRAM Variable Extraction Tool
Target: AMD AM4 / Gigabyte B550 Platform

Supported Sources:
1. Live System (`/sys/firmware/efi/efivars`) - Direct runtime extraction.
2. Raw BIOS ROM Image (`.FId`, `.bin`, `.rom`) - Static extraction from StdDefaults / NVAR stores.
3. Extracted FFS Blobs (`cef5b9a3` / NVRAM stores).
"""

import os
import sys
import struct
import argparse
from pathlib import Path

# Well-known GUIDs
SETUP_GUID = "ec87d643-eba4-4bb5-a1e5-3f3e36b20da9"
EFI_GLOBAL_VARIABLE = "8be4df61-93ca-11d2-aa0d-00e098032b8c"

class NvramExtractor:
    def __init__(self):
        pass

    @staticmethod
    def extract_from_live(var_name="Setup", guid=SETUP_GUID):
        """
        Extracts variable from Linux sysfs efivars interface.
        Format: 4 bytes attributes (little-endian) + raw variable payload.
        """
        efivars_dir = Path("/sys/firmware/efi/efivars")
        if not efivars_dir.exists():
            print("[-] /sys/firmware/efi/efivars is not mounted or system booted in legacy BIOS mode.", file=sys.stderr)
            return None

        target_file = efivars_dir / f"{var_name}-{guid}"
        if not target_file.exists():
            print(f"[-] Variable '{target_file.name}' not found in efivars.", file=sys.stderr)
            return None

        raw = target_file.read_bytes()
        if len(raw) < 4:
            print(f"[-] Variable file too short ({len(raw)} bytes).", file=sys.stderr)
            return None

        attr = struct.unpack("<I", raw[:4])[0]
        payload = raw[4:]
        return {
            "source": "live_efivars",
            "name": var_name,
            "guid": guid,
            "attributes": attr,
            "size": len(payload),
            "payload": payload
        }

    @staticmethod
    def extract_all_live():
        """
        Lists and extracts all variables from live efivars.
        """
        efivars_dir = Path("/sys/firmware/efi/efivars")
        if not efivars_dir.exists():
            return []

        results = []
        for p in sorted(efivars_dir.glob("*-*")):
            name_parts = p.name.rsplit("-", 5)
            if len(name_parts) == 6:
                name = name_parts[0]
                guid = "-".join(name_parts[1:])
            else:
                name = p.name
                guid = "unknown"

            raw = p.read_bytes()
            attr = struct.unpack("<I", raw[:4])[0] if len(raw) >= 4 else 0
            payload = raw[4:] if len(raw) >= 4 else b""
            results.append({
                "name": name,
                "guid": guid,
                "attributes": attr,
                "size": len(payload),
                "payload": payload
            })
        return results

    @staticmethod
    def extract_from_rom(rom_path):
        """
        Extracts all AMI NVAR variables from a raw BIOS ROM image or extracted FFS section.
        """
        p = Path(rom_path)
        if not p.exists():
            print(f"[-] ROM file {rom_path} not found.", file=sys.stderr)
            return []

        data = p.read_bytes()
        variables = []
        idx = 0

        while True:
            pos = data.find(b"NVAR", idx)
            if pos == -1:
                break

            if pos + 11 > len(data):
                break

            size = struct.unpack_from("<H", data, pos + 4)[0]
            attr = struct.unpack_from("<I", data, pos + 6)[0]
            state = data[pos + 10]

            nul = data.find(b"\x00", pos + 11)
            if nul == -1 or nul >= pos + min(size, 256):
                idx = pos + 4
                continue

            try:
                name = data[pos + 11 : nul].decode("ascii")
            except UnicodeDecodeError:
                idx = pos + 4
                continue

            data_start = nul + 1
            data_end = pos + size
            payload = data[data_start:data_end]

            variables.append({
                "source": str(p),
                "offset": pos,
                "name": name,
                "size": len(payload),
                "total_entry_size": size,
                "attributes": attr,
                "state": state,
                "payload": payload
            })
            # If this is the StdDefaults container, recursively parse inner NVAR entries
            if name == "StdDefaults":
                inner_idx = data_start
                while inner_idx < data_end:
                    sub_pos = data.find(b"NVAR", inner_idx, data_end)
                    if sub_pos == -1 or sub_pos + 11 > data_end:
                        break
                    sub_sz = struct.unpack_from("<H", data, sub_pos + 4)[0]
                    sub_attr = struct.unpack_from("<I", data, sub_pos + 6)[0]
                    sub_state = data[sub_pos + 10]
                    sub_nul = data.find(b"\x00", sub_pos + 11, min(data_end, sub_pos + 256))
                    if sub_nul == -1:
                        inner_idx = sub_pos + 4
                        continue
                    try:
                        sub_name = data[sub_pos + 11 : sub_nul].decode("ascii")
                    except UnicodeDecodeError:
                        inner_idx = sub_pos + 4
                        continue
                    sub_payload = data[sub_nul + 1 : sub_pos + sub_sz]
                    variables.append({
                        "source": f"{p} (StdDefaults)",
                        "offset": sub_pos,
                        "name": sub_name,
                        "size": len(sub_payload),
                        "total_entry_size": sub_sz,
                        "attributes": sub_attr,
                        "state": sub_state,
                        "payload": sub_payload
                    })
                    inner_idx = sub_pos + max(sub_sz, 4)

            idx = pos + max(size, 4)

        return variables

def main():
    parser = argparse.ArgumentParser(description="Multi-Source UEFI NVRAM Variable Extractor")
    parser.add_argument("--live", action="store_true", help="Extract from live /sys/firmware/efi/efivars")
    parser.add_argument("--rom", type=str, help="Extract from a BIOS ROM image file")
    parser.add_argument("--var", type=str, default="Setup", help="Specific variable to extract (default: Setup)")
    parser.add_argument("--save-bin", type=str, help="Save extracted payload as raw binary file")
    parser.add_argument("--advisor", action="store_true", help="Pipe extracted Setup variable directly into bios_config_advisor")
    args = parser.parse_args()

    result = None

    if args.live or (not args.rom and Path("/sys/firmware/efi/efivars").exists()):
        print("[+] Extracting from live system efivars...")
        result = NvramExtractor.extract_from_live(var_name=args.var)
        if result:
            print(f"    [OK] Variable: {result['name']} ({result['guid']})")
            print(f"    [OK] Attributes: 0x{result['attributes']:08x}")
            print(f"    [OK] Payload size: {result['size']} bytes (0x{result['size']:x})")
    elif args.rom:
        print(f"[+] Extracting NVAR records from ROM: {args.rom}...")
        vars_found = NvramExtractor.extract_from_rom(args.rom)
        print(f"    Found {len(vars_found)} NVAR records:")
        for v in vars_found:
            print(f"    - @0x{v['offset']:06x} | Size: {v['size']:4d} B | Name: {v['name']}")
            if v['name'] == args.var and result is None:
                result = v

    if result and args.save_bin:
        out_path = Path(args.save_bin)
        out_path.write_bytes(result["payload"])
        print(f"[+] Saved payload to {out_path} ({len(result['payload'])} bytes)")

    if result and args.advisor and result["name"] == "Setup":
        print("\n" + "=" * 80)
        print(" RUNNING CONFIG ADVISOR ON EXTRACTED SETUP VARIABLE")
        print("=" * 80)
        sys.path.insert(0, str(Path(__file__).parent))
        from bios_config_advisor import BiosConfigSimulator, print_report
        sim = BiosConfigSimulator(raw_buffer=result["payload"])
        print_report(sim)

if __name__ == "__main__":
    main()
