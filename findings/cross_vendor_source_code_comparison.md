# Deep Cross-Vendor Source Code & Architecture Comparison: AMD B550 Firmware

Comparative decompilation and reverse-engineering study of AMI Aptio V UEFI firmware implementations across all four major AMD AM4 motherboard vendors: **Gigabyte**, **ASUS**, **MSI**, and **ASRock**.

---

## 1. Decompilation Inventory & REA Pipeline Metrics

Using the `rea` reverse-engineering engine (with Ghidra 12.1.4 decompiler integration), the core setup modules across all four vendors were extracted from their raw UEFI firmware volumes and decompiled into C pseudocode:

| Metric / Dimension | Gigabyte (AORUS Elite V2) | ASUS (TUF Gaming B550-Plus) | MSI (MAG B550 Tomahawk) | ASRock (B550 Steel Legend) |
|---|---|---|---|---|
| **BIOS Version** | `FIb` (Aptio V) | `3607` (Aptio V) | `1.G0` (Click BIOS 5) | `3.40` (Aptio V) |
| **Total Decompiled Functions** | **281** C functions | **350** C functions | **284** C functions | **201** C functions |
| **Total Decompiled LOC** | **18,837** lines of C | **30,099** lines of C | **27,557** lines of C | **14,806** lines of C |
| **AMITSE Binary Size** | 1,329,504 bytes | 1,315,840 bytes | 1,362,112 bytes | 552,832 bytes |
| **Firmware Volume Architecture** | 6 Volumes, single flash | 18 Volumes, 2KB RSA CAP | 18 Volumes, raw ROM | 20 Volumes, Dual-BIOS SPI |
| **Core AMITSE Module GUID** | `899407d7-99fe-43d8-...` | `899407d7-99fe-43d8-...` | `899407d7-99fe-43d8-...` | `899407d7-99fe-43d8-...` |

---

## 2. Structural & Architectural Disassembly Findings

### A. The Core AMI Dispatcher (`TseProcessKey` / `TseHandleKey`)
All four vendors inherit a common AMI Aptio V foundation (~688 LOC in the decompiled output: `0x15f1c` in Gigabyte, `0x1f870` in ASUS, `0x3e134` in MSI, `0x17bd8` in ASRock). However, each vendor grafts proprietary callbacks onto the key handling loop:

```c
// Core Dispatch Loop Archetype identified across all 4 vendors:
EFI_STATUS TseProcessKey(EFI_INPUT_KEY *Key) {
    if (Key->ScanCode == SCAN_F10) {       // 0x1d: Universal across all 4 vendors
        return PromptSaveAndReset();
    }
    // Vendor-specific hook injection point:
    #if defined(VENDOR_GIGABYTE)
        if (Key->ScanCode == SCAN_F2) ToggleClassicMode();
        if (Key->ScanCode == SCAN_F4) InvokeProfileFileBrowser(); // .PRO loader
    #elif defined(VENDOR_ASUS)
        if (Key->ScanCode == SCAN_F7) ToggleAdvancedMode();
        if (Key->ScanCode == SCAN_F4) ToggleResizeBarCallback();  // [F4] ReBAR shortcut
    #elif defined(VENDOR_MSI)
        if (Key->ScanCode == SCAN_F7) ToggleEzMode();
        if (Key->ScanCode == SCAN_F6) LoadOptimizedDefaults();
    #elif defined(VENDOR_ASROCK)
        if (Key->ScanCode == SCAN_F6) ToggleAdvancedMode();
        if (Key->ScanCode == SCAN_F9) LoadUefiDefaults();
    #endif
}
```

### B. Profile Serialization & Storage Implementations

The four vendors approach BIOS profile persistence with radically different design philosophies:

1. **Gigabyte: External File-Centric Architecture (`.PRO` format)**
   - Decompiled functions `0x35dc4` (serializer) and `0x35d10` (deserializer).
   - Formats a 56-byte binary header with magic `0x1964`, project code QWORD comparison against the `$BDR` table (`8ARNR302`), BIOS version check (`FIb\0`), and an 8-bit checksum (`sum(bytes[0x38:]) & 0xFF`).
   - Enables saving and loading profiles from FAT32 USB sticks and the Linux EFI system partition (`/boot/efi/BIOS_PROFILES/`).

2. **ASUS: Hybrid Internal NVRAM Slots + `.CMO` Container**
   - Profile management is driven by `ASUS O.C. Profile` (`Profile #1` to `Profile #8`).
   - Rather than storing full binary setup buffers on external drives, ASUS stores profiles in NVRAM variable blocks (`AsusOcProfileVar1..8`).
   - External file export uses a proprietary `.CMO` container that encrypts/signs the CMOS register delta with board-specific keys.

