# ASUS TUF GAMING B550-PLUS / PRIME B550-PLUS: BIOS Architecture & Tuning Analysis

**Target Hardware:** ASUS TUF GAMING B550-PLUS / ASUS PRIME B550-PLUS  
**Firmware Analyzed:** Version 3607 (AGESA ComboV2PI 1.2.0.Ca, Released March/April 2024)  
**Binary Image:** `TUF-GAMING-B550-PLUS-ASUS-3607.CAP` (33,558,528 bytes)  
**Platform Architecture:** AMI Aptio V with ASUS EZ Mode / Advanced Mode GUI  

---

## 1. Capsule Header & Firmware Structure

```
+-------------------------------------------------------------------------+
| ASUS Capsule Header (2,048 Bytes / 0x800)                                |
|  - GUID: 4A3CA68B-7723-48FB-803D-578CC1FEC44D (EFI_CAPSULE_GUID)        |
|  - Header Size: 0x800 | Flags: PERSIST_ACROSS_RESET | RSA Public Key   |
+-------------------------------------------------------------------------+
| UEFI ROM Body (33,556,480 Bytes = Exactly 32.00 MiB / 256 Mbit SPI)     |
|  - 18 Firmware Volumes (_FVH signatures at 0x40800, 0x90800, etc.)      |
|  - AGESA ComboV2PI 1.2.0.Ca (Sinkclose & Zenbleed microcode mitigation) |
|  - Internal Project Model: 'TUF GAMING B550-PLUS'                       |
+-------------------------------------------------------------------------+
```

### USB FlashBack Requirements
* To flash without a CPU or from an unbootable state using the rear FlashBack button:
  * The file must be renamed to **`TGB550PS.CAP`**.
  * The USB flash drive must be formatted to **FAT32** with an MBR partition table.

---

## 2. Comparative Taxonomy: Gigabyte B550 vs. ASUS B550-PLUS

| Subsystem / Feature | Gigabyte B550 AORUS ELITE V2 | ASUS TUF GAMING B550-PLUS | Engineering Function & Impact |
|---|---|---|---|
| **Memory Overclocking** | `Tweaker` $\rightarrow$ `Extreme Memory Profile (X.M.P.)` | `Ai Tweaker` $\rightarrow$ `Ai Overclock Tuner` $\rightarrow$ **`D.O.C.P.`** | Loads rated 3200 MT/s SPD profiles & 1.35V DRAM voltage. |
| **Infinity Fabric Clock** | `Tweaker` $\rightarrow$ `FCLK Frequency` | `Ai Tweaker` $\rightarrow$ **`FCLK Frequency`** | Keeps AMD Infinity Fabric synchronous 1:1 ($FCLK = 1600\,\text{MHz}$). |
| **Gear Down Mode (GDM)** | `Tweaker` $\rightarrow$ `Advanced Memory` $\rightarrow$ `Gear Down Mode` | `Ai Tweaker` $\rightarrow$ `DRAM Timing Control` $\rightarrow$ **`Gear Down Mode`** | Stabilizes Dual-Rank (2R) DDR4 memory modules. |
| **Re-Size BAR Quick-Key**| None (Menu only) | **`[F4] Re-Size BAR`** (Top Toolbar) | One-touch toggle for Above 4G Decoding and ReBAR. |
| **Above 4G Decoding** | `Settings` $\rightarrow$ `Above 4G Decoding` | `Advanced` $\rightarrow$ `PCI Subsystem Settings` $\rightarrow$ **`Above 4G Decoding`** | Allocates 64-bit MMIO space above 4GB. |
| **Re-Size BAR Support** | `Settings` $\rightarrow$ `Re-Size BAR Support` | `Advanced` $\rightarrow$ `PCI Subsystem Settings` $\rightarrow$ **`Re-Size BAR Support`** | Grants CPU full aperture access to GPU VRAM. |
| **CPU Boost (PB2)** | `Tweaker` $\rightarrow$ `Core Performance Boost` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common Options` $\rightarrow$ **`Core Performance Boost`** | Unlocks 3.7 GHz base clock cap up to 4.65 GHz boost. |
| **C6 Sleep Anti-Freeze** | `Tweaker` $\rightarrow$ `Power Supply Idle Control` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common Options` $\rightarrow$ **`Power Supply Idle Control`** | Set to `Typical Current Idle` to eliminate Linux C6 freezes. |
| **Firmware Dropper** | `Settings` $\rightarrow$ `APP Center Download & Install` | `Tool` $\rightarrow$ **`ASUS Armoury Crate`** | Suppresses ACPI WPBT table and unwanted software injection. |
| **Linux CPPC Scaling** | `Tweaker` $\rightarrow$ `CPPC` / `CPPC Preferred Cores` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `NBIO Common Options` $\rightarrow$ `SMU` $\rightarrow$ **`CPPC`** | Enables `amd-pstate-epp` autonomous kernel frequency scaling. |
| **Hardware IOMMU** | `Settings` $\rightarrow$ `AMD IOMMU` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `NBIO Common Options` $\rightarrow$ **`IOMMU`** | Enables native ACPI IVRS table; eliminates `iommu=soft`. |
| **CSM Compatibility** | `Boot` $\rightarrow$ `CSM Support` | `Boot` $\rightarrow$ `CSM (Compatibility Support Module)` $\rightarrow$ **`Launch CSM`** | Must be `Disabled` for pure UEFI GOP. |
| **Fast Boot** | `Boot` $\rightarrow$ `Fast Boot` | `Boot` $\rightarrow$ **`Fast Boot`** | Must be `Disabled` under Linux for full AGESA memory training. |

