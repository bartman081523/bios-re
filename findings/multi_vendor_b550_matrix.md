# Multi-Vendor B550 Motherboard Firmware Matrix & Taxonomy Guide

Universal architecture and taxonomy matrix for AMD B550 motherboards across all four major vendors: **Gigabyte**, **ASUS**, **MSI**, and **ASRock**.

---

## 1. Verified Motherboard Firmware Portfolio

The following 8 reference BIOS images across all 4 key motherboard manufacturers have been acquired, structurally analyzed, and integrated into the `bios-re` suite:

| Manufacturer | Motherboard Model | BIOS Version | ROM File / Format | Size | Firmware Volume Signature |
|---|---|---|---|---|---|
| **Gigabyte** | B550 AORUS ELITE V2 (Rev 1.2) | FIb | `B550AORUSELITEV212.FIb` | 16.00 MiB | 6 Firmware Volumes (`_FVH`) |
| **ASUS** | TUF GAMING B550-PLUS | 3607 | `TUF-GAMING-B550-PLUS-ASUS-3607.CAP` | 32.00 MiB + 2KB | 18 Firmware Volumes (`_FVH`) |
| **ASUS** | ROG STRIX B550-F GAMING | 3607 | `ROG-STRIX-B550-F-GAMING-ASUS-3607.CAP` | 32.00 MiB + 2KB | 18 Firmware Volumes (`_FVH`) |
| **ASUS** | PRIME B550-PLUS | 3607 | `PRIME-B550-PLUS-ASUS-3607.CAP` | 32.00 MiB + 2KB | 18 Firmware Volumes (`_FVH`) |
| **MSI** | MAG B550 TOMAHAWK (MS-7C91) | 1.G0 | `E7C91AMS.1G0` | 32.00 MiB | 18 Firmware Volumes (`_FVH`) |
| **MSI** | MPG B550 GAMING PLUS (MS-7C56) | 1.G0 | `E7C56AMS.1G0` | 32.00 MiB | 18 Firmware Volumes (`_FVH`) |
| **ASRock** | B550 Steel Legend | 3.40 | `B550SL_3.40` | 32.00 MiB | 10 Firmware Volumes (`_FVH`) |
| **ASRock** | B550 Pro4 | 3.40 | `B550P4_3.40` | 32.00 MiB | 10 Firmware Volumes (`_FVH`) |

---

## 2. Cross-Vendor Comparative Taxonomy Matrix

