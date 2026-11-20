# Reverse Engineering des AMI Aptio V / AMITSE BIOS-Profil-Formats

## 1. Übersicht & Zielsetzung

Ziel war es, das exakte binäre Speicher- und Ladeformat für BIOS-Profile (`.PRO`-Dateien) zu rekonstruieren, die von AMI Aptio V / AMITSE Firmware (insb. Gigabyte B550 / AM4) auf FAT32-Partitionen (wie der EFI-Systempartition `/boot/efi`) abgelegt und im BIOS-Setup über **F4** bzw. `Save & Exit` -> `Select File in HDD/FDD/USB` geladen werden.

Die Analyse erfolgte an der extrahierten AMITSE-Setup-Engine (`scratches/amitse.efi`, GUID `b1da0adf-4f77-4070-a88e-bffe1c60529a`).

---

## 2. Dekompilations-Ergebnisse der AMITSE-Routinen

### A. Validierungs-Routine (`0x36228` in `amitse.efi`)
Diese Funktion prüft jede Datei, die als Profil geladen werden soll:

```assembly
0000000000036228:
   36228: sub    $0x28,%rsp
   3622c: mov    $0x1964,%eax
   36231: mov    %rcx,%r9               ; %rcx = Zeiger auf gelesene Profil-Datei
   36234: cmp    %ax,(%rcx)             ; [Gate 1]: Magic an Offset 0x00 MUSS 0x1964 sein!
   36237: jne    0x362a5                ; Mismatch -> 0xc8 ("Invalid Profile")
   36239: cmpb   $0x38,0x5(%rcx)        ; [Gate 2]: Header-Größe an Offset 0x05 MUSS 0x38 (56 Bytes) sein!
   3623d: jne    0x362a5                ; Mismatch -> 0xc8 ("Invalid Profile")
   3623f: movslq %edx,%rcx              ; %edx = Dateigröße
   36242: lea    0x38(%r9),%r8          ; %r8 = Zeiger auf Payload (ab Offset 0x38)
   36246: mov    $0x0,%eax
   3624b: mov    %al,%dl                ; dl = Akkumulator = 0
   3624d: sub    $0x38,%rcx             ; rcx = Nutzlast-Länge
   36251: je     0x3625f
   36253: add    (%r8),%dl              ; [Gate 3]: 8-Bit-Akkumulations-Summe über gesamte Nutzlast
   36256: inc    %r8
   36259: sub    $0x1,%rcx
   3625d: jne    0x36253
   3625f: cmp    %dl,0x7(%r9)           ; Vergleiche berechnete Summe mit Byte an Offset 0x07!
   36263: je     0x3626c
   36265: mov    $0xc9,%ecx             ; Mismatch -> 0xc9 ("Wrong Checksum")
   3626a: jmp    0x362aa
   3626c: mov    $0xffe40028,%ecx
   36271: cmpl   $0x4856465f,(%rcx)     ; Prüft Firmware Volume Header ("_FVH")
   36277: jne    0x36283
   36279: lea    0x30(%rsp),%rcx
   3627e: call   0x35c7c                ; Liest Modell-ID (RAX) und BIOS-Version aus $BDR-Tabelle
   36283: cmp    %rax,0x10(%r9)         ; [Gate 4]: Modell-QWORD an Offset 0x10 prüfen!
   36287: je     0x36290
   36289: mov    $0xca,%ecx             ; Mismatch -> 0xca ("Wrong Model Name")
   3628e: jmp    0x362aa
   36290: mov    0x30(%rsp),%eax        ; EAX = Aktive BIOS-Version
   36294: mov    $0xb4,%ecx             ; 0xb4 = "Profile Loaded" (Erfolg)
   36299: cmp    %eax,0xc(%r9)          ; [Gate 5]: BIOS-Version-DWORD an Offset 0x0C prüfen!
   3629d: lea    0x17(%rcx),%edx        ; 0xb4 + 0x17 = 0xcb ("Different BIOS Version")
   362a0: cmove  %edx,%ecx              ; Bei Mismatch -> Warnung "Different BIOS version"
   362a3: jmp    0x362aa
   362a5: mov    $0xc8,%ecx             ; 0xc8 = "Invalid Profile"
   362aa: mov    %ecx,%eax              ; Rückgabe Statuscode
   362ac: add    $0x28,%rsp
   362b0: ret
```

---

### B. Modell- & BIOS-Versions-Ermittlung via `$BDR` (`0x35c7c`)

```assembly
0000000000035c7c:
   35c7c: movabs 0xffe40020,%rax
   35c86: mov    %rcx,%r8
   35c89: shr    $0x2,%rax
   35c8d: mov    $0xffe40000,%edx
35c9a: cmpl   $0x52444224,(%rdx)     ; Sucht Signatur "$BDR"
   35ca0: jne    0x35cad
   35ca7: cmp    $0x5aa5,0x8(%rdx)      ; Prüft Magic-Word 0x5aa5 an +0x08
   35cb3: mov    0x28(%rdx),%ecx        ; Offset +0x28 = BIOS-Versions-DWORD (z.B. "FIb\0")
   35cbb: mov    %ecx,(%r8)
   35cbe: mov    0x20(%rdx),%rax        ; Offset +0x20 = Modell-ID-QWORD (z.B. "8ARNR302")
   35cc2: ret
```

---

### C. Variablen-Zuweisung & Entpack-Routine (`0x35d10`)