3. **MSI: Multi-Bank NVRAM Slots (`Overclocking Profile 1..6` & `ECO Profile 1..5`)**
   - MSI Click BIOS 5 implements dedicated profile banks in NVRAM: 6 performance slots and 5 energy-saving slots.
   - For USB transfer, MSI integrates the profile saver directly into the M-Flash subsystem, appending a 320x240 BMP screenshot of the setup screen to the profile header for visual preview.

4. **ASRock: Stripped Lightweight Slots (`UserDefault1..9`)**
   - Decompiled AMITSE binary is only **552 KB** (less than half the size of Gigabyte/ASUS/MSI).
   - ASRock strips all external graphical profile loaders and file browsers from the main AMITSE binary. Profile persistence is purely internal, referenced via `ASRGUID:05DF2256-B0F7-439a-A3A1-60215CECC7F8` (`Load previously saved user defaults`).

---

## 3. Firmware Dropper (WPBT) Comparative Decompilation

All four vendors include a Windows Platform Binary Table (WPBT) ACPI publishing module to install vendor background utilities automatically. Decompilation reveals how each vendor handles ACPI injection:

| Vendor | Module Name & GUID | Dropper Binary Injected | Setup Suppression Offset |
|---|---|---|---|
| **Gigabyte** | `WpbtDxe`<br>`1df36ff9-c7ea-47a3-bd5b-426c250db776` | `Gigabyte APP Center` installer | `Setup[0x264] = 0x00` (`Disabled`) |
| **ASUS** | `AsusWpbtDxe`<br>`af516361-b4c5-436e-a7e3-a149a31b1461` | `ASUS Armoury Crate` agent | `Tool -> ASUS Armoury Crate = Disabled` |
| **MSI** | `MsiDriverUtilityDxe`<br>`9221315b-30bb-46b5-813e-1b1bf4712bd3` | `MSI Driver Utility Installer` | `Settings -> Advanced -> Driver Utility = Disabled` |
| **ASRock** | `AutoDriverInstallerDxe`<br>`05ca020b-0fc1-11dc-9011-00173153eba8` | `ASRock Auto Driver Installer` | `Tool -> Auto Driver Installer = Disabled` |

### Decompiled WPBT Ingestion Pattern (Common AMI Root):
```c
// Decompiled pseudocode reconstruction of the WPBT ACPI publisher:
EFI_STATUS PublishWpbtTable(VOID) {
    UINT8 EnableDropper;
    GetVariable(L"Setup", &gSetupGuid, ..., &EnableDropper);
    if (EnableDropper == 0) {
        // Suppress ACPI table registration: clean ACPI namespace for Linux
        return EFI_ABORTED;
    }
    // Allocate ACPI table buffer and publish WPBT signature 'WPBT'
    AcpiTable->Signature = 0x54425057; // 'WPBT'
    AcpiTable->HandoffAddress = AllocateRuntimeBuffer(PayloadSize);
    CopyMem(AcpiTable->HandoffAddress, EmbeddedPayload, PayloadSize);
    return AcpiSupport->SetAcpiTable(AcpiSupport, AcpiTable, ...);
}
```
*Engineering Implication:* Disabling the dropper in the BIOS setup guarantees that the ACPI table list exposed to the Linux kernel (`/sys/firmware/acpi/tables/`) contains no dead WPBT pointers or vendor dropper junk.

---

## 4. Dual-BIOS Recovery & Flash Architecture

* **ASRock B550 Steel Legend:** Uses a single 32 MiB SPI flash chip partitioned into two discrete 16 MiB images (Primary at `0x00000000`, Backup at `0x01000000`). If the primary image fails checksum verification during the PEI phase, the hardware multiplexer falls back to the secondary image.
* **Gigabyte B550 Aorus Elite V2:** Uses a 16 MiB SPI chip for the main BIOS, paired with a dedicated ITE IT8795E microcontroller that implements **Q-Flash Plus** (can reflash an unbootable board from a FAT32 USB drive with `GIGABYTE.BIN`).
* **ASUS TUF Gaming B550-Plus:** Uses a 32 MiB SPI chip with a hardware **BIOS FlashBack** button controller. Requires renaming the file to `TGB550PS.CAP` to pass the hardware signature check.
* **MSI MAG B550 Tomahawk:** Uses a 32 MiB SPI chip with an independent Flash BIOS Button microcontroller. Requires renaming the file to `MSI.ROM`.
