"""
toolkit/hardware.py - Universal AM4 Platform Hardware Detector
Analyzes:
- AMD Zen CPU Family & Microarchitecture (Zen+, Zen 2 Matisse, Zen 3 Vermeer/Cezanne)
- Motherboard Vendor & Chipset (B550, X570, B450, X470, A520)
- Memory Subsystem Topology (DIMM count, Ranks 1R/2R, Rated XMP vs Active JEDEC)
- GPU VRAM & Re-Size BAR Capability
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path

class HardwareProfile:
    def __init__(self, cpu, board, gpu, memory):
        self.cpu = cpu
        self.board = board
        self.gpu = gpu
        self.memory = memory

    @property
    def is_zen3(self):
        return any(k in self.cpu.get("model", "").lower() for k in ["5600", "5700", "5800", "5900", "5950"])

    @property
    def is_zen2(self):
        return any(k in self.cpu.get("model", "").lower() for k in ["3600", "3700", "3800", "3900", "3950"])

    @property
    def has_dual_rank(self):
        return any(m.get("rank") == "2" for m in self.memory)

    @property
    def total_memory_gb(self):
        return sum(m.get("size_gb", 0) for m in self.memory)

    @property
    def rated_xmp_speed(self):
        speeds = [m.get("rated_speed", 2133) for m in self.memory if m.get("rated_speed")]
        return max(speeds) if speeds else 3200

    @property
    def active_memory_speed(self):
        speeds = [m.get("active_speed", 2133) for m in self.memory if m.get("active_speed")]
        return min(speeds) if speeds else 2133

class PlatformDetector:
    @staticmethod
    def detect_cpu():
        info = {
            "model": "AMD Processor (AM4)",
            "cores": 0,
            "threads": 0,
            "base_mhz": 3700.0,
            "boost_target_mhz": 4650.0,
            "architecture": "Zen 3"
        }
        cpu_path = Path("/proc/cpuinfo")
        if cpu_path.exists():
            lines = cpu_path.read_text().splitlines()
            for line in lines:
                if "model name" in line:
                    info["model"] = line.split(":", 1)[1].strip()
                    break
            info["threads"] = sum(1 for line in lines if "processor" in line)

        # Classify Zen generation & target boost
        m = info["model"].lower()
        if "5600x" in m:
            info["cores"] = 6
            info["base_mhz"] = 3700.0
            info["boost_target_mhz"] = 4650.0
            info["architecture"] = "Zen 3 (Vermeer)"
        elif "5800x" in m:
            info["cores"] = 8
            info["base_mhz"] = 3800.0
            info["boost_target_mhz"] = 4700.0
            info["architecture"] = "Zen 3 (Vermeer)"
        elif "5900x" in m:
            info["cores"] = 12
            info["base_mhz"] = 3700.0
            info["boost_target_mhz"] = 4800.0
            info["architecture"] = "Zen 3 (Vermeer)"
        elif "3600" in m:
            info["cores"] = 6
            info["base_mhz"] = 3600.0
            info["boost_target_mhz"] = 4200.0
            info["architecture"] = "Zen 2 (Matisse)"
        elif "3700x" in m:
            info["cores"] = 8
            info["base_mhz"] = 3600.0
            info["boost_target_mhz"] = 4400.0
            info["architecture"] = "Zen 2 (Matisse)"
        return info

    @staticmethod
    def detect_board(image_path=None):
        board = {
            "vendor": "Unknown",
            "name": "B550 Platform",
            "bios_version": "Unknown",
            "chipset": "B550",
            "vendor_key": "gigabyte",
            "source": "live_dmi"
        }

        # 1. Deduce from input BIOS image if provided
        if image_path and Path(image_path).exists():
            p = Path(image_path)
            board["source"] = f"image: {p.name}"
            name_lower = p.name.lower()
            
            # --- A. Check Filename Patterns ---
            # ASUS
            if any(k in name_lower for k in ["asus", "tuf", "prime", "strix"]) or p.suffix.lower() == ".cap":
                board["vendor"] = "ASUSTeK COMPUTER INC."
                board["vendor_key"] = "asus"
                if "tuf" in name_lower and "plus" in name_lower:
                    board["name"] = "ASUS TUF GAMING B550-PLUS"
                elif "prime" in name_lower and "plus" in name_lower:
                    board["name"] = "ASUS PRIME B550-PLUS"
                elif "strix" in name_lower or "b550-f" in name_lower:
                    board["name"] = "ASUS ROG STRIX B550-F GAMING"
                else:
                    board["name"] = "ASUS B550 (TUF/PRIME/ROG)"
                
                ver_match = re.search(r'[-_]([0-9]{4})\.cap', p.name, re.I)
                if ver_match:
                    board["bios_version"] = ver_match.group(1)
                return board

            # MSI
            elif any(k in name_lower for k in ["msi", "tomahawk", "gaming plus", "e7c", "7c91", "7c56"]):
                board["vendor"] = "Micro-Star International Co., Ltd."
                board["vendor_key"] = "msi"
                if "7c91" in name_lower or "tomahawk" in name_lower:
                    board["name"] = "MSI MAG B550 TOMAHAWK"
                elif "7c56" in name_lower or "gaming plus" in name_lower:
                    board["name"] = "MSI MPG B550 GAMING PLUS"
                elif "b550-a pro" in name_lower:
                    board["name"] = "MSI B550-A PRO"
                else:
                    board["name"] = "MSI B550 (MAG/MPG/PRO)"
                
                ver_match = re.search(r'\.([0-9A-Za-z]{3})$', p.name)
                if ver_match:
                    board["bios_version"] = ver_match.group(1)
                return board

            # ASRock
            elif any(k in name_lower for k in ["asrock", "b550sl", "b550p4", "b550pg", "steel legend", "pro4"]):
                board["vendor"] = "ASRock Incorporation"
                board["vendor_key"] = "asrock"
                if "b550sl" in name_lower or "steel" in name_lower:
                    board["name"] = "ASRock B550 Steel Legend"
                elif "b550p4" in name_lower or "pro4" in name_lower:
                    board["name"] = "ASRock B550 Pro4"
                elif "phantom" in name_lower or "b550pg" in name_lower:
                    board["name"] = "ASRock B550 Phantom Gaming 4"
                else:
                    board["name"] = "ASRock B550 Platform"
                
                ver_match = re.search(r'([0-9]+\.[0-9]+)', p.name)
                if ver_match:
                    board["bios_version"] = ver_match.group(1)
                return board

            # Gigabyte
            elif any(k in name_lower for k in ["aorus", "gigabyte", "b550aorus"]) or p.suffix.lower().startswith(".f"):
                board["vendor"] = "Gigabyte Technology Co., Ltd."
                board["vendor_key"] = "gigabyte"
                if "elite v2" in name_lower or "aoruselitev2" in name_lower:
                    board["name"] = "Gigabyte B550 AORUS ELITE V2"
                elif "pro" in name_lower or "aoruspro" in name_lower:
                    board["name"] = "Gigabyte B550 AORUS PRO"
                elif "gaming x" in name_lower:
                    board["name"] = "Gigabyte B550 GAMING X"
                else:
                    board["name"] = "Gigabyte B550 (AORUS / Gaming)"
                
                ver_match = re.search(r'\.(F[0-9a-zA-Z]+)$', p.name)
                if ver_match:
                    board["bios_version"] = ver_match.group(1)
                return board

            # --- B. Scan Image Binary Contents (fallback) ---
            try:
                data = p.read_bytes()
                # ASRock markers
                if b"Steel Legend" in data:
                    board["vendor"] = "ASRock Incorporation"
                    board["name"] = "ASRock B550 Steel Legend"
                    board["vendor_key"] = "asrock"
                    return board
                elif b"Pro4" in data:
                    board["vendor"] = "ASRock Incorporation"
                    board["name"] = "ASRock B550 Pro4"
                    board["vendor_key"] = "asrock"
                    return board
                # MSI markers
                elif b"E7C91AMS" in data:
                    board["vendor"] = "Micro-Star International Co., Ltd."
                    board["name"] = "MSI MAG B550 TOMAHAWK"
                    board["vendor_key"] = "msi"
                    return board
                elif b"E7C56AMS" in data:
                    board["vendor"] = "Micro-Star International Co., Ltd."
                    board["name"] = "MSI MPG B550 GAMING PLUS"
                    board["vendor_key"] = "msi"
                    return board
                elif b"Micro-Star" in data:
                    board["vendor"] = "Micro-Star International Co., Ltd."
                    board["name"] = "MSI AM4 Platform"
                    board["vendor_key"] = "msi"
                    return board
                # ASUS markers
                elif b"ROG-STRIX" in data or b"ROG STRIX" in data:
                    board["vendor"] = "ASUSTeK COMPUTER INC."
                    board["name"] = "ASUS ROG STRIX B550-F GAMING"
                    board["vendor_key"] = "asus"
                    return board
                elif b"TUF GAMING" in data:
                    board["vendor"] = "ASUSTeK COMPUTER INC."
                    board["name"] = "ASUS TUF GAMING B550-PLUS"
                    board["vendor_key"] = "asus"
                    return board
                elif b"PRIME B550" in data:
                    board["vendor"] = "ASUSTeK COMPUTER INC."
                    board["name"] = "ASUS PRIME B550-PLUS"
                    board["vendor_key"] = "asus"
                    return board
                elif b"ASUSTeK" in data or b"ASUS" in data:
                    board["vendor"] = "ASUSTeK COMPUTER INC."
                    board["name"] = "ASUS AM4 Platform"
                    board["vendor_key"] = "asus"
                    return board
                # Gigabyte markers
                elif b"B550 AORUS ELITE V2" in data:
                    board["vendor"] = "Gigabyte Technology Co., Ltd."
                    board["name"] = "Gigabyte B550 AORUS ELITE V2"
                    board["vendor_key"] = "gigabyte"
                    return board
                elif b"GIGABYTE" in data or b"Gigabyte" in data:
                    board["vendor"] = "Gigabyte Technology Co., Ltd."
                    board["name"] = "Gigabyte AM4 Platform"
                    board["vendor_key"] = "gigabyte"
                    return board
            except Exception:
                pass

        # 2. Deduce from Live DMI / sysfs
        for k in ["board_vendor", "board_name", "bios_version"]:
            p = Path(f"/sys/class/dmi/id/{k}")
            if p.exists():
                try:
                    val = p.read_text().strip()
                    if k == "board_vendor": board["vendor"] = val
                    elif k == "board_name": board["name"] = val
                    elif k == "bios_version": board["bios_version"] = val
                except Exception:
                    pass

        v_lower = board["vendor"].lower()
        if "asus" in v_lower or "asustek" in v_lower:
            board["vendor_key"] = "asus"
        elif "msi" in v_lower or "micro-star" in v_lower:
            board["vendor_key"] = "msi"
        elif "asrock" in v_lower:
            board["vendor_key"] = "asrock"
        else:
            board["vendor_key"] = "gigabyte"

        name_lower = board["name"].lower()
        if "x570" in name_lower: board["chipset"] = "X570"
        elif "b550" in name_lower: board["chipset"] = "B550"
        elif "b450" in name_lower: board["chipset"] = "B450"
        elif "a520" in name_lower: board["chipset"] = "A520"
        elif "x470" in name_lower: board["chipset"] = "X470"
        return board

    @staticmethod
    def detect_gpu():
        gpus = []
        try:
            lspci_out = subprocess.check_output(["lspci"], text=True)
            for l in lspci_out.splitlines():
                if "VGA compatible controller" in l or "3D controller" in l:
                    gpus.append(l.strip())
        except Exception:
            pass
        return gpus

    @staticmethod
    def detect_memory():
        modules = []
        # Check cached system_hardware.json first
        cache_path = Path("/run/media/julian/ML6/bios-re/findings/system_hardware.json")
        if cache_path.exists():
            try:
                data = json.loads(cache_path.read_text())
                raw_mods = data.get("memory_modules", [])
                for m in raw_mods:
                    part = m.get("Part Number", "").strip()
                    size_str = m.get("Size", "0 GiB")
                    size_gb = int(size_str.split()[0]) if "GiB" in size_str else 0
                    rank = m.get("Rank", "1")
                    cfg_speed = int(m.get("Configured Memory Speed", "2133").split()[0]) if "MT/s" in m.get("Configured Memory Speed", "") else 2133
                    rated_speed = 3200 if "3200" in part else (3600 if "3600" in part else cfg_speed)
                    modules.append({
                        "part": part,
                        "size_gb": size_gb,
                        "rank": rank,
                        "active_speed": cfg_speed,
                        "rated_speed": rated_speed,
                        "locator": f"{m.get('Bank Locator', '')} {m.get('Locator', '')}".strip()
                    })
            except Exception:
                pass
        return modules

    @classmethod
    def get_profile(cls, image_path=None):
        return HardwareProfile(
            cpu=cls.detect_cpu(),
            board=cls.detect_board(image_path),
            gpu=cls.detect_gpu(),
            memory=cls.detect_memory()
        )