---

## 3. Step-by-Step Configuration Walkthrough for ASUS B550-PLUS

1. **Enter UEFI Setup:**
   * Power on system, tap **`Del`** or **`F2`**.
   * If in EZ Mode, press **`F7`** to switch to **Advanced Mode**.

2. **D.O.C.P. (Memory) & Infinity Fabric:**
   * Navigate to **`Ai Tweaker`**.
   * `Ai Overclock Tuner` $\rightarrow$ Set to **`D.O.C.P.`** (Select Profile 1).
   * `FCLK Frequency` $\rightarrow$ Set to **`1600MHz`** (for DDR4-3200).
   * `DRAM Timing Control` $\rightarrow$ Verify **`Gear Down Mode = Enabled`**.

3. **Graphics & PCIe Addressing:**
   * Either press **`F4`** in top toolbar to enable Re-Size BAR, or:
   * Navigate to **`Advanced`** $\rightarrow$ **`PCI Subsystem Settings`**.
   * `Above 4G Decoding` $\rightarrow$ **`Enabled`**.
   * `Re-Size BAR Support` $\rightarrow$ **`Auto`**.

4. **CPU Boost, Power Supply & CPPC (Linux Optimization):**
   * Navigate to **`Advanced`** $\rightarrow$ **`AMD CBS`** $\rightarrow$ **`CPU Common Options`**.
     * `Core Performance Boost` $\rightarrow$ **`Auto`**.
     * `Global C-state Control` $\rightarrow$ **`Enabled`**.
     * `Power Supply Idle Control` $\rightarrow$ **`Typical Current Idle`**.
   * Navigate to **`Advanced`** $\rightarrow$ **`AMD CBS`** $\rightarrow$ **`NBIO Common Options`**.
     * `IOMMU` $\rightarrow$ **`Enabled`**.
     * `SMU Common Options` $\rightarrow$ `CPPC` $\rightarrow$ **`Enabled`**.
     * `SMU Common Options` $\rightarrow$ `CPPC Preferred Cores` $\rightarrow$ **`Enabled`**.

5. **Firmware Hygiene & Boot Cleanliness:**
   * Navigate to **`Tool`** $\rightarrow$ **`ASUS Armoury Crate`**.
     * `Download & Install ARMOURY CRATE app` $\rightarrow$ **`Disabled`**.
   * Navigate to **`Boot`**.
     * `Fast Boot` $\rightarrow$ **`Disabled`**.
     * `CSM (Compatibility Support Module)` $\rightarrow$ `Launch CSM` $\rightarrow$ **`Disabled`**.

6. **Save & Exit:**
   * Press **`F10`** $\rightarrow$ Review changed registers list $\rightarrow$ Select **`OK / Enter`**.
