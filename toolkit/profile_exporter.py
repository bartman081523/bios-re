"""
toolkit/profile_exporter.py - AMITSE UEFI Binary Profile Generator & EFI Exporter
Reverse engineered from AMI Aptio V / AMITSE engine (b1da0adf-4f77-4070-a88e-bffe1c60529a).

Exports both Standard and Linux-Optimized Profile sets:
- STABILITY.PRO & STABILITY_LINUX.PRO
- BALANCED.PRO  & BALANCED_LINUX.PRO
- PERFORMANCE.PRO & PERFORMANCE_LINUX.PRO
"""

import os
import struct
import shutil
from pathlib import Path
from .profiles import ProfileGenerator

class ProfileExporter:
    SETUP_SIZE = 0x282 # 642 bytes for AM4 B550 Setup variable
    HEADER_SIZE = 0x38 # 56 bytes
    MAGIC = 0x1964

    GIGABYTE_PROJECT_MAP = {
        "B550 AORUS ELITE V2": "8ARNR302",
        "B550 AORUS ELITE":    "8ARNR301",
        "B550 AORUS PRO V2":   "8ARNR304",
        "B550 AORUS PRO":      "8ARNR303",
        "B550 AORUS MASTER":   "8ARNR300",
        "B550 GAMING X V2":    "8ARNR306",
        "B550 GAMING X":       "8ARNR305",
        "B550M AORUS PRO":     "8ARNR307",
        "B550I AORUS PRO AX":  "8ARNR308",
    }

    @staticmethod
    def extract_bdr_metadata(image_path: str):
        try:
            with open(image_path, "rb") as f:
                bios = f.read()
            pos = bios.find(b"$BDR")
            if pos != -1 and bios[pos+8:pos+10] == b"\xa5\x5a":
                model_bytes = bios[pos+0x20:pos+0x28]
                bios_ver_bytes = bios[pos+0x28:pos+0x2c]
                model_str = model_bytes.split(b"\x00")[0].decode("ascii", errors="replace")
                bios_ver_str = bios_ver_bytes.split(b"\x00")[0].decode("ascii", errors="replace")
                return model_str, bios_ver_str
        except Exception:
            pass
        return None, None

    @classmethod
    def derive_metadata(cls, hw_profile, bios_image_path=None):
        model_str = None
        bios_ver = hw_profile.board.get("bios_version", "FIb")

        if bios_image_path and Path(bios_image_path).is_file():
            img_model, img_ver = cls.extract_bdr_metadata(bios_image_path)
            if img_model:
                model_str = img_model
            if img_ver:
                bios_ver = img_ver

        if not model_str:
            ref_candidates = [
                "images/B550AORUSELITEV212.FIb",
                "images/B550AORUSELITEV212.FH",
                "images/B550AORUSELITEV212.FG"
            ]
            for cand in ref_candidates:
                if Path(cand).is_file():
                    img_model, img_ver = cls.extract_bdr_metadata(cand)
                    if img_model:
                        model_str = img_model
                        break

        if not model_str:
            board_name = hw_profile.board.get("name", "")
            model_str = cls.GIGABYTE_PROJECT_MAP.get(board_name, "8ARNR302")

        return model_str, bios_ver

    @classmethod
    def build_profile_binary(cls, base_setup: bytes, deltas: list, model_id: str, bios_version: str) -> bytes:
        if len(base_setup) < cls.SETUP_SIZE:
            raise ValueError(f"Base setup buffer must be at least {cls.SETUP_SIZE} bytes (got {len(base_setup)})")

        setup_buf = bytearray(base_setup[:cls.SETUP_SIZE])

        for delta in deltas:
            offset = delta.get("offset")
            val = delta.get("target_val")
            if offset is not None and val is not None and offset < len(setup_buf):
                setup_buf[offset] = val

        var_index = 0
        var_size = len(setup_buf)
        record = struct.pack("<IH", var_index, var_size) + bytes(setup_buf)

        payload_len = len(record)
        checksum = sum(record) & 0xFF

        header = bytearray(cls.HEADER_SIZE)
        struct.pack_into("<HHBBBBI", header, 0,
                         cls.MAGIC,
                         payload_len,
                         0x11,
                         cls.HEADER_SIZE,
                         0x00,
                         checksum,
                         1
        )

        bios_bytes = bios_version.encode("ascii")[:4].ljust(4, b"\x00")
        header[0x0c:0x10] = bios_bytes

        model_bytes = model_id.encode("ascii")[:8].ljust(8, b"\x00")
        header[0x10:0x18] = model_bytes

        return bytes(header) + record

    @classmethod
    def validate_profile_binary(cls, profile_bytes: bytes, expected_model: str = None, expected_bios_ver: str = None):
        if len(profile_bytes) < cls.HEADER_SIZE:
            return False, 0xc8, "Invalid Profile: File smaller than 56-byte header"

        magic = struct.unpack("<H", profile_bytes[0:2])[0]
        if magic != cls.MAGIC:
            return False, 0xc8, f"Invalid Profile: Magic mismatch (0x{magic:04x} != 0x1964)"

        hdr_size = profile_bytes[5]
        if hdr_size != cls.HEADER_SIZE:
            return False, 0xc8, f"Invalid Profile: Header size mismatch ({hdr_size} != 56)"

        payload_bytes = profile_bytes[cls.HEADER_SIZE:]
        calc_sum = sum(payload_bytes) & 0xFF
        file_sum = profile_bytes[7]
        if calc_sum != file_sum:
            return False, 0xc9, f"Wrong Checksum: calculated 0x{calc_sum:02x} != stored 0x{file_sum:02x}"

        if expected_model:
            exp_bytes = expected_model.encode("ascii")[:8].ljust(8, b"\x00")
            file_model = profile_bytes[0x10:0x18]
            if file_model != exp_bytes:
                return False, 0xca, f"Wrong Model Name: '{file_model}' != '{exp_bytes}'"

        if expected_bios_ver:
            exp_ver_bytes = expected_bios_ver.encode("ascii")[:4].ljust(4, b"\x00")
            file_ver = profile_bytes[0x0c:0x10]
            if file_ver != exp_ver_bytes:
                return True, 0xcb, f"Profile created by different BIOS version: '{file_ver}' != '{exp_ver_bytes}' (BIOS prompts Y/N)"

        return True, 0xb4, "Profile Loaded (All AMITSE validation gates passed)"

    @classmethod
    def export_all(cls, target_dir: str or Path, hw_profile, base_setup: bytes = None, bios_image_path: str = None, linux_only: bool = False):
        target_path = Path(target_dir)

        if base_setup is None:
            efivar_path = Path("/sys/firmware/efi/efivars/Setup-ec87d643-eba4-4bb5-a1e5-3f3e36b20da9")
            if efivar_path.is_file():
                raw = efivar_path.read_bytes()
                base_setup = raw[4:]
            else:
                base_setup = bytes(cls.SETUP_SIZE)

        model_id, bios_ver = cls.derive_metadata(hw_profile, bios_image_path)

        profiles = [
            ("STABILITY.PRO",        ProfileGenerator.build_stability_deltas(hw_profile, linux_mode=False), "Failsafe 24/7 (JEDEC 2133 MT/s @ 1.20V, Typical Current Idle)"),
            ("BALANCED.PRO",         ProfileGenerator.build_balanced_deltas(hw_profile, linux_mode=False),  f"Gold Standard Daily Driver (XMP {hw_profile.rated_xmp_speed} MT/s, PB2, Above4G, Re-Size BAR)"),
            ("PERFORMANCE.PRO",      ProfileGenerator.build_performance_deltas(hw_profile, linux_mode=False), f"Enthusiast Performance (XMP {hw_profile.rated_xmp_speed} MT/s, Re-Size BAR, CPPC)"),
            ("STABILITY_LINUX.PRO",  ProfileGenerator.build_stability_deltas(hw_profile, linux_mode=True),  "Linux Kernel 6.x Failsafe (JEDEC @ 1.20V, C6-Freeze-Immune, IOMMU On, FastBoot Off)"),
            ("BALANCED_LINUX.PRO",   ProfileGenerator.build_balanced_deltas(hw_profile, linux_mode=True),   f"Linux Kernel 6.x Gold Standard (XMP {hw_profile.rated_xmp_speed}, amd-pstate-epp CPPC, BAR1, C6-Immune)"),
            ("PERFORMANCE_LINUX.PRO",ProfileGenerator.build_performance_deltas(hw_profile, linux_mode=True),f"Linux Kernel 6.x Ultra-Low-Latency (XMP {hw_profile.rated_xmp_speed}, BAR1, CPPC EEVDF)")
        ]

        if linux_only:
            profiles = [p for p in profiles if "_LINUX" in p[0]]

        results = []
        try:
            target_path.mkdir(parents=True, exist_ok=True)
            write_allowed = True
        except PermissionError:
            write_allowed = False

        fallback_dir = Path("./profiles")
        fallback_dir.mkdir(parents=True, exist_ok=True)

        for filename, deltas, desc in profiles:
            pbin = cls.build_profile_binary(base_setup, deltas, model_id, bios_ver)
            valid, code, msg = cls.validate_profile_binary(pbin, model_id, bios_ver)

            local_file = fallback_dir / filename
            local_file.write_bytes(pbin)

            dest_file = None
            if write_allowed:
                dest_file = target_path / filename
                dest_file.write_bytes(pbin)

            results.append({
                "filename": filename,
                "description": desc,
                "size": len(pbin),
                "model_id": model_id,
                "bios_version": bios_ver,
                "checksum": pbin[7],
                "valid": valid,
                "status_code": hex(code),
                "status_msg": msg,
                "local_path": str(local_file),
                "dest_path": str(dest_file) if dest_file else None,
                "is_linux": "_LINUX" in filename
            })

        return results, write_allowed