```assembly
0000000000035d10:
   35d10: test   %ecx,%ecx              ; %ecx = Anzahl Records (aus Header +0x08)
   35d12: je     0x35d73
   35d23: mov    %rdx,%rbx              ; %rbx = Zeiger auf Payload (ab Offset 0x38)
   35d26: mov    %ecx,%edi              ; %edi = Record-Zähler
35d28: movzwl 0x4(%rbx),%eax         ; %eax = WORD Variablen-Größe (642 / 0x282 für Setup)
   35d2c: mov    (%rbx),%ecx            ; %ecx = DWORD Variablen-Index (0 für Setup)
   35d2e: mov    %eax,%esi
   35d30: shl    $0x4,%rcx              ; Index * 16 (Eintrag in Variablentabelle)
   35d34: add    $0x6,%rbx              ; %rbx überspringt 4 Byte Index + 2 Byte Größe -> Rohdaten!
   35d38: add    0x2d289(%rip),%rcx     ; Tabelle der registrierten NVRAM-Variablen
   35d3f: cmp    %rax,0x8(%rcx)         ; Prüft, ob Datengröße mit Sollgröße übereinstimmt (0x282)
   35d43: jne    0x35d5b                ; Bei Größenabweichung überspringen
   35d45: mov    (%rcx),%rcx            ; %rcx = Zielspeicher im NVRAM-Setup-Cache
   35d48: mov    %eax,%r8d              ; %r8d = 642 Bytes
   35d52: mov    %rbx,%rdx              ; %rdx = Quelldaten aus .PRO-Datei
   35d55: call   *0x160(%rax)           ; CopyMem(Ziel, Quelle, 642)
   35d5b: add    %rsi,%rbx              ; Weiterrücken um Datengröße
   35d5e: sub    $0x1,%rdi              ; Record-Zähler dekrementieren
   35d62: jne    0x35d28
   35d73: ret
```

---

## 3. Exakte Binärstruktur der `.PRO`-Datei

| Offset | Länge | Datentyp | Bezeichnung | Inhalt / Wert |
| :--- | :--- | :--- | :--- | :--- |
| **0x00** | 2 Bytes | UINT16 (LE) | Magic | `0x1964` (`64 19`) |
| **0x02** | 2 Bytes | UINT16 (LE) | Payload-Länge | `0x0288` (648 Bytes für Setup) |
| **0x04** | 1 Byte | UINT8 | Profil-Version | `0x11` |
| **0x05** | 1 Byte | UINT8 | Header-Größe | `0x38` (56 Bytes) |
| **0x06** | 1 Byte | UINT8 | Reserviert | `0x00` |
| **0x07** | 1 Byte | UINT8 | Checksumme | `sum(Payload[0x38:]) & 0xFF` |
| **0x08** | 4 Bytes | UINT32 (LE) | Record-Anzahl | `0x00000001` (1 Record für Setup) |
| **0x0C** | 4 Bytes | ASCII | BIOS-Version | `FIb\0` (`46 49 62 00`) |
| **0x10** | 8 Bytes | ASCII | Board-Modell-ID | `8ARNR302` (Gigabyte B550 Aorus Elite V2) |
| **0x18** | 32 Bytes | Nullbytes | Padding | `0x00` * 32 |
| **0x38** | 4 Bytes | UINT32 (LE) | Variable-Index | `0x00000000` (Index 0 = Setup) |
| **0x3C** | 2 Bytes | UINT16 (LE) | Variable-Größe | `0x0282` (642 Bytes) |
| **0x3E** | 642 Bytes | Bytes | Setup-Nutzlast | Vollständiges modifiziertes NVRAM-Setup |

Gesamtdateigröße: **704 Bytes** (`0x2C0`).

---

## 4. Bereitgestellte Profile

1. **`STABILITY.PRO`**:
   - XMP: Deaktiviert (JEDEC 2133 MT/s @ 1.20V)
   - Core Performance Boost: Auto
   - Above 4G Decoding: Enabled
   - Re-Size BAR: Disabled (Failsafe)
   - Power Supply Idle: Typical Current Idle (0x00, kein C6-Freeze)
   - WPBT: Disabled (keine Firmware-Injektion)
   - CPPC & Preferred Cores: Enabled
   - Gear Down Mode: Enabled
   - IOMMU: Enabled

2. **`BALANCED.PRO`**:
   - XMP: Profile 1 (DDR4-3200 MT/s @ 1.35V, 1:1 FCLK 1600 MHz)
   - Core Performance Boost: Auto (PB2 bis 4.65 GHz)
   - Above 4G Decoding: Enabled
   - Re-Size BAR: Auto / Enabled
   - Power Supply Idle: Typical Current Idle
   - WPBT: Disabled
   - CPPC & Preferred Cores: Enabled
   - Gear Down Mode: Enabled
   - IOMMU: Enabled

3. **`PERFORMANCE.PRO`**:
   - XMP: Profile 1 (DDR4-3200 MT/s @ 1.35V)
   - Core Performance Boost: Auto
   - Above 4G Decoding: Enabled
   - Re-Size BAR: Auto
   - CPPC & Preferred Cores: Enabled
   - Power Supply Idle: Typical Current Idle
   - WPBT: Disabled

---

## 5. Deployment auf FAT32 EFI-Partition

Die Profile können mit dem Skript `deploy_profiles_to_efi.sh` direkt auf die EFI-Systempartition geschrieben werden:
```bash
sudo ./deploy_profiles_to_efi.sh
```
Oder direkt über das Hauptwerkzeug:
```bash
sudo ./am4_advisor.py --export-profiles /boot/efi/BIOS_PROFILES
```

Nach dem Neustart ins BIOS (`F2` / `Del`) können die Profile mit **F4** direkt von der EFI-Partition geladen werden.
