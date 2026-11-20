# Emulations-/Test-Tooling für B550-AM4-BIOS-Mods (Recherche)

**Datum:** 2026-11-19 · **Ziel:** BIOS-Mods testen / Original-Firmware dynamisch untersuchen
**Ist-Stand lokal:** QEMU 11.1.3 (x86_64/i386) ✅ · OVMF (`/usr/share/edk2/x64/OVMF*.fd`) ✅ ·
binwalk ✅ · Ghidra 12.1.4 + rea ✅ · **Unicorn/Qiling/PSPEmu/capstone/utk: nicht installiert**.

## Kernaussage

Ein *vollständiges* B550-Vendor-BIOS in generischem QEMU zu booten ist **nicht praktikabel**:
die Firmware hängt an AMD-PSP/AGESA/FCH/SMU-Init und Chipset-spezifischer Hardware. Es gibt
aber drei etablierte, komplementäre Emulations-Ebenen — je nach Frage:

| Ebene | Projekt (GitHub) | Was es kann | Aufwand |
|---|---|---|---|
| **Modul** (PEIM/DXE) | **Qiling** (UEFI-OS-Modul) · **gdbinit/efi_dxe_emulator** (Unicorn) | lädt ein einzelnes PE32 (z. B. `SmBusPei`), stubbte Boot-/Runtime-Services + Protokolle, Debugger | niedrig–mittel |
| **Firmware-Boot-Kette** (AMD) | **PSPReverse/PSPEmu** | emuliert die AMD-PSP (ARM), führt On-/Off-Chip-Bootloader + SecureOS + AGESA aus der echten Vendor-Image; GDB-Stub, DrCov, Proxy-Modus auf Real-HW; Zen/Zen+/Zen2 (partiell) | hoch (Submodule capstone/unicorn/libgdbstub) |
| **UEFI-Referenz** | **QEMU + OVMF** (`tianocore/edk2`, EmulatorPkg) | Standard-UEFI-Umgebung zum Booten/Testen eigener/gepatchter UEFI-Module; EmulatorPkg läuft als Linux-Userspace-Prozess | niedrig (lokal da) |
| **ROM-Edit-Pipeline** | **LinuxBoot UTK / fiano** | FV/FFS parsen, PE32 ersetzen, Image schreiben (vor QEMU-Test) | niedrig |

Verwandt/optional: **AMI Aptio Community Edition + AMD openSIL** (Genoa/EPYC, nicht AM4);
**CHIPSEC** (Firmware-Security-Tests, teils QEMU).

## Empfohlene Reihenfolge für dieses Projekt

1. **Qiling-UEFI auf einem extrahierten PEIM** (z. B. `SmBusPei` PE32-i386 aus
   `scratches/p4_SmBusPei_FId_o139.pe.bin`) — billigster Einstieg, beweist den
   Modul-Ausführungspfad und erlaubt das FId-Timing-Verhalten (TSC-Delay) dynamisch zu sehen.
   `pip install qiling` (zieht Unicorn/Capstone).
2. **QEMU + OVMF** als Harness für *gepatchte* Module: PE32 in eine OVMF-FV einbetten bzw.
   als DXE-Driver in einem OVMF-Build dispatchen, Boot bis UEFI-Shell prüfen.
3. **PSPEmu** nur bei Bedarf für die AGESA/PSP-/Secure-Boot-Ebene (K5/K8/K9/K10-Kontext);
   Build über die Submodule (`capstone`, `unicorn`, `libgdbstub`).
4. **UTK/fiano** in die Edit-Pipeline aufnehmen (statt eigener Python-Carver) — optional,
   da `p4_te2pe.py`/rea-uefi das FV/FFS/PE-Handling bereits abdecken.

## Konsequenz / Nicht-Ziele

- Kein QEMU-Fork nötig; die vorhandenen Projekte decken Modul- und PSP-Ebene ab.
- Voll-BIOS-Boot bleibt Real-HW/QFlash (siehe K8–K10: Secure-Flash-Hash-Scope,
  Anti-Rollback-Floor 9.04) — Emulation ersetzt **kein** Hardware-Flash-Ritual.
- Nächster konkreter Schritt: Qiling installieren, `SmBusPei_FId_o139.pe.bin` laden,
  fehlende PPI/BS-Stubs protokollieren (das zeigt, welche Services der PEIM real braucht).

## Update 2 — verifizierter Stand (2026-11-19, A)

| Test | Ergebnis |
|---|---|
| QEMU 11.1.3 + OVMF 4 MB (`-bios /usr/share/edk2/x64/OVMF.4m.fd`) | bootet bis `BdsDxe: No bootable option` ✅ |
| B550 `FId` (16 MiB) als `-bios` | **kein Output / Timeout** — nicht QEMU-bootfähig (PSP/AGESA/Flash-Layout) ❌ |
| Qiling 1.4.6 UEFI (`QL_OS.UEFI`) | 64-bit-only → für PE32-PEIMs unbrauchbar (siehe `peim_dynamic_exec.md`) |
| Unicorn-PEIM-Harness | läuft (FId + FIb, SMBus-`Execute` → `EFI_SUCCESS`); Repo `bartman081523/uefi-peim-harness` |
| OVMF `-pflash` (CODE+VARS) + `-drive file=fat:rw:<esp>` mit `EFI/BOOT/BOOTX64.EFI` | BDS lädt `Boot0002` (QEMU HARDDISK) und startet die UEFI-App ✅ |

**Konsequenz für „gepatchte Module testen":**
- **DXE/App-Ebene:** funktioniert heute ohne edk2-Build — `.efi` auf die FAT-ESP legen
  (`systemd-bootx64.efi`, SYSLINUX, eigener Treiber) und in OVMF booten/laden.
- **PEIM-Ebene (SmBusPei):** braucht einen OVMF-Build mit dem PEIM in der `PEIFV`
  (edk2-Source + BaseTools fehlen lokal; nur `iasl`/`nasm`/`python3` vorhanden).
- **Voll-BIOS:** bleibt Real-HW/QFlash; QEMU ersetzt das nicht.

**Nächster sinnvoller Schritt:** edk2 klonen und OVMF (OvmfPkgX64) bauen, den gepatchten
`SmBusPei` in die PEIFV legen, mit `-pflash -s -S` + OVMF-Debug-Log booten. Alternativ
zuerst einen DXE-Treiber über die FAT-ESP testen (Pipeline ist bereits belegt).

## Update 3 — EDK2 OVMF Build & SmBusPei PEIFV-Injektion verifiziert (2026-11-19, A)

In `/run/media/julian/ML6/edk2` wurde der vollständige EDK2-Build (`tianocore/edk2`) für `OvmfPkgIa32X64.dsc` (IA32 PEI + X64 DXE) aufgesetzt:

1. **Infrastruktur & BaseTools:**
   - BaseTools fehlerfrei kompiliert (`make -C BaseTools -j$(nproc)`), alle 328 Unittests grün.
   - Toolchain: `GCC` (nicht veraltetes `GCC5`).

2. **Injektion in `PEIFV`:**
   - In `OvmfPkg/OvmfPkgIa32X64.fdf` wurde die fehlende Build-Regel `[Rule.Common.PEIM.BINARY]` ergänzt.
   - Modul `OvmfPkg/SmBusPei/SmBusPei.inf` deklariert die prebuilt Binary `SmBusPei.efi` (5664 Bytes aus B550 FId) mit Bytecode-Depex `TRUE` (`0x06 0x08`).
   - In `PEIFV.Fv.map` erfolgreich auf Adresse `0x0000854eb0`, EntryPoint `0x0000855170` (RVA `+0x2c0`) gemappt.

3. **Empirischer Trace in QEMU (debugcon 0x402):**
   - `PeiCore` lädt und dispatchet `SmBusPei` (GUID `0AF9B07A-F8BD-1040-A434-4329FB61330D`) bei `0x1FBCE000` (EntryPoint `0x1FBCE2C0`).
   - **UEFI-PI-Standard-Konformität bewiesen:** Entgegen früheren Vermutungen nutzt AMI eine 100% standardkonforme 32-bit `EFI_PEI_SERVICES`-Tabelle (Header 24 B, `0x18` = `InstallPpi`, `0x20` = `LocatePpi`, `0x24` = `NotifyPpi`, `0x4c` = `AllocatePool`).
   - **DEPEX-Auflösung:** Der PEIM ruft am Entry `LocatePpi` für AMD Fabric GUID `1F4C6F90-B06B-48D8-A201-BAE5F1CD7D56`. Fehlt dieses PPI, beendet sich das Modul vorzeitig mit `EFI_NOT_FOUND`.
   - **Vollständige Modulausführung:** Durch Bereitstellung eines minimalen Stub-Deskriptors für `1F4C6F90` in `PlatformPei` durchläuft `SmBusPei` seine Initialisierung vollständig:
     - Registriert 4× Notify auf `gEfiEndOfPeiSignalPpiGuid` (`605EA650-C65C-42E1-BA80-91A52AB618C6`).
     - Installiert 2× `gEfiPeiSmbus2PpiGuid` (`9CA93627-B65B-4324-A202-C0B461764543`) für Controller-Ports `0x0B00` und `0x0B20`.
     - Installiert 2× AMI-SmBus-PPI (`ABD42895-78CF-4872-8444-1B5C180BFBDA`).
     - Kehrt sauber mit `EFI_SUCCESS` an `PeiCore` zurück.
   - `PeiCore` setzt den Boot fort (`DxeIpl.efi` -> DXE -> BDS). QEMU läuft ohne Fehler durch.
