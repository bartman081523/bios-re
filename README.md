# AM4 / B550 Epistemic BIOS Engineering Suite

Universal, autonomous BIOS advisory suite and binary profile generator for AMD AM4 (B550 / X570) platforms. Designed for multi-vendor motherboard architectures (Gigabyte, ASUS, MSI, ASRock) with deep Linux kernel 6.x telemetry and AMI Aptio V / AMITSE profile synthesis.

---

## Supported Motherboard Architectures

The suite natively parses and generates verified step-by-step walkthroughs for all 4 major AM4 motherboard manufacturers from live DMI or directly from vendor firmware images (`--image`):

| Vendor | GUI Architecture | Mode Toggle | Tested & Verified Models |
| :--- | :--- | :--- | :--- |
| **Gigabyte** | AORUS / Gaming UI | `F2` | B550 AORUS ELITE V2 (Rev 1.0/1.1/1.2/1.4/1.5), B550 AORUS PRO, B550 GAMING X |
| **ASUS** | ROG / TUF / Prime UEFI | `F7` | TUF GAMING B550-PLUS, ROG STRIX B550-F GAMING, PRIME B550-PLUS |
| **MSI** | Click BIOS 5 | `F7` | MAG B550 TOMAHAWK (MS-7C91), MPG B550 GAMING PLUS (MS-7C56), B550-A PRO |
| **ASRock** | Polychrome / Legend UEFI| `F6` | B550 Steel Legend, B550 Pro4, B550 Phantom Gaming 4 |

For detailed cross-vendor comparisons, consult the [Multi-Vendor B550 Matrix](findings/multi_vendor_b550_matrix.md).

---

## Key Features

1. **Autonomous Motherboard & Platform Detection**
   - Automatically detects CPU microarchitecture (Zen 2 Matisse / Zen 3 Vermeer), memory rank (1R vs 2R Dual-Rank), XMP profiles, and motherboard vendor/model.
   - Derives menu paths and vendor-specific nomenclature (e.g. D.O.C.P. on ASUS, A-XMP on MSI, X.M.P. on Gigabyte) dynamically from live DMI or directly from an input ROM image (`--image`).

2. **Live NVRAM Bottleneck Audit**
   - Directly parses the UEFI `Setup` variable (`ec87d643-eba4-4bb5-a1e5-3f3e36b20da9`) in memory.
   - Detects inactive XMP/DOCP, disabled Core Performance Boost (PB2), constrained GPU VRAM apertures (Above 4G / Re-Size BAR), dangerous C6 low-current power dropouts, and OEM dropper mechanisms (WPBT / APP Center / Armoury Crate).

3. **Linux Kernel 6.x Telemetry Engine (`--linux`)**
   - Audits live firmware settings against Linux kernel subsystems (`cpuidle`, `amd-pstate-epp`, `pci/drm`, `iommu`, `efifb`).
   - Identifies and resolves sporadic Linux C6 desktop freezes, SWIOTLB bounce-buffer degradation (`iommu=soft`), 256MB BAR1 VRAM bottlenecks in DXVK/Proton, and ACPI table clutter.

4. **AMITSE Binary Profile Generator (`--export-profiles`)**
   - Generates 100% compliant, reverse-engineered AMITSE binary profiles (`.PRO`, 704 bytes) for FAT32 EFI partitions (`/boot/efi/BIOS_PROFILES/`).
   - Fully passes internal firmware validation gates (Magic `0x1964`, 8-bit accumulation checksum, Model ID `$BDR` QWORD check, BIOS version DWORD check).
   - Can be loaded directly inside the BIOS setup screen via **F4** (*Load Profile*) or `Save & Exit` -> `Select File in HDD/FDD/USB`.

5. **Linux OS Runtime Switcher (`--linux-profile` / `apply_linux_profile.sh`)**
   - Real-time userspace governor and energy-performance preference (EPP) controller for the running Linux system.
   - Instantly toggles between `stability`, `balanced` (official AMD Zen 3 sweet-spot), and `performance` (zero-latency + NVIDIA persistence mode).

---

## Repository Structure

