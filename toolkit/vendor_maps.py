"""
toolkit/vendor_maps.py - Multi-Vendor BIOS Taxonomy & Menu Path Translator
Supports:
- Gigabyte (AORUS, Gaming, Ultra Durable)
- ASUS (TUF Gaming, PRIME, ROG STRIX)
- MSI (MAG, MPG, PRO, B550 Tomahawk)
- ASRock (Steel Legend, Pro4, Phantom)
"""

VENDOR_TAXONOMY = {
    "gigabyte": {
        "display_name": "Gigabyte B550 (AORUS / Gaming)",
        "menu_mode_toggle": "F2 (Advanced Mode)",
        "save_exit_key": "F10",
        "save_and_exit_key": "F10",
        "save_and_exit_menu": "Save & Exit Setup",
        "terms": {
            "xmp": {
                "name": "Extreme Memory Profile (X.M.P.)",
                "tab": "M.I.T.",
                "path": "M.I.T. -> Advanced Memory Settings -> Extreme Memory Profile(X.M.P.)",
                "target": "Profile 1"
            },
            "fclk": {
                "name": "Infinity Fabric Frequency and Dividers",
                "tab": "M.I.T.",
                "path": "M.I.T. -> Advanced Memory Settings -> Infinity Fabric Frequency and Dividers",
                "target": "1600MHz (Synchronous 1:1)"
            },
            "cpb": {
                "name": "Core Performance Boost",
                "tab": "M.I.T.",
                "path": "M.I.T. -> Advanced Frequency Settings -> Advanced CPU Settings -> Core Performance Boost",
                "target": "Auto"
            },
            "idle": {
                "name": "Power Supply Idle Control",
                "tab": "M.I.T.",
                "path": "M.I.T. -> Advanced Frequency Settings -> Advanced CPU Settings -> Power Supply Idle Control",
                "target": "Typical Current Idle"
            },
            "above4g": {
                "name": "Above 4G Decoding",
                "tab": "Peripherals",
                "path": "Peripherals -> Above 4G Decoding",
                "target": "Enabled"
            },
            "bar": {
                "name": "Re-Size BAR Support",
                "tab": "Peripherals",
                "path": "Peripherals -> Re-Size BAR Support",
                "target": "Auto"
            },
            "wpbt": {
                "name": "APP Center Download & Install",
                "tab": "Peripherals",
                "path": "Peripherals -> APP Center Download & Install Configuration -> APP Center Download & Install",
                "target": "Disabled"
            },
            "csm": {
                "name": "CSM Support",
                "tab": "BIOS",
                "path": "BIOS -> CSM Support",
                "target": "Disabled"
            },
            "iommu": {
                "name": "AMD IOMMU",
                "tab": "Peripherals",
                "path": "Peripherals -> AMD IOMMU (or Chipset -> IOMMU)",
                "target": "Enabled"
            },
            "fastboot": {
                "name": "Fast Boot",
                "tab": "BIOS",
                "path": "BIOS -> Fast Boot",
                "target": "Disabled"
            }
        }
    },

    "asus": {
        "display_name": "ASUS B550 (TUF GAMING / PRIME / ROG STRIX)",
        "menu_mode_toggle": "F7 (Advanced Mode)",
        "save_exit_key": "F10",
        "save_and_exit_key": "F10",
        "save_and_exit_menu": "Save Changes & Reset",
        "shortcut_bar": "[F4] Re-Size BAR Quick Toggle in top toolbar",
        "terms": {
            "xmp": {
                "name": "Ai Overclock Tuner (D.O.C.P.)",
                "tab": "Ai Tweaker",
                "path": "Ai Tweaker -> Ai Overclock Tuner -> D.O.C.P. (D.O.C.P. Standard)",
                "target": "D.O.C.P."
            },
            "fclk": {
                "name": "FCLK Frequency",
                "tab": "Ai Tweaker",
                "path": "Ai Tweaker -> FCLK Frequency",
                "target": "1600MHz (Synchronous 1:1)"
            },
            "cpb": {
                "name": "Core Performance Boost / PBO",
                "tab": "Ai Tweaker / Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> Core Performance Boost",
                "target": "Auto"
            },
            "idle": {
                "name": "Power Supply Idle Control",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> Power Supply Idle Control",
                "target": "Typical Current Idle"
            },
            "above4g": {
                "name": "Above 4G Decoding",
                "tab": "Advanced",
                "path": "Advanced -> PCI Subsystem Settings -> Above 4G Decoding (or [F4] Key)",
                "target": "Enabled"
            },
            "bar": {
                "name": "Re-Size BAR Support",
                "tab": "Advanced",
                "path": "Advanced -> PCI Subsystem Settings -> Re-Size BAR Support (or [F4] Key)",
                "target": "Auto"
            },
            "wpbt": {
                "name": "ASUS Armoury Crate",
                "tab": "Tool",
                "path": "Tool -> ASUS Armoury Crate -> Download & Install ARMOURY CRATE app",
                "target": "Disabled"
            },
            "csm": {
                "name": "Launch CSM",
                "tab": "Boot",
                "path": "Boot -> CSM (Compatibility Support Module) -> Launch CSM",
                "target": "Disabled"
            },
            "iommu": {
                "name": "IOMMU",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> NBIO Common Options -> IOMMU",
                "target": "Enabled"
            },
            "fastboot": {
                "name": "Fast Boot",
                "tab": "Boot",
                "path": "Boot -> Fast Boot",
                "target": "Disabled"
            },
            "cppc": {
                "name": "CPPC",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> CPPC",
                "target": "Enabled"
            },
            "cppc_pref": {
                "name": "CPPC Preferred Cores",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> CPPC Preferred Cores",
                "target": "Enabled"
            },
            "gdm": {
                "name": "Gear Down Mode",
                "tab": "OC Tweaker",
                "path": "OC Tweaker -> DRAM Timing Configuration -> Gear Down Mode",
                "target": "Enabled"
            },
            "cppc": {
                "name": "CPPC",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> NBIO Common Options -> SMU Common Options -> CPPC",
                "target": "Enabled"
            },
            "cppc_pref": {
                "name": "CPPC Preferred Cores",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> NBIO Common Options -> SMU Common Options -> CPPC Preferred Cores",
                "target": "Enabled"
            },
            "gdm": {
                "name": "Gear Down Mode",
                "tab": "Ai Tweaker",
                "path": "Ai Tweaker -> DRAM Timing Control -> Gear Down Mode",
                "target": "Enabled"
            }
        }
    },

    "msi": {
        "display_name": "MSI B550 (MAG / MPG / PRO)",
        "menu_mode_toggle": "F7 (Advanced Mode)",
        "save_exit_key": "F10",
        "save_and_exit_key": "F10",
        "save_and_exit_menu": "Save Changes and Reboot",
        "terms": {
            "xmp": {
                "name": "A-XMP",
                "tab": "OC",
                "path": "OC -> A-XMP",
                "target": "Profile 1"
            },
            "fclk": {
                "name": "FCLK Frequency",
                "tab": "OC",
                "path": "OC -> FCLK Frequency",
                "target": "1600MHz"
            },
            "cpb": {
                "name": "Core Performance Boost",
                "tab": "OC",
                "path": "OC -> Advanced CPU Configuration -> Core Performance Boost",
                "target": "Auto"
            },
            "idle": {
                "name": "Power Supply Idle Control",
                "tab": "OC",
                "path": "OC -> Advanced CPU Configuration -> Power Supply Idle Control",
                "target": "Typical Current Idle"
            },
            "above4g": {
                "name": "Above 4G Decoding",
                "tab": "Settings",
                "path": "Settings -> Advanced -> PCIe/PCI Sub-system Settings -> Above 4G Memory/Crypto Currency Mining",
                "target": "Enabled"
            },
            "bar": {
                "name": "Re-Size BAR Support",
                "tab": "Settings",
                "path": "Settings -> Advanced -> PCIe/PCI Sub-system Settings -> Re-Size BAR Support",
                "target": "Auto"
            },
            "wpbt": {
                "name": "MSI Driver Utility Installer",
                "tab": "Settings",
                "path": "Settings -> Advanced -> MSI Driver Utility Installer",
                "target": "Disabled"
            },
            "csm": {
                "name": "BIOS CSM/UEFI Mode",
                "tab": "Settings",
                "path": "Settings -> Advanced -> Windows OS Configuration -> BIOS CSM/UEFI Mode",
                "target": "UEFI"
            },
            "iommu": {
                "name": "AMD IOMMU",
                "tab": "OC",
                "path": "OC -> Advanced CPU Configuration -> AMD Overclocking -> AMD CBS -> NBIO Common Options -> IOMMU",
                "target": "Enabled"
            },
            "fastboot": {
                "name": "MSI Fast Boot",
                "tab": "Settings",
                "path": "Settings -> Boot -> MSI Fast Boot",
                "target": "Disabled"
            },
            "cppc": {
                "name": "CPPC",
                "tab": "OC",
                "path": "OC -> Advanced CPU Configuration -> AMD CBS -> CPU Common Options -> CPPC",
                "target": "Enabled"
            },
            "cppc_pref": {
                "name": "CPPC Preferred Cores",
                "tab": "OC",
                "path": "OC -> Advanced CPU Configuration -> AMD CBS -> CPU Common Options -> CPPC Preferred Cores",
                "target": "Enabled"
            },
            "gdm": {
                "name": "Gear Down Mode",
                "tab": "OC",
                "path": "OC -> Advanced DRAM Configuration -> Gear Down Mode",
                "target": "Enabled"
            }
        }
    },

    "asrock": {
        "display_name": "ASRock B550 (Steel Legend / Pro4 / Phantom)",
        "menu_mode_toggle": "F6 (Advanced Mode)",
        "save_exit_key": "F10",
        "save_and_exit_key": "F10",
        "save_and_exit_menu": "Save Changes and Exit",
        "terms": {
            "xmp": {
                "name": "Load XMP Setting",
                "tab": "OC Tweaker",
                "path": "OC Tweaker -> DRAM Timing Configuration -> Load XMP Setting",
                "target": "XMP 2.0 Profile 1"
            },
            "fclk": {
                "name": "Infinity Fabric Frequency and Dividers",
                "tab": "OC Tweaker",
                "path": "OC Tweaker -> DRAM Timing Configuration -> Infinity Fabric Frequency and Dividers",
                "target": "1600MHz"
            },
            "cpb": {
                "name": "Core Performance Boost",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> Core Performance Boost",
                "target": "Auto"
            },
            "idle": {
                "name": "Power Supply Idle Control",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> Power Supply Idle Control",
                "target": "Typical Current Idle"
            },
            "above4g": {
                "name": "Above 4G Decoding",
                "tab": "Advanced",
                "path": "Advanced -> PCI Configuration -> Above 4G Decoding",
                "target": "Enabled"
            },
            "bar": {
                "name": "Re-Size BAR Support",
                "tab": "Advanced",
                "path": "Advanced -> PCI Configuration -> Re-Size BAR Support",
                "target": "Auto"
            },
            "wpbt": {
                "name": "Auto Driver Installer",
                "tab": "Tool",
                "path": "Tool -> Auto Driver Installer",
                "target": "Disabled"
            },
            "csm": {
                "name": "CSM",
                "tab": "Boot",
                "path": "Boot -> CSM (Compatibility Support Module) -> CSM",
                "target": "Disabled"
            },
            "iommu": {
                "name": "AMD IOMMU",
                "tab": "Advanced",
                "path": "Advanced -> AMD PBS -> AMD IOMMU",
                "target": "Enabled"
            },
            "fastboot": {
                "name": "Fast Boot",
                "tab": "Boot",
                "path": "Boot -> Fast Boot",
                "target": "Disabled"
            },
            "cppc": {
                "name": "CPPC",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> CPPC",
                "target": "Enabled"
            },
            "cppc_pref": {
                "name": "CPPC Preferred Cores",
                "tab": "Advanced",
                "path": "Advanced -> AMD CBS -> CPU Common Options -> CPPC Preferred Cores",
                "target": "Enabled"
            },
            "gdm": {
                "name": "Gear Down Mode",
                "tab": "OC Tweaker",
                "path": "OC Tweaker -> DRAM Timing Configuration -> Gear Down Mode",
                "target": "Enabled"
            }
        }
    }
}

class VendorResolver:
    @staticmethod
    def resolve_vendor_key(detected_vendor_str, user_override=None):
        if user_override and user_override.lower() in VENDOR_TAXONOMY:
            return user_override.lower()
        
        v_low = (detected_vendor_str or "").lower()
        if "asus" in v_low or "asustek" in v_low:
            return "asus"
        elif "msi" in v_low or "micro-star" in v_low:
            return "msi"
        elif "asrock" in v_low:
            return "asrock"
        return "gigabyte"

    @classmethod
    def get_taxonomy(cls, detected_vendor_str, user_override=None):
        k = cls.resolve_vendor_key(detected_vendor_str, user_override)
        return VENDOR_TAXONOMY.get(k, VENDOR_TAXONOMY["gigabyte"])

    @staticmethod
    def translate_delta(delta, taxonomy):
        term_id = delta.get("id")
        terms = taxonomy.get("terms", {})
        if term_id in terms:
            t = terms[term_id]
            res = dict(delta)
            res["name"] = t.get("name", delta.get("name"))
            res["menu_path"] = t.get("path", delta.get("menu_path"))
            res["menu_tab"] = t.get("tab", delta.get("menu_tab"))
            return res
        return delta
