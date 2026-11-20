# WPBT Dropper & Execution Analysis (Bug K4)

**Datum:** 2026-11-19  
**Target:** `B550AORUSELITEV212.FId` (und Vergleich FG/FH/FIb)  
**Modules:**
- `WpbtDxe`: GUID `0996199f-2ce2-4d97-830b-077a7b28588a` (DXE Driver)
- `WPBT Payload`: GUID `aeb1671d-019c-4b3b-ba00-35a2e6280436` -> `section-0.payload.bin` (PE32+ Native Executable, PDB `nativeskel.pdb`, SHA-256 `7ed7e4dc3dcd5cd909e088a8309d5ec646d6bbaed3c67d651acf23ab552dc067`)

---

## 1. Overview & Chain of Execution

The Gigabyte WPBT mechanism injects executable code into Windows on every boot through the following verified stages:

```
+-----------------------------------------------------------------------------------------+
| UEFI Boot (DXE Phase)                                                                   |
| WpbtDxe (0996199f) registers gEfiEventReadyToBootGuid callback                         |
| Checks Setup Variable [0x264] ("APP Center Download & Install")                        |
|   -> If 0 (Disabled): Aborts with EFI_UNSUPPORTED (no WPBT ACPI table created)          |
|   -> If 1 (Enabled / Default): Builds ACPI WPBT table pointing to embedded PE payload   |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Windows Boot (Kernel Phase)                                                             |
| Windows Kernel reads ACPI WPBT table                                                    |
| Copies payload from physical memory to disk (%TEMP% / system buffer)                    |
| Executes payload as a Native / System process                                           |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Payload Execution (Entry: 0x140001580)                                                  |
| 1. Checks command line / environment                                                    |
| 2. Extracts embedded PE binary from resource section                                    |
| 3. Writes binary to \SystemRoot\System32\GigabyteUpdateService.exe                      |
| 4. Invokes FUN_140001300 to configure Windows Registry Service                          |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Service Registry Configuration (FUN_140001300)                                          |
| Key: \Registry\Machine\System\CurrentControlSet\Services\GigabyteUpdateService          |
|   - DisplayName   = "GIGABYTE Update Service"                                           |
|   - ObjectName    = "LocalSystem"                                                       |
|   - ErrorControl  = 0x00000001 (SERVICE_ERROR_NORMAL)                                   |
|   - Start         = 0x00000002 (SERVICE_AUTO_START)                                     |
|   - Type          = 0x00000010 (SERVICE_WIN32_OWN_PROCESS)                              |
|   - ImagePath     = "\SystemRoot\System32\GigabyteUpdateService.exe"                    |
|   - Handshake     = 0x00000001                                                          |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Windows SCM Launch                                                                      |
| Service Control Manager launches GigabyteUpdateService.exe under LocalSystem privileges |
| Executes network updates / telemetry / software installs                                |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Decompiled Source Code (Ghidra via REA)

### 2.1 Service Installer (`FUN_140001300`)

```c
ulonglong FUN_140001300(undefined8 param_1, undefined8 param_2, undefined4 param_3,
                       undefined8 param_4, longlong param_5)
{
  longlong lVar1;
  ulonglong uVar2;
  longlong lVar3;
  undefined4 local_res18 [2];
  undefined8 local_res20;
  undefined1 local_58 [16];
  undefined1 local_48 [16];
  undefined4 local_38 [2];
  undefined8 local_30;
  undefined1 *local_28;
  undefined4 local_20;
  undefined8 local_18;
  undefined8 uStack_10;
  
  local_res18[0] = param_3;
  local_res20 = param_4;
  RtlInitUnicodeString(local_48, L"\\Registry\\Machine\\System\\CurrentControlSet\\Services\\GigabyteUpdateService");
  RtlInitUnicodeString(local_58, L"\\Registry\\Machine\\System\\CurrentControlSet\\Services\\GigabyteUpdateService");
  
  local_38[0] = 0x30;
  local_28 = local_48;
  local_30 = 0;
  local_20 = 0x240;
  local_18 = 0;
  uStack_10 = 0;
  
  // Create or open the service key in registry
  uVar2 = NtCreateKey(&local_res20, 0xf003f, local_38, 0, 0, 1, 0);
  if (-1 < (int)uVar2) {
    RtlInitUnicodeString(local_58, L"DisplayName");
    NtSetValueKey(local_res20, local_58, 0, 1, L"GIGABYTE Update Service", 0x30);
    
    RtlInitUnicodeString(local_58, L"ObjectName");
    NtSetValueKey(local_res20, local_58, 0, 1, L"LocalSystem", 0x18);
    
    local_res18[0] = 1;
    RtlInitUnicodeString(local_58, L"ErrorControl");
    NtSetValueKey(local_res20, local_58, 0, 4, local_res18, 4);
    
    // Start = 2 (SERVICE_AUTO_START)
    local_res18[0] = 2;
    RtlInitUnicodeString(local_58, L"Start");
    NtSetValueKey(local_res20, local_58, 0, 4, local_res18, 4);
    
    // Type = 0x10 (SERVICE_WIN32_OWN_PROCESS)
    local_res18[0] = 0x10;
    RtlInitUnicodeString(local_58, L"Type");
    NtSetValueKey(local_res20, local_58, 0, 4, local_res18, 4);
    
    // ImagePath = \SystemRoot\System32\GigabyteUpdateService.exe
    RtlInitUnicodeString(local_58, L"ImagePath");
    lVar3 = -1;
    do {
      lVar1 = lVar3 * 2;
      lVar3 = lVar3 + 1;
    } while (*(short *)(param_5 + 2 + lVar1) != 0);
    NtSetValueKey(local_res20, local_58, 0, 2, param_5, (int)lVar3 * 2 + 2);
    
    local_res18[0] = 1;
    RtlInitUnicodeString(local_58, L"Handshake");
    NtSetValueKey(local_res20, local_58, 0, 4, local_res18, 4);
    
    NtClose(local_res20);
    uVar2 = uVar2 & 0xffffffff;
  }
  return uVar2;
}
```

### 2.2 Dropper Entry Point (`0x140001580`)

```c
void entry(void)
{
  // ... Initializations & Native NT Environment Setup ...
  RtlInitUnicodeString(&uStr, L"\\SystemRoot\\System32\\GigabyteUpdateService.exe");
  InitializeObjectAttributes(&objAttr, &uStr, OBJ_CASE_INSENSITIVE, NULL, NULL);
  
  // Drops the embedded binary directly to System32
  status = NtCreateFile(&fileHandle, FILE_GENERIC_WRITE, &objAttr, &ioStatus, ...);
  if (NT_SUCCESS(status)) {
    NtWriteFile(fileHandle, NULL, NULL, NULL, &ioStatus, embeddedPayload, payloadSize, ...);
    NtClose(fileHandle);
  }
  
  // Registers persistent service in Registry
  FUN_140001300(..., L"\\SystemRoot\\System32\\GigabyteUpdateService.exe");
  
  NtTerminateProcess(NtCurrentProcess(), 0);
}
```

---

## 3. Mitigation & Remediation Strategy (Pyramid Levels)

1. **Level L0 (Zero Modification / Setup Toggle):**
   - In BIOS Setup (IFR Form `qid 0x019c`):
     - Name: `APP Center Download & Install`
     - Values: `0` = Disabled, `1` = Enabled (Default)
   - When set to `Disabled`, `WpbtDxe` reads `SetupData[0x264] == 0` and returns `EFI_UNSUPPORTED`.
   - **Result:** No WPBT ACPI table is published. Windows will never receive or execute the dropper.

2. **Level L1 (NVRAM Factory Default Patch):**
   - In `cef5b9a3` (StdDefaults NVRAM volume):
     - Offset `0x264` is changed from `0x01` to `0x00`.
   - **Result:** Default BIOS reset boots with WPBT disabled out-of-the-box.

3. **Level L3 (Module Elimination / Inactivation):**
   - Removing `aeb1671d` from FV or patching `WpbtDxe` entry to `mov eax, 0x80000003; ret`.
   - **Constraint:** Edits inside the DXE main volume (`FV@0x92f000`) fall within the K8 RSA-2048 Secure Flash hash scope, requiring an external SPI programmer or hardware ISP if flashed.
