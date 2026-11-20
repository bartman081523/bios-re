# Cross-Check: rea `inspect_uefi_firmware` ↔ UEFIExtract (NE alpha 73)

**Datum:** 2026-10-26 · **Images:** `images/B550AORUSELITEV212.{FIb,FH,FG}` (SHA-256-log: `findings/session-log.md`)
**Referenz-Tool:** `UEFIExtract NE alpha 73 (Nov 21 2025)` aus
`/run/media/julian/ML4/coreboot/coreboot/util/bios2gpio-amd/UEFIExtract` (vom bios2gpu-amd-Projekt gepflegt).
**Referenz-Output:** `cartography/reference/{fib,fh,fg}/{*.dump, *.report.txt, *.guids.csv}` (je ~84 MiB dump).
**rea-Output:** `cartography/{fib,fh,fg}.json` (~705 KiB je Image) + `.md`.

Beobachtungs-Korpus-Disziplin: nur untenstehende Fakten sind gemessen; Interpretationen sind markiert.

## 1. Volume-Offsets & Längen — deckungsgleich (9/9)

Vergleich je Image (FIb): rea `firmware_volumes` vs. UEFIExtract-`report.txt`-Volume-Zeilen.

| FV | rea (offset/length) | UEFIExtract | Übereinstimmung |
|---|---|---|---|
| Top FV @0x37000 | 0x37000 / 0x20000 | `0037000 0020000` | exakt |
| Top FV @0x92f000 (FVMAIN) | 0x92f000 / 0x510000 | `0092F000 00510000` | exakt |
| Top FV @0xe3f000 | 0xe3f000 / 0x1000 | `00E3F000 00001000` | exakt |
| Top FV @0xe40000 | 0xe40000 / 0x1C0000 | `00E40000 001C0000` | exakt |
| Depth-1 0x950110 | 0x1000 | `N/A 00001000` | Länge exakt |
| Depth-1 0x951160 | 0x17000 | `N/A 00017000` | Länge exakt |
| Depth-1 0x95b4c0 | 0x1e7000 | `N/A 001E7000` | Länge exakt |
| Depth-1 0xa0bf70 | 0x3e000 | `N/A 0003E000` | Länge exakt |
| Depth-1 0xa1eeb8 | 0xc93000 | `N/A 00C93000` | Länge exakt |

- UEFIExtract zeigt für abgeleitete (komprimierte Layer) Volumes `N/A`-Offsets, und die dort gezeigten
  "Offsets" sind **Größen** (Report-Quirk, z. B. `003C0000` beim Derived-FV = Größe). Verwechselt man das,
  sieht es "wie ein fehlendes FV bei 0x3C0000" aus.
- rea ehrlich markiert: Depth-1-Offsets liegen im **Dekompressionsraum**, sichtbar im `logical_path`
  (`…/section[n]/lzma/FV@…`); `parent_offset` verlinkt nach oben. Depth-1-Offsets wandern zwischen den
  Versionen leicht (FIb 0x95b4c0 ↔ FH 0x95b4c8 ↔ FG 0x95b4c8; 0xa1eeb8 ↔ 0xa1eea0 ↔ 0xa1ee98) — kompatible
  Header-Größenunterschiede, kein Strukturunterschied.
- **guids.csv ist über alle drei Images byte-identisch** (md5 `8aa6d15c…`) → der GUID-Satz ist
  strukturgebunden; die Differenzen FG↔FH↔FIb liegen in Daten-Bytes, siehe `findings/differential.md`.
- Ergänzung (2026-10-26, Modul-Ebene): Die UEFIExtract-Zeile „`00CDC000 00C93000 … 5C60F367-…`" nennt den
  **FvNameGuid** des DXE-Layer-FV — nicht die File-System-GUID (die bleibt `8c8ce578-…` in allen
  drei Versionen). Auflösung + Modulgranularität: `findings/differential.md` §4, `findings/module_diff.md`.

## 2. Derived-only-FV 44a2d731 — rea korrekt weggelassen

UEFIExtract zeigt unter der PSP-Region „BIOS binary" (`00E42000 001BE000`, Type 62) ein
`Image UEFI N/A 003C0020` mit `Volume FFSv2 N/A 003C0000 44A2D731-D551-4594-93B4-BD2B60351E0E`
(report.txt-Zeilen 491–496 und 3742–3746).