| Architectural Subsystem | Gigabyte (Aorus/Gaming) | ASUS (TUF/ROG/Prime) | MSI (Click BIOS 5) | ASRock (Polychrome/Steel) |
|---|---|---|---|---|
| **GUI Mode Switch** | `F2` (Advanced Mode) | `F7` (Advanced Mode) | `F7` (Advanced Mode) | `F6` (Advanced Mode) |
| **Memory Overclocking** | `Tweaker` $\rightarrow$ `Extreme Memory Profile (X.M.P.)` | `Ai Tweaker` $\rightarrow$ `Ai Overclock Tuner` $\rightarrow$ `D.O.C.P.` | `OC` $\rightarrow$ `A-XMP` | `OC Tweaker` $\rightarrow$ `DRAM Timing` $\rightarrow$ `Load XMP Setting` |
| **Infinity Fabric Clock** | `Tweaker` $\rightarrow$ `Advanced Memory` $\rightarrow$ `FCLK Frequency` | `Ai Tweaker` $\rightarrow$ `FCLK Frequency` | `OC` $\rightarrow$ `FCLK Frequency` | `OC Tweaker` $\rightarrow$ `Infinity Fabric Frequency and Dividers` |
| **Dual-Rank Stabilization** | `Tweaker` $\rightarrow$ `Advanced Memory` $\rightarrow$ `Gear Down Mode` | `Ai Tweaker` $\rightarrow$ `DRAM Timing Control` $\rightarrow$ `Gear Down Mode` | `OC` $\rightarrow$ `Advanced DRAM Configuration` $\rightarrow$ `Gear Down Mode` | `OC Tweaker` $\rightarrow$ `DRAM Timing Configuration` $\rightarrow$ `Gear Down Mode` |
| **Above 4G Decoding** | `Settings` $\rightarrow$ `Above 4G Decoding` | `Advanced` $\rightarrow$ `PCI Subsystem` $\rightarrow$ `Above 4G Decoding` (or `[F4]`) | `Settings` $\rightarrow$ `Advanced` $\rightarrow$ `PCIe/PCI Sub-system` $\rightarrow$ `Above 4G` | `Advanced` $\rightarrow$ `PCI Configuration` $\rightarrow$ `Above 4G Decoding` |
| **Re-Size BAR Support** | `Settings` $\rightarrow$ `Re-Size BAR Support` | `Advanced` $\rightarrow$ `PCI Subsystem` $\rightarrow$ `Re-Size BAR Support` (or `[F4]`) | `Settings` $\rightarrow$ `Advanced` $\rightarrow$ `PCIe/PCI Sub-system` $\rightarrow$ `Re-Size BAR` | `Advanced` $\rightarrow$ `PCI Configuration` $\rightarrow$ `Re-Size BAR Support` |
| **Precision Boost 2 (PB2)**| `Tweaker` $\rightarrow$ `Core Performance Boost` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common` $\rightarrow$ `Core Performance Boost` | `OC` $\rightarrow$ `Advanced CPU Configuration` $\rightarrow$ `Core Performance Boost` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common` $\rightarrow$ `Core Performance Boost` |
| **C6 Idle Anti-Freeze** | `Tweaker` $\rightarrow$ `Power Supply Idle Control` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common` $\rightarrow$ `Power Supply Idle Control` | `OC` $\rightarrow$ `Advanced CPU Configuration` $\rightarrow$ `AMD CBS` $\rightarrow$ `Power Supply Idle Control` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common` $\rightarrow$ `Power Supply Idle Control` |
| **Autonomous CPPC (Linux)**| `Tweaker` $\rightarrow$ `Advanced CPU` $\rightarrow$ `CPPC` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `NBIO Common` $\rightarrow$ `SMU` $\rightarrow$ `CPPC` | `OC` $\rightarrow$ `Advanced CPU` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common` $\rightarrow$ `CPPC` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common Options` $\rightarrow$ `CPPC` |
| **Hardware IOMMU (AMD-Vi)** | `Settings` $\rightarrow$ `AMD IOMMU` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `NBIO Common` $\rightarrow$ `IOMMU` | `OC` $\rightarrow$ `Advanced CPU` $\rightarrow$ `AMD Overclocking` $\rightarrow$ `AMD CBS` $\rightarrow$ `IOMMU` | `Advanced` $\rightarrow$ `AMD PBS` $\rightarrow$ `AMD IOMMU` |
| **Firmware Dropper (WPBT)** | `Settings` $\rightarrow$ `APP Center Download & Install = Disabled` | `Tool` $\rightarrow$ `ASUS Armoury Crate` $\rightarrow$ `Download & Install app = Disabled` | `Settings` $\rightarrow$ `Advanced` $\rightarrow$ `MSI Driver Utility Installer = Disabled` | `Tool` $\rightarrow$ `Auto Driver Installer = Disabled` |
| **CSM Compatibility** | `Boot` $\rightarrow$ `CSM Support = Disabled` | `Boot` $\rightarrow$ `CSM (Compatibility Support Module)` $\rightarrow$ `Launch CSM = Disabled` | `Settings` $\rightarrow$ `Advanced` $\rightarrow$ `Windows OS Configuration` $\rightarrow$ `BIOS CSM/UEFI = UEFI` | `Boot` $\rightarrow$ `CSM (Compatibility Support Module)` $\rightarrow$ `CSM = Disabled` |
| **Fast Boot** | `Boot` $\rightarrow$ `Fast Boot = Disabled` | `Boot` $\rightarrow$ `Fast Boot = Disabled` | `Settings` $\rightarrow$ `Boot` $\rightarrow$ `MSI Fast Boot = Disabled` | `Boot` $\rightarrow$ `Fast Boot = Disabled` |
| **Save & Reset Shortcut** | `F10` | `F10` | `F10` | `F10` |

---

## 3. Vendor-Specific Firmware Format Peculiarities

### 1. ASUS (.CAP format)
* **Capsule Header:** 2,048-byte RSA security header (`4A3CA68B-7723-48FB-803D-578CC1FEC44D`).
* **FlashBack Procedure:** USB BIOS FlashBack requires renaming the `.CAP` file according to model prefix (e.g., `TGB550PS.CAP` for TUF Gaming B550-Plus, `SB550FG.CAP` for ROG Strix B550-F Gaming).
* **Hardware Shortcut:** Features a dedicated `[F4]` hotkey in the top toolbar to toggle Above 4G Decoding and Re-Size BAR simultaneously.

### 2. MSI (Raw Aptio ROM)
* **File Structure:** Raw 32 MiB binary image named `E[Model]AMS.[Version]` (e.g. `E7C91AMS.1G0`).
* **FlashBack Procedure:** To use the rear Flash BIOS Button, rename the ROM file to **`MSI.ROM`** on a FAT32 drive.
* **Firmware Dropper:** MSI packages the "MSI Driver Utility Installer" inside the ACPI WPBT table; must be disabled under `Settings -> Advanced`.

### 3. ASRock (Instant Flash ROM)
* **File Structure:** Raw 32 MiB binary image named `[Model]_[Version]` (e.g. `B550SL_3.40`, `B550P4_3.40`).
* **FlashBack Procedure:** Supports ASRock Instant Flash directly in the UEFI `Tool` tab or BIOS Flashback button on select boards (rename to `CREATIVE.ROM` or model-specific name).
* **Firmware Dropper:** "Auto Driver Installer" in the `Tool` menu must be disabled to maintain clean ACPI tables.

### 4. Gigabyte (Q-Flash Plus)
* **File Structure:** 16 MiB or 32 MiB raw image named `[Model].[Rev/Ver]` (e.g. `B550AORUSELITEV212.FIb`).
* **FlashBack Procedure:** Q-Flash Plus requires the file to be named **`GIGABYTE.BIN`** on a FAT32 USB drive.
* **AMITSE Profiles:** Uses standard AMI Aptio AMITSE binary format (`.PRO`, 704 bytes) with Magic `0x1964` and project model QWORD validation.