```
├── am4_advisor.py               # Main unified CLI tool
├── deploy_profiles_to_efi.sh    # One-command root deployment to /boot/efi
├── apply_linux_profile.sh       # One-command Linux OS runtime profile switcher
├── toolkit/
│   ├── advisor.py               # Central coordinator & presentation layer
│   ├── hardware.py              # Hardware detection engine (CPU, DMI, GPU, SPD RAM)
│   ├── nvram.py                 # UEFI NVRAM Setup variable manager
│   ├── profiles.py              # Profile definitions & delta generators
│   ├── vendor_maps.py           # Multi-vendor taxonomy & menu path translator
│   ├── linux_audit.py           # Linux kernel subsystem compatibility auditor
│   ├── linux_runtime.py         # Linux runtime sysfs governor & EPP controller
│   └── profile_exporter.py      # AMITSE binary profile builder & validator
├── profiles/                    # Validated AMITSE binary profile files (.PRO)
│   ├── BALANCED.PRO
│   ├── BALANCED_LINUX.PRO
│   ├── PERFORMANCE.PRO
│   ├── PERFORMANCE_LINUX.PRO
│   ├── STABILITY.PRO
│   └── STABILITY_LINUX.PRO
└── findings/                    # Reverse engineering documentation & decompile logs
    ├── amitse_profile_format_reverse_engineering.md
    ├── asus_b550_plus_analysis.md
    └── am4_linux_compatibility_audit.md
```

---

## Installation & Requirements

- Linux with Python 3.8+
- Root access only for reading live NVRAM (`/sys/firmware/efi/efivars`) or writing to `/boot/efi`
- No third-party Python packages required (standard library only)

```bash
git clone https://github.com/bartman081523/bios-re.git
cd bios-re
chmod +x am4_advisor.py deploy_profiles_to_efi.sh apply_linux_profile.sh
```

---

## Usage Guide

### 1. Standard Step-by-Step Walkthrough
Outputs the exact delta required to reach the target profile on the detected motherboard:
```bash
./am4_advisor.py                    # Balanced profile walkthrough (default)
./am4_advisor.py --profile stability
./am4_advisor.py --profile performance
```

### 2. Linux Kernel Compatibility Audit
Performs a deep inspection of kernel frequency scaling drivers, C6 idle state freeze risks, and DMA isolation:
```bash
./am4_advisor.py --linux
```

### 3. Static BIOS ROM Analysis
Analyzes a vendor BIOS image without a live system (automatically derives taxonomy):
```bash
./am4_advisor.py --image ASUS_B550_PLUS.CAP
```

### 4. 3-Way Comparison Matrix
Compares live NVRAM values against profile targets and Linux prerequisites:
```bash
./am4_advisor.py --compare --linux
```

### 5. Exporting AMITSE Profiles to EFI Partition
Generates all 6 verified binary profiles into `./profiles/` and copies them to `/boot/efi/BIOS_PROFILES/`:
```bash
sudo ./deploy_profiles_to_efi.sh
# Or via CLI:
sudo ./am4_advisor.py --export-profiles /boot/efi/BIOS_PROFILES
```

### 6. Linux OS Runtime Profile Switching
Inspect or switch CPU EPP and GPU power states in the running Linux kernel:
```bash
./apply_linux_profile.sh status
sudo ./apply_linux_profile.sh balanced       # Recommended: amd-pstate-epp balance_performance
sudo ./apply_linux_profile.sh performance    # Unthrottled: EPP performance + GPU persistence mode
sudo ./apply_linux_profile.sh stability      # Energy-saving: EPP balance_power
```

### 7. Direct Reboot to BIOS Setup
Reboots the machine straight into UEFI firmware setup:
```bash
sudo ./am4_advisor.py --reboot
```

---

## Profile Matrix

| Profile | Target Audience | Memory & Fabric | CPU & Boost | Graphics & IOMMU | Linux Telemetry |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **STABILITY** | 24/7 Home Server, KVM, Failsafe | JEDEC 2133 MT/s @ 1.20V | Core Performance Boost Auto | Above 4G Enabled, Re-Size BAR Disabled | Typical Current Idle (C6 freeze immune), IOMMU Enabled |
| **BALANCED** *(Recommended)* | Daily Driver, Gaming, Workstation | XMP Profile 1 (3200 MT/s @ 1.35V), 1:1 FCLK | Precision Boost 2 scaling up to 4.65 GHz | Above 4G Enabled, Re-Size BAR Auto | `amd-pstate-epp` CPPC enabled, C6 freeze immune |
| **PERFORMANCE** | Enthusiast, Low-Latency Compute | XMP Profile 1, 1:1 FCLK tuned | Precision Boost 2 Uncapped | Full BAR1 VRAM Aperture | EEVDF scheduler core priority, Zero-Latency |

---

## License

MIT License. Designed with epistemic humility and Popperian falsification rigor for firmware reverse engineering.