Messung:
- GUID 44a2d731 … **kommt im rohen 16-MiB-Image nicht vor** (Byte-Suche leer).
- Es liegt im dekodierten Inhalt des GUID-defined-Abschnitts `ce3233f5-2cd6-4d87-9152-4a238bb6d1c4`
  (FFS-File `3e3b6dc0-064d-4b01-9203-7836c9b498e7` @0xe41fd0, 0xf938d B) — komprimiert ≈1,02 MB,
  dekomprimiert ≈0x3C0020 B; Inhalt: `Raw`-Section (0x1C) + FVI-Section (0x3C0004) → FV 44a2d731 (0x3C0000)
  mit PEI-Modulen (RomLayoutPei 7EB7126D, PeiCore 52C05B14, CapsulePei C779F6D8, te-Images, UI/Version-Sections).
- rea behandelt dies als `unknown-guid` mit ehrlicher Limitation
  („…unknown definition GUID ce3233f5…; payload retained as section") und leerem `sub_volumes` — **das ist
  kein Bug, sondern Vertragsverhalten** (recognized-with-gap). Falsifizierung dieses Verständnisses wäre:
  ein FV, das rea hätte lesen können aber verschluckt hat — nicht gefunden.

## 3. Parser-Befund A: verborgenes FV @0x9300c0 (beide Tools lassen es durch)

Rohes `_FVH`-Scanning über das Image (16-Byte-Alignment) findet **6 Signatur-Hits**, d. h. FV-Basen:
`0x37000, 0x92f000, 0x9300c0, 0x950110, 0xe3f000, 0xe40000`.

- rea mappt 5 — das FV bei **0x9300c0** fehlt.
- Der FV liegt im **Data-Bereich** des Raw-FFS-Files `05CA020B-0FC1-11DC-9011-00173153EBA8`
  („AMI ROM hole", FFS-File @0x9300a8, length 0x20018) — sein 40-Byte-Zero-Vector + FFS2-GUID
  beginnen 0x18 nach dem FFS-Header.
- rea's Section-Parser liest dort eine „Section" und stoppt: `{offset: 0x9300c0, header_length: 4,
  length: 0, type_code: 0, type_name: "unknown", sha256: e3b0c442…855 (=SHA-256 leerer String),
  compression: {kind: none}, sub_volumes: []}` — der Zero-Vector wird als 4-Byte-Section-Header
  interpretiert und der Walk endet. **Bogus-Record + fehlender FV.**
- UEFIExtract überspringt es ebenfalls („File | Raw | AMI ROM hole", keine Kinder im dump).

**Nicht ein false positive** — Plausibilitätskette (Plan-Risikozeile), für alle drei Images identisch gemessen:

| Eigenschaft | Wert |
|---|---|
| Zero-Vector (16 B) | alles 0x00 ✓ |
| FS_GUID | `8c8ce578-8a3d-4f1c-9935-896185c32dd3` (FFS2) ✓ |
| FvLength | 0x20000 ✓ (≤ Restbereich) |
| HeaderLength | 0x48 ✓ |
| Header-Checksumme | **16-bit-Summe aller Header-Wörter = 0** (cs-Feld 0xea51) ✓ |
| `_FVH` @ +0x28 | ✓ |
| Erster FFS-Header @0x930108 | erased pad (GUID all-FF, Size 0x2c, State 0xf8) ✓ parset |
| Content | **26 684 non-FF-Bytes** im Body (131 000 B), Beispieldaten @0x930400 |
| Versionen | FG ✓, FH ✓, FIb ✓ — identischer cs/len/Content-Umfang |

Interpretation (E-Grad: gering): AMI „ROM hole"-Volume mit NV-/Vendor-Dateninhalt; Zweck unbestimmt —
in Phase 5 als Extraktionsziel nutzen, Vorher-Nachher-Byte-Vergleich der 26 KB-Daten über FG↔FH↔FIb steht aus.

**Verbesserungskandidat (Phase 4):** bounded `_FVH`-Discovery innerhalb **Raw-FFS-File-Daten**
(`FfsSections.ts`/`UefiImageScan.ts`): wenn ein „Section-Start"-Bytesatz (0-Vector) dem Kopf eines
plausiblen FV entspricht (Zero-Vector + FFS2/FFS3-GUID + gültige Header-Checksumme + blockmap-Terminator),
dann Sub-FV anlegen statt Bogus-Section; Budgets aus `UEFI_FIRMWARE_LIMITS`. Test-Fixture: das
0x9300c0-Muster (FFS-File mit eingebettetem FV, dessen Header mit Zero-Vector beginnt).

### §3-Resultat (K1 umgesetzt, 2026-10-26 — Parser-Fix in rea)

Umsetzung in `UefiImageScan.ts` (`walkSectionChain`, Option A ohne Schema-/Katalog-Änderung): RAW-FFS-
Body (typeCode 0x01) mit leerer oder nur-Bogus-Section-Kette (`declared_length < header_length`,
ausgelöst durch den FV-Zero-Vector) wird einmalig mit `scanVolumesInRegion(... /embedded)` nach
eingebetteten FVs geprüft — Zulassung bleibt vollständig bei der bestehenden Kette (Alignment,
FvLength-Plausibilität, Header-Checksumme, blockmap-Terminator, Budgets). Bestätigt → Volume-Record mit
`parent_offset` (flache Linkage, kein Schema-Feld am FFS-File) + limitations-Zeile; nicht bestätigt →
altes Verhalten unbekannter Framing-Bytes unverändert.

**Verifikation an FId (nach Fix, `scratches/k1_fid_after.md` + JSON):**

| Prüfgröße | Ergebnis |
|---|---|
| Volume-Anzahl | **10** (vorher 9) — 4 Top-Level + 6 Depth-1 |
| Neu: `…/FFS:05ca020b…/embedded/FV@0x9300c0` | offset 0x9300c0, length 0x20000, depth 1, parent 0x92f000, sha256 `c2dd2665eea1591e…` |
| FFS-File `05ca020b` | `type raw`, length 131096, **sections: []** — Bogus-Zero-Length-Record beseitigt |
| FV-Inhalt erstmals walkbar | 2 FFS-Files: pad `ffffffff` (44 B) + **freeform `7bb28b99` (26 767 B, 1 Section)** — deckungsgleich mit den 26 684 non-FF-Bytes aus §3 |
| Limitations | `Raw file body … reinterpreted: 1 embedded firmware volume(s) …` (A) |
| Tests | `UefiImageScan.test.ts` 10/10 (+2 neue: positives 0x9300c0-Muster, negatives „unframed body ohne bestätigtes FV bleibt unverändert"); uefi-Suite + Acceptance 43/43 |
| Coverage | bleibt `complete` |

Die unter Phase 3 erzeugten `cartography/*.json` sind Stand vor dem Fix (9 FVs) und werden nicht
überschrieben; der Nach-Fix-Report liegt in `scratches/k1_fid_after.md`.

## 4. Compression-Gap B: GUID `ce3233f5-…`

- In allen drei Images: FFS-File `3e3b6dc0` @0xe41fe8, Section 0xf9375/0xf93ca/0xf939d B (per Version),
  `data_offset 24`, `attributes 1` (PROCESSING_REQUIRED), `compression.kind: unknown-guid`.
- Payload-Struktur (empirisch, FIb): 20 Byte `0x00`, dann LZMA-alone-artiger Header
  (`5d 92 0f 00` + 8×`00`), dann komprimierte Daten. Hand-Dekodierung scheiterte:
  FORMAT_ALONE (size-Feld 0 → sofort EOL), FORMAT_RAW LZMA1 (dict 0x0f92→ungültig; erzwungene
  dict-Größen 0x1000…0x1000000 mit lc3/lp0/pb2: „Corrupt input data"). Wird von UEFIExtract dekodiert
  (s. o.). Es ist kein Standard-LZMA-custom (EE4E5898) und kein LZMAF86.
- **Kandidat für Phase 4:** Dekompressor identifizieren (UEFITool/UEFIExtract-Quelle oder ABI-Differenz),
  dann als Compression-GUID ergänzen — danach kann rea den PEI-FV 44a2d731 abbilden
  (heute: payload als Section erhalten, ehrlicher Gap).

### §4-Resultat (K2 umgesetzt, 2026-10-26 — Dekompressor identifiziert + Parser-Fix in rea)

- **Identifikation:** `ce3233f5-2cd6-4d87-9152-4a238bb6d1c4` = **EFI_GUIDED_SECTION_ZLIB_AMD**
  (UEFITool `common/ffs.h:451`; Begleiter `991efac0…` = ZLIB_AMD2). Das vermeintliche
  „LZMA-alone-artige" `5d 92 0f 00` war ein Irrtum der Roh-Interpretation: bei DataOffset 0x18 liegt
  der Stream erst hinter dem **EFI_AMD_ZLIB_SECTION_HEADER** (ffs.h:458): 256 B = 0×14 Null +
  `CompressedSize` u32 LE @0x14 + 0×E8 Null-Footer; ab Payload-Offset **0x100** folgt ein
  **zlib-wrapped** Stream (`78 da …`). Die `5d 92…`-Bytes im Feld sind Stream-Residual, kein Header.
- **Ground truth FId** (`scratches/k2_peifv.bin`-Erstellung + rea-Zeiger): Section @0xe41fe8,
  size 0xf94c0, CompressedSize 1 020 840 == Stream-Länge exakt; zlib-Decode (wbits=+15, UEFITool
  `inflateInit2(15U)`-Konvention) → 3 932 192 B (0x3C0020): RAW-Section (28 B, type 0x19) +
  FVI-Section (0x3c0004/0x17) + FV @0x20 (FvLength 0x3C0000, FS-GUID FFS2, Checksumme i. O.,
  ext-header @0x60); image-absolute FV-Angel: 0xe41fe8+0x18+0x20 = **0xe42020**.
- **rea-Fix** (L0, Tests 46/46): compression.kind `ami-zlib` (GUID-Tabelle + Schema-Enum),
  Scan-Lane `format: "lzma" | "zlib"` mit 0×100-Peel vor Dekodierung, Provider-Dekodierung synchron
  über node:zlib `inflateSync` (Budget = lzmaOutputBytes, Handler `node-zlib@<zlib>`), Extraktion
  labelt `.decoded.bin` als `decompressed-zlib`, ami-zlib läuft in den Dekodier-Pfad (statt Gap).
  Schema-Change → MCP-Katalog regeneriert.
- **Falsifikator erfüllt (A):** `inspect-uefi-firmware` auf FId meldet **11/11 Volumes**, inkl.
  `flash/FV@0xe40000/FFS:3e3b6dc0…/section[0]/zlib/FV@0xe42020` (0x3C0000, depth 1, parent
  0xe40000); Inhalt erstmals walkbar: freeform 1b45cc0a/5b85965c (a-priori-Art), **pei-core
  `52c05b14` (ui „P")** + PeiM-Inventar je depex/te/ui/version. `extract-uefi-firmware
  --file-offset 0xe41fd0` → `section-0xe41fe8.decoded.bin`, source `decompressed-zlib`,
  3 932 192 B, sha256 **d9a7e8dc… == Hand-Dekodier** (`k2_peifv.bin`), handler `node-zlib@1.3.2`,
  coverage complete, 0 Gaps. Rest: je 4 konservative `_FVH … not confirmed` false-positives im
  dekodierten Stream (Observation, kein Fehler).

## 5. Fazit (Evidenz-Grade)

| Befund | Grad | Quelle |
|---|---|---|
| FV-Offsets/Längen deckungsgleich (9/9) | **A** (zwei unabhängige Tools) | beide Tools |
| guids.csv identisch FG↔FH↔FIb | **A** | md5-Vergleich |
| 44a2d731 = derived-only | **A** | GUID-scan raw + report |
| FV @0x9300c0 checksum-korrekt & non-empty, identisch in 3 Images | **A** | roh-Scan + Prüfschritte |
| rea fehlt 0x9300c0 als FV (Bogus-Section-Record) | **A** | rea-JSON + report |
| K1-Fix: rea meldet FV@0x9300c0 (depth 1, 10/10 Volumes), Bogus-Record weg | **A** (Fixture + Real-Image) | `UefiImageScan.test.ts`, `k1_fid_after.md` |
| 0x9300c0-Inhalt erstmals gemappt: freeform `7bb28b99` 26 767 B, `ffffffff`-pad, sonst FF | **A** | rea-JSON nach Fix |
| Inhalt des 0x9300c0-FVs = NV-/Vendor-Daten | **E** (Spekulation, unbestätigt) | 26- KB-Bytes |
| K2: GUID `ce3233f5` = EFI_GUIDED_SECTION_ZLIB_AMD, 0×100-AMD-Header + zlib-Wrap | **A** (UEFITool-Quelle + Byte-Decode FId) | `ffs.h:451/458`, `k2_peifv.bin` |
| K2-Fix: rea meldet PEI-FV FV@0xe42020 (11/11 Volumes), PeiCore+PeiM walkbar | **A** (Fixture + Real-Image) | `UefiImageScan.test.ts`, `UefiAnalysisProvider.test.ts`, `k2_fid_after.json` |
| K2-Extraktion: `.decoded.bin` 3 932 192 B == Hand-Dekodier (sha256 d9a7e8dc…) | **A** (zwei unabhängige Wege) | `k2_extract.json` vs `k2_peifv.bin` |

## 6. Modul-Ebene (Phase-3-Verfeinerung, nachgelagert)

Dekodierte Layer je Version (`findings/module_diff.md`, `findings/module_inspect.md`; Scratches
`diff_modules.py`/`module_inspect.py`/`body_delta.py`): **518 gemeinsame Module je Paar (0 neu,
0 entfernt)**; Layer-Längen nur am DXE-Layer Δ (13 484 048 → 13 185 040 B dekodiert); identifizierte
Content-Änderungen: `aeb1671d` = Gigabyte-Download-Assistant-WPBT-EXE (−303 047 B komprimiert, FG↔FH
dekodiert identisch), `fbf95065` = Microsoft-Zertifikat-Bundle (+1 825), `76d5cf91` = OA3 (+1 504),
`deadbeef` = ACPI-SSDT `GBT/GSWApp` (+630, FG↔FH 2 Bytes), `414d94ad` = opaker 5A88641B-Blob
(~511/509 Bytes @0x158..0x467), `3fd1d3a2` = „$FID"-Release-Metadaten. Ableitungen:
`findings/differential.md` §4. UEFIExtract-Child-Offsets der Layer-Module (z. B. aeb1671d-PE32
0xDD55C/0x917EC, report-Zeilen 3708+) sind mit der GUID-Signatur-Methode kompatibel.

## 7. P-1/K6-D — RomLayout-Tabellen vs. reales Image (2026-10-27)

Zwei unabhängige Quellen, deckungsgleich (beide A):

1. **Dekompilierte Struktur** (SecSMIFlash 3370a4bd, Ghidra): 0x2cd8-Selektion `Flag & 0x200`,
   stride 0x18, Offset u32@+8/Size u32@+0xc/Flag u32@+0x14; Multi-Hash über Crypto-Protokoll;
   Gate 0x2024 benutzt dieselbe Tabellenform und den **Capsule-Wrap-Offset ±0x102c** — konsistent
   mit FV@0x9300d0 (= Loch-FV K1-Befund) und dem 4-KB-Vorraum-FV@0xe3f010.
2. **Roh-Image** (B550AORUSELITEV212.FId, python-peek): FV-Header @0x37010/0x92f010/0x9300d0/
   0xe3f010/0xe40010 in genau den Tabellen-Regionen; Non-FF-Zählung der Löcher: [0,0x37000) = 53 B
   @0x20000 (aa55aa55…), [0x77000,0x87000) = 0 B (komplett gelöscht), Loch-FV = 26 755 non-FF,
   [0xe3f000,0xe40000) = 135 B, PSP-Zone [0x90f200,0x92f000) = 113 859 non-FF (29 Pages,
   `_PT_`-Magic @0x90f000, 5f 50 54 5f + 0c c0 01 00) — **deckungsgleich** mit dem geparsten
   RomLayout: hash-gedeckte Bereiche tragen Code/Content, hash-freie Bereiche tragen PSP-/Vendor/
   leere Daten.

Keine Abweichung zwischen der gepackten 4112-B-Capsule-Struktur und dem 16-MB-Image-Befund;
Residual bleibt die Location der erwarteten Digests (tabellenlos in der RomLayout).