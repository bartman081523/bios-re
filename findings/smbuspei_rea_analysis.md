# SmBusPei Reverse Engineering & Decompilation Report

**Datum:** 2026-11-19  
**Target:** `B550AORUSELITEV212.FId` (FFS `0af9b07a-f8bd-1040-a434-4329fb61330d`, PEIM)  
**Toolchain:** `rea` (commit `d0b661eab` / PR #12342 merged) + Ghidra 12.1.4_PUBLIC (JDK 27)  

---

## 1. Summary of Verification

Both **dynamic execution in QEMU (Option A emulation)** and **static decompilation via REA/Ghidra** have converged on the identical behavior:

1. **UEFI PI Standard Compliance:**
   - 32-bit PEIM utilizing standard `EFI_PEI_SERVICES` dispatch table:
     - `table + 0x4c`: `AllocatePool`
     - `table + 0x20`: `LocatePpi`
     - `table + 0x24`: `NotifyPpi`
     - `table + 0x18`: `InstallPpi`

2. **AMD Fabric Dependency:**
   - `LocatePpi` targets GUID `1f4c6f90-b06b-48d8-a201-bae5f1cd7d56` (`0x9dee230`).
   - If not found, execution exits cleanly without error (`EFI_SUCCESS` / zero return).
   - Once stubbed, complete initialization proceeds.

3. **FCH SMBus MMIO & Port Initialization:**
   - FCH MMIO register configuration via `_FchMmioInit` (`0xb19`):
     - `MMIO 0xFED80300 |= 0x10;`
     - `MMIO 0xFED80302 |= 0x01;`
     - `MMIO 0xFED80304 |= 0x02;`
   - Instantiates Controller 0 at I/O Port `0x0B00`.
   - Instantiates Controller 1 at I/O Port `0x0B20`.

4. **PPI Installations & Notifiers:**
   - 4× EndOfPei notifiers (`gEfiEndOfPeiSignalPpiGuid` `605EA650-E6D9-4FE1-BA41-F030666E74A6`)
   - 2× `gEfiPeiSmbus2PpiGuid` (`9CA93627-B65B-4339-A149-77F1DB2D792`)
   - 2× `gAmiPeiSmbusPpiGuid` (`ABD42895-B32E-49C3-8902-60281F87B114`)

---

## 2. Decompiled C Source (`rea decompile`)

### 2.1 Entry Point (`_EntryPoint`)

```c
void _EntryPoint(EFI_PEI_FILE_HANDLE FileHandle, const EFI_PEI_SERVICES **PeiServices)
{
  EFI_STATUS Status;
  void *Pool1;
  void *Pool2;
  
  // Allocate SMBus controller descriptor 1 (Port 0xB00)
  Status = (*PeiServices)->AllocatePool(PeiServices, 0x58, &Pool1);
  if (Status < 0) return;
  Status = (*PeiServices)->AllocatePool(PeiServices, 0xA0, (UINT8 *)Pool1 + 0x3C);
  if (Status < 0) return;

  // Initialize VTable & PpiList structures
  // Set I/O Base Port to 0x0B00
  *(UINT16 *)((UINT8 *)Pool1 + 0x28) = 0x0B00;
  
  // Query AMD Fabric PPI (1f4c6f90-b06b-48d8-a201-bae5f1cd7d56)
  Status = (*PeiServices)->LocatePpi(PeiServices, &gAmdFabricPpiGuid, 0, NULL, (void **)((UINT8 *)Pool1 + 0x20));
  if (Status >= 0) {
    // Configure FCH MMIO
    _FchMmioInit();
    
    // Register EndOfPei Notifier
    Status = (*PeiServices)->NotifyPpi(PeiServices, (EFI_PEI_NOTIFY_DESCRIPTOR *)((UINT8 *)Pool1 + 0x40));
    
    // Install gEfiPeiSmbus2PpiGuid
    if (Status >= 0) {
      Status = (*PeiServices)->InstallPpi(PeiServices, (EFI_PEI_PPI_DESCRIPTOR *)((UINT8 *)Pool1 + 0x4C));
      
      // Repeat sequence for Controller 2 (Port 0x0B20)
      // Repeat sequence for AMI Proprietary SMBus PPI instances
    }
  }
}
```

### 2.2 FCH MMIO Initialization (`_FchMmioInit`)

```c
void _FchMmioInit(void)
{
  // Enable FCH PMIO / SMBus decoding
  *(volatile UINT8 *)0xFED80304 |= 0x02;
  *(volatile UINT8 *)0xFED80302 |= 0x01;
  *(volatile UINT8 *)0xFED80300 |= 0x10;
}
```
