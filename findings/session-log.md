# session-log — bios-re Beobachtungs-Korpus

Disziplin (Mind `observation_corpus`): Rohdaten ungefiltert, Interpretation nur in Annotationsschicht.

---

## 2026-10-26 — Initial-Scan B550AORUSELITEV212.FIb (d6ce0901), roh

- 16 MiB; Bytes 0..0x1FFFF sind 0xFF (Erased-Region am Kopf).
- 0x20000: `AA 55 AA 55` … `00 00 00 00 00 70 0E 00 … 24 FF 00 F0 3A FF` (unbedeutend-interpretiert:
  Kandidat für PSP-Struktur — nicht benannt).
- `_FVH`-Treffer (6): 0x37028, 0x92f028, 0x9300e8, 0x950138, 0xe3f028, 0xe40028
  → FV-Header-Basen = Hit − 0x18 (Signatur liegt bei FvHeader-Offset 40).
- FV-FileSystemGuid alle `8c8ce578-8a3d-4f1c-9935-896185c32dd3` (FFS2).
- `PSPD`-ASCII-Treffer: 0x615834, 0x615888, 0x795834, 0x795888 — Kontext: `PSPDirectorySearch()::Entry-Type…`
  ASCII-String + Code; keine `$_PSPP`-Magics.
- FV-Header-Dekodierung (Beispiel 0x37010): FvLength=0x00020000, `_FVH`, Attr `FF FE 04 00`,
  HeaderLength 0x48, ExtHeaderOffset 0x60, Revision 0x02 — konsistent mit UEFI PI Spec.

<!-- Interpretationsschicht: FIb enthält 6 FVs, davon das größte (0x92f010, 0x00510000) vermutlich FVMAIN. -->

---

## 2026-10-26 — Phase 3: Kartografie, Cross-Check, Differential (alle drei Images)

**roh (rea):** `inspect-uefi-firmware` auf FIb/FH/FG je ~705 KiB Evidence → `cartography/{fib,fh,fg}.json`
(+ generierte Tabellen-MDs). Je Image: 9 FVs (4 Top-Level + 5 Depth-1 im Dekompressionsraum), 23 Depth-0-FFS,
8 unknown_regions (alles `erased-ff`), integrity leer, `entry_basis amd-psp-first`, `coverage complete`,
`$PSP`-Tabelle @0x60f000 (61 Einträge, alle `declared-unverified`), 10 `psp_candidates`.

**UEFIExtract NE alpha 73 (Referenz):** dump/report/guids.csv je Version →
`cartography/reference/{fib,fh,fg}/`.

**Befunde (Details/Beweis: `findings/crosscheck.md`):**
1. FV-Offsets/Längen rea == UEFIExtract, 9/9; Depth-1-Offsets = Dekompressionsraum (UEFIExtract: `N/A`+Größe).
2. Derived-only-FV `44a2d731` (im dekodierten `ce3233f5`-Layer, GUID nicht im rohen Image) — rea korrekt weggelassen.
3. **Parser-Befund A:** FV @0x9300c0 (im AMI-ROM-Hole-Raw-File `05ca020b` @0x9300a8) wird von rea als Bogus
   Zero-Length-Section (`type 0, length 0`, sha256 = leerer String) gelesen, nicht als FV erkannt; UEFIExtract
   überspringt es ebenfalls. Checksumme gültig (16-bit-Summe 0, cs 0xea51), 26 684 non-FF-Bytes, in allen
   drei Images identisch. Extract-Versuch des Files publiziert 0 Dateien.
4. **Compression-Gap B:** GUID `ce3233f5-2cd6-4d87-9152-4a238bb6d1c4` (Payload: 20×`00` + LZMA-alone-
   artiger Header `5d 92 0f 00` + 8×`00`); Hand-Dekodierung fehlschlagend (FORMAT_ALONE size=0, RAW
   LZMA1 lc3/lp0/pb2 mit dict-Erzwungung 0x1000…0x1000000: „Corrupt input data"). UEFIExtract dekodiert
   es (≈0x3C0020 → PEI-FV mit RomLayoutPei/PeiCore/CapsulePei).

**Extraktion (FIb, `extracted/` + `extracted/MANIFEST.sha256`):**
- `extract-uefi-firmware --volume-offset 0x92f000` → 14 Dateien (u. a. 4 dekodierte LZMA-Layer:
  0xa1ee90 13 185 040 B = DXE-Layer von 9e21fd93; 0x95b498 1 994 768 B; 0xa0bf48 253 968 B; 0x951138 94 224 B);
  2 pad-file-Gaps (0x92f048, 0x9500c0 — als `extraction_gaps` geführt).
- `--volume-offset 0xe40000` → 8 Dateien + 3 Gaps; `3e3b6dc0` wird als `compressed-passthrough` (1 020 765 B
  ab 0xe42000) publiziert + `unknown-guid-handler`-Gap.
- `--file-offset 0x9300a8` (ROM hole) → **0 Dateien** (Bogus-Section-Folge; Inhalt bleibt Phase-5-Extraktionsziel
  nach Parser-Fix).

**Differential (`findings/differential.md`, via `scratches/diff_b550.py`):**
- Depth-0-Struktur stabil: 23 Files identischer GUID-Reihenfolge über FG/FH/FIb; Größenänderungen nur an
  5 FVI-Files. `9e21fd93`: 4 219 057 (FG) → 4 218 909 (FH) → 3 913 887 B (FIb) — **−305 kB** am komprimierten
  Main-Layer in FIb.
- Roh-Byte-Diff: FG↔FH 27 ranges/5,3 MB, FG↔FIb 96/6,3 MB, FH↔FIb 93/6,1 MB. ~98 % davon sind
  komprimierte Layer (Kaskadeneffekt); ~264 kB außerhalb der gemappten Volumes ändern sich nur FG/FH↔FIb
  (PSP-Dateibereich/Mikrocode, 0x57000–0x92f000 + PSP-Tabellenbereich).
- Konstant geänderte kleine Inhalte (exakt gezählt, nicht Hull): `cef5b9a3` (FV@37000, Setup-Defaults-
  Blob: **415 geänderte Bytes FG→FH, identisch FG→FIb; 0 FH→FIb**), `414d94ad` (FV@92f000, komprimiert,
  511 B FG→FH), Version-Block im Payload `56e14f88` (**3–5 B pro Version** @0xe404ed–0xf3; Strings
  `8ARNR302{FG,FH,FIb}` + „B550 AORUS ELITE V2", „ALASKA AM I"). `0dca793a` ändert sich nicht (nur
  Coalesce-Hull-Artefakt in der Diff-Tabelle).
- Phase-4-Anker vorvermerkt: Setup-Default-Werte (cef5b9a3), Version-Block (56e14f88), PSP-Bereichs-
  Updates FG→FIb, plus die beiden Parser-/Dekoder-Kandidaten (0x9300c0-FV-Discovery, `ce3233f5`).

---

## 2026-10-26 — Phase 3 Rest: Modul-Ebene aus dekodierten Layern

**Scratches:** `diff_modules.py` → `findings/module_diff.md` · `module_inspect.py` →
`findings/module_inspect.md` · `body_delta.py` (dekodierte Body-Shas/Byte-Positionen).

**roh (Join depth + parent_offset + FFS-GUID + Ordinal):**
- 518 gemeinsame Module je Paar; 0 neu, 0 entfernt; FFS-sha geändert FG↔FH 97 · FG↔FIb 122 · FH↔FIb 55.
- Depth-1-Layer-Tabelle: nur der DXE-Layer ändert Länge (13 484 032 → 13 185 024 B **Δ**); own offsets
  wandern 0xa1ee98 → 0xa1eeb8. Dekodierte Layer: FG/FH 13 484 048 B (0xCD_C010) · FIb 13 185 040 B
  (0xC93_010); Layout RAW-Section 12 B + FVI-Section 4 B + FV ab 0x10.
- `aeb1671d`: dekodiert FG↔FH **byte-identisch** (0/222 4k-Blöcke); FH↔FIb −310 640 B (>4000 Bytes,
  0x0..0x917EB); PE-Timestamps 2023-06-02 07:01 → 2026-03-16 03:10; PDB
  `…WPBT\WPBT\GigabyteDownloadAssistant\obj\Release\…\.pdb`; .NET/WinForms-Strings.
- `fbf95065`: EFI_TIME-Kopf 2024-01-25 10:07:15 (FG=FH) → 2026-03-09 16:02:40 (FIb); nur-FIb-Strings
  „Microsoft Option ROM UEFI CA 2023", „Microsoft RSA Devices Root CA 2021", CRL/CRT-URLs.
- `76d5cf91` (OA3): dekodiert FG↔FH identisch; FIb +1 504 B, 1 682 Bytes @0xD5..0x9BF, `.text`
  0x553 → 0xA53.
- `deadbeef`: ACPI SSDT (OEM-ID `GBT`, Table-ID `GSWApp`, rev 2); FG↔FH **2 Bytes** (+0x9 =
  ACPI-Checksumme, +0x10F5 AML); FIb +630 B (nur-FIb-AML-String „20251215").
- `414d94ad`: FREEFORM_SUBTYPE_GUID `5a88641b-bbb9-4aa6-80f7-498ae407c31f`, Daten 4 096 B ohne
  lesbare Strings; FG↔FH 511 Bytes @0x158..0x467; FH↔FIb 509 Bytes @0x158..0x467.
- `3fd1d3a2`: „$FID"-Struktur, FFS 164 B konstant; EFI_TIME je Release 2025-09-26 / 2025-10-28 /
  2026-04-14; Strings „8ARNR302", „ALASKA AM I".

<!-- Interpretationsschicht: UEFIExtract „5C60F367" = FvNameGuid (nicht FS-GUID) — Korrektur.
−305 kB = aeb1671d GDA-Rebuild (≈99 %); Details differential.md §4. -->

---

## 2026-10-26 — Phase 4: String-Spuren für Kandidaten (WPBT, AGESA, Release-Notes)

**roh (Dekoded-Layer-Scan je Version + Raw-Scan):**
- `WPBT` ascii: Layer 1 Hit @0x525905 (FIb) — Kontext `WPBTf.C...f.S.I...K.f...`; Raw-Image 0 Hits.
- `AGESA Version : ComboAm4v2PI %s` (utf16) @FG 0x34c63c · FH 0x34c63c · FIb 0x34c78c.
- AGESA-Version-Literal (Layer, ascii, je 1 Fund): FG `1.2.0.F` · FH `1.2.0.F` · FIb `1.2.0.11`.
- `Released Date:` (utf16, Layer) @FG 0x69de30 · FH 0x69db70 · FIb 0x69e1f0.
- Raw: keine WPBT-/Release-UTF-16-/AGESA-UTF-16-Treffer; ascii nur „AGESA Driver".

<!-- Interpretationsschicht: Release-Notes-Textblock nicht im Image (negatives Ergebnis, A);
Release-Identität = 8ARNR302-Version-Block + $FID-Daten. WPBT-Tabelle wird zur Laufzeit von
DXE-Code gebaut (kein rohes Tabellen-Signatur). AGESA-Wechsel FG/FH→FIb: 1.2.0.F → 1.2.0.11
(K5-Falsifikator bestätigt). Kandidatenliste: findings/bug_candidates.md. -->

---

## 2026-10-26 — Neue 4. Release: FId

- User-Übermittlung: Zip `~/Downloads/mb_bios_b550-aorus-elite-v2_8arnr302_fid.zip`
  (11 779 483 B, zip-sha256 `e9c9ffaf42dc31fddb0c6b79ea73a022738c954ad0b3d4489020796de314e5d1`).
- Inhalt: `B550AORUSELITEV212.FId`, 16 777 216 B, Zip-Dateidatum 2026-08-18.
- Entpackt nach `images/reference/B550AORUSELITEV212.FId`; **sha256
  `38784c23f9d69b9d64c6245362ac466ce3517ecf6c36e3147bd2099f1d2ac674`** — ≠ FIb/FH/FG (A):
  also eine vierte, unabhängige Release (nicht byte-identisch mit FIb).
- Korpus jetzt: FG (36c9a32a…) · FH (363e0fc9…) · FIb (d6ce0901…) · FId (38784c23…).
- **Rekonstruktionsnotiz:** Bei der_fid-MD-Generierung wurden `cartography/{fib,fh,fg}.md`
  versehentlich durch eine kürzere Generatoversion ersetzt (6,3→2,1 kB). Wiederhergestellt aus den
  unversehrten JSON-Datenquellen (Generator jetzt `scratches/make_md.py`, alle vier MDs konsistent
  ~8,4 kB, superset-Sektionen: Kopf/Top-FV/Depth-1/Typverteilung/FFS-Files/PSP-Kandidaten/Limitationen).
  JSON-Quellendaten wurden nicht verändert (md5 der fib.json unverändert geprüft).

---

## 2026-10-26 — Modul-Ebene 4-Wege + AGESA-Scan (roh)

**roh (scratches/diff_modules.py → findings/module_diff.md):** FFS-sha geändert FG↔FH 97 · FH↔FIb 55 ·
FIb↔FId 40; je 518 gemeinsame Module, 0 neu/entfernt. Depth-1-Layer-GUID 8c8ce578 n4 (own offset
0xa1ee98→0xa1eeb8→…): Längen 13484032 / 13484032 / 13185024 / 13205504 **Δ**. FIb↔FId Größenbewegungen:
`d9fd094f` (R, driver) 151110→171334 (+20224 B @layer 0x109f1d0); `601f27e3` (freeform) 55340→57388
(+2048); `f80697e9` +192; `ba28936b` +288; `b7246c46` +96; `15e4c005` +128; `899407d7` +160;
`8835d63e` +32; `8f4b8f82` +64; `3f79bee2` +64; `d20d5c9f` +128; `b1da0adf` −250 (220187→219937);
`9e21fd93` (d0) +9082 komprimiert; `84366c9e` (d0) +3; `3e3b6dc0` (d0) +331. `cef5b9a3` fehlt im
FH↔FIb- UND FIb↔FId-Changed-Raster (identisch FG→FId bis auf FG↔FH). `414d94ad` (d0): sha geändert,
±0 B, in allen drei Paaren.

**roh (scratches/agesa_scan.py, dekodierter 9e21fd93-Layer):**

- FG: layer 13484048 · fmt `0x34c63c` · ReleasedDate `0x69de30` · Literale `1.2.0.F` @
  2548594 (0x26e372) / 3137650 (0x2fd207) / 3454002 (0x34b432).
- FH: layer 13484048 · fmt `0x34c63c` · ReleasedDate `0x69db70` · `1.2.0.F` @ dieselben Offsets.
- FIb: layer 13185040 · fmt `0x34c78c` · ReleasedDate `0x69e1f0` · `1.2.0.11` @2548818/3137874/3454290.
- FId: layer 13205520 · fmt `0x34c90c` · ReleasedDate `0x6a2ac0` · **`1.2.0.12`** @2549202/3138258/3454674.

<!-- Interpretationsschicht: Layer-Delta FIb→FId +20480 B ≈ d9fd094f (+20224 B) dominiert;
Summe FFS-Deltas +23174 > +20480 → Padding-Absorption (E, nicht byte-genau). AGESA-Reihe
1.2.0.F → 1.2.0.11 → 1.2.0.12: jede Release hebt AGESA (K5-Falsifikator, A). K6-Fenster
0x158..0x467 mit 4 Datenpunkten 511/509/509/512 geändert B. Details differential.md §5. -->

---

## 2026-10-26 — K6-Payload-Decodierung `414d94ad` (roh)

**Scratches:** `k6_decode.py` · `k6_regions.py` · `k6_repeat.py` · `k6_romlayout.py` · `k6_subwin.py`.
Payload = image[0x92F078 + 44 .. +4096], depth-0, je Release. Payload-sha256: FG `01bf8faf5f9a10c2…`
· FH `9785ff5f95eb65ba…` · FIb `032e3b13b5dbbdda…` · FId `ebf315b5b481f155…`.

- Kopf: GUID `4a3ca68b-7723-48fb-803d-578cc1fec44d` @0x00; u16 @0x10: 0x1000 · 0 · 0 · 1 · 0x1000 ·
  0x100 · 0x1000 · 0x0E38; WIN_CERTIFICATE @0x20: dwLength 0xE18 · wRevision 0x0200 ·
  wCertificateType 0x0EF1; CertType `a7717414-c616-4977-9420-844712a735bf` @0x28; HashType
  `51aa59de-fdf2-4ea3-bc63-875fb7842ee9` @0x38 und @0x248.
- Items: PubKey1 0x48..0x148 · Sig1 0x148..0x248 · PubKey2 0x258..0x358 · Sig2 0x358..0x458;
  pub1 == pub2 in allen 4 (sha `6e3dec6ecaf6e3e2…` ×4); sig je Version: FG `4e94775b`/`0b639eb7` ·
  FH `ed69e1c3`/`5c8227ca` · FIb `e069e7d2`/`c02a13d4` · FId `bd9c0be3`/`d4fc9651`.
- Subfenster-Diff je Paar: Kopf 0 · PubKey-Fenster 0 · Sig1 255/253/256/256 · Sig2 256 je Paar ·
  Padding 0 · RomLayout 0 → je Release ändern sich ausschließlich Sig1+Sig2.
- Padding 0x458..0xE38 alles 0; RomLayout 0xE38..0xFD0 (17 Einträge à 24 B); 0xFD0..0x1000
  Nullen; keine Fingerprints (LZMA/MZ/_FVH/ACPI/PSP) im Payload.
- RomLayout-Einträge (addr4G = 0xFF000000|addr · addr · size · flag · tag):
  r1 0xE40314/0x1BFCEC/0/0x660A · r2 0xE402E3/0x31/0/0x640A · r3 0xE40000/0x2E3/0/0x660A ·
  r4 0xE3F000/0x1000/0/0x4008 · r5 0x9500C0/0x4EEF40/0/0x20A · r6 0x9300C0/0x20000/0/0xA ·
  r7 0x92F000/0xA4/0/0x20A · r8 0x90F000/0x20000/1/0x6200 · r9 0x87000/0x888000/1/0x6200 ·
  r10 0x77000/0x10000/1/0 · r11 0x57000/0x20000/1/0x6200 · r12 0x37000/0x20000/0/0x6200 ·
  r13 0x21000/0x16000/1/0 · r14 0x20000/0x1000/1/0 · r15 0x0/0x20000/1/0 · r16 0x9300A4/0x1C/0/0x20A ·
  r17 0x92F0A4/0x1000/0/0 (Selbstreferenz). Lückenlos 0x000000..0x1000000 (alle addr+size).
- GUID-Referenz (UEFITool `common/ffs.h`): `4a3ca68b-…` = APTIO_SIGNED_CAPSULE_GUID; unsigned
  Pendant `14eebb90-890a-43db-aed1-5d3c4588a418`.

<!-- Interpretationsschicht: Secure-Flash-Capsule-Zertifikat; je Release nur Sig-Neuerzeugung;
PubKey + RomLayout konstant über alle 4 Releases. Konsequenz: K6-Fenster Korrektur-Tabu
(differential.md §6). -->

---

## 2026-10-26 — K3-Payload-Decodierung `cef5b9a3` (roh)

**Scratches:** `k3_decode.py` (Runs/Transitionen/Hexdump je Run) · `k3_shift.py` (Entry-Kette +
Shift-Check, Output `k3_shift_out.txt`). Section-Data @0x37094 (RAW-Section 0x52, 4-B-Kopf
abgetrennt), 0x1FF6C = 130 924 B je Release. Payload-sha256: FG `f08118a530289e297d82bdfd462b34ce` ·
FH == FIb == FId `6915b416e562ba506770ab43561f36d5`.

**roh u32@0:** FG `0xFFFF0725` · FH/FIb/FId `0xFFFF0724`. Kopf: `FF 83 00` + `"StdDefaults"`.
Entry-Kette ab 0x13 (FG-Koordinaten; FH+ um −1 verschoben ab 0x2A6):

| Entry | FG @ | Size | Attr | State | Name |
|---|---|---|---|---|---|
| 1 | 0x0013 | 0x0294/0x0293 | 0x83FFFFFF | 0 | `Setup` |
| 2 | 0x02A7/0x02A6 | 0x001E | 0x83FFFFFF | 1 | `PlatformLang` (`en-US`) |
| 3 | 0x02C5/0x02C4 | 0x0068 | 0x83FFFFFF | 2 | `AMITSESetup` |
| 4 | 0x032D/0x032C | 0x0015 | 0x83FFFFFF | 3 | `XhciDID` |
| 5 | 0x0342/0x0341 | 0x0254 | 0x83FFFFFF | 4 | `GcSensorVarName` |
| 6 | 0x0596/0x0595 | 0x001E | 0x82FFFFFF | 5 | `PCI_COMMON` |
| 7 | 0x05B4/0x05B3 | 0x0019 | 0x83FFFFFF | 6 | `SioSetupData` |
| 8 | 0x05CD/0x05CC | 0x0047 | 0x83FFFFFF | 0 | `UsbSupport` |
| 9 | 0x0614/0x0613 | 0x0023 | 0x83FFFFFF | 7 | `NetworkStackVar` |
| 10 | 0x0637/0x0636 | 0x0022 | 0x83FFFFFF | 8 | `SecureBootSetup` |
| 11 | 0x0659/0x0658 | 0x0018 | 0x83FFFFFF | 9 | `Setup` (2.) |

Kette endet @0x671 (FG) / 0x670 (FH+); danach FF bis 0x724 (in FH+ `FF` füllt die freigewordene
1 B); Rest 0x724..0x1FF5B alles FF; **letzte 16 nicht-FF-Bytes @0x1FF5C..0x1FF6B (Image 0x56FEC..):
`6f d2 99 45 11 1a b8 49 b9 1f 85 87 45 cf f8 24`** — in allen 4 Releases identisch, kein
bekanntes Magic (unbenannt).

**roh FG↔FH-Diff:** 415 B / 43 Runs, hull 0x0000..0x0720. Runs (Start, Länge): 0x0000(1) · 0x0017(1) ·
0x0297(1) · 0x029C(2) · 0x02A0(1) · 0x02A2(1) · 0x02A6(7) · 0x02AF(28) · 0x02CD(14) · 0x032B(8) ·
0x0335(19) · 0x034A(18) · 0x036D(3) · 0x039A(3) · 0x03C7(2) · 0x03F4(2) · 0x0421(2) · 0x0595(7) ·
0x059E(9) · 0x05A8(3) · 0x05B3(7) · 0x05BC(15) · 0x05CC(7) · 0x05D5(8) · 0x05DE(6) · 0x05EA(3) ·
0x060C(1) · 0x060E(3) · 0x0612(8) · 0x061C(18) · 0x062F(1) · 0x0631(1) · 0x0633(1) · 0x0636(7) ·
0x063F(10) · 0x064A(9) · 0x0658(7) · 0x0661(8) · 0x066C(1) · 0x066E(1) · 0x0670(1) · 0x0680(116) ·
0x06F5(44).

**roh Shift-Check:** D = FG mit FG[0x297] entfernt; D vs FH → Diffs nur `0x0000` (u32-Länge
0x0725→0x0724) und `0x0017` (u16 Setup-Size 0x0294→0x0293); +16 @0x1FF5B.. als −1-Verschiebungs-
Artefakt im FF-Tail des eigenen Checks (roh dort 0).

**roh gelöschtes Byte:** FG[0x297] = 0x0F, Datenoffset im `Setup`-Entry = 0x297 − 0x24 = **0x273**;
Kontext (0x288..0x2A0) FG `…21 FF 00 01 00 01 0F 0F 0F FF FF FF FF FF 02 00 00` ·
FH/FIb/FId `…21 FF 00 01 00 01 0F 0F FF FF …` (Dreier-Folge 0x0F → Zweier-Folge).

<!-- Interpretationsschicht: AMI-StdDefaults-NVRAM-Store; FG→FH exakt 1 Default-Wert 0x0F
entfernt + 2 Längenfelder nachgezogen; alle übrigen Runs = Shift-Artefakte (differential.md §7).
Schalter-Benennung offen (IFR-Mapping nötig). -->

---

## 2026-10-26 — K1-Fix rea: `_FVH`-Discovery in Raw-FFS-Body (roh, Nach-Fix-Scan FId)

**rea-Change:** `UefiImageScan.ts` — `walkSectionChain` prüft RAW-FFS-Bodies (typeCode 0x01) mit
leerer oder nur-Bogus-Kette einzeln auf eingebettete FVs (`scanVolumesInRegion` mit depth+1,
logical_path `…/embedded`, admission unverändert: Alignment/FvLength/Header-Checksumme/Blockmap/
Budgets). Keine Schema-Änderung (flache Volumes-Liste + parent_offset + logical_path).

**roh Nach-Fix-Scan FId (`scratches/k1_fid_after.md` + JSON):**
- firmware_volumes: **10** (vorher 9) — Top 0x37000 · 0x92f000 · 0xe3f000 · 0xe40000 + Depth-1
  0x9300c0 · 0x950110 · 0x951160 · 0x95b4c0 · 0xa0bf70 · 0xa1eeb8.
- Neu: `flash/FV@0x92f000/FFS:05ca020b-0fc1-11dc-9011-00173153eba8/embedded/FV@0x9300c0` —
  offset 9633984, length 131072, depth 1, parent_offset 9629696, sha256
  `c2dd2665eea1591e44227656e9fa54b05705e9d926445e42a6908813a6e6e3f9`, FS-GUID FFS2,
  header_length 72, attributes 64255 (0xfaff), revision 2, blockmap {32 × 4096}.
- FFS `05ca020b`: type raw, length 131096, **sections []** (Bogus-Zero-Length-Record weg).
- FV-Inhalt (`ffs_files`, 2):
  - pad `ffffffff-…` @0x9300e8 …offset 9634056, len 44, state 248;
  - freeform `7bb28b99-61bb-11d5-9a5d-0090273fc14d` @9634104 (0x930118), len 26767, state 248,
    sha256 `ac7866c95dfb271961561c6d6597fb671f1a53ff22788e1bf84f2c2550114d3c`, 1 Section
    @9634128 (0x930130): `guid-defined`, len 26743, compression **lzma-custom**
    (`ee4e5898-3914-4259-9d6e-dc7bd79403cf`), data_offset 24, attributes 1, sha256
    `f4ee341cdf61169ebca4d8981bdfb1d8d431cb466794534dcf3d65e1ba0ab3b0`.
- Limitations neu: 1 Zeile „Raw file body … reinterpreted: 1 embedded firmware volume(s) …";
  20 „_FVH hit … not confirmed: header-unparseable" (wie vor dem Fix); `ce3233f5`-Gap unverändert;
  coverage **complete**.
- Extract: `--volume-offset 0x9300c0` und `--file-offset 0x930118` → beides abgelehnt
  („No physically mapped … at offset"; Extractor-Index kennt nur Depth-0-FFS) — residual, kein
  Output-Directory angelegt. LZMA-custom-Section → Dekodierung via Dekoder-Lane trivial, Ziel Phase 5.

**Tests:** `UefiImageScan.test.ts` 10/10 (+positives 0x9300c0-Muster, +negatives unframed-body);
uefi+acceptance 43/43. (Voll-Suite-Lauf separat geloggt.)

<!-- Interpretationsschicht: Parser-Fix bestätigt Falsifikator (6. FV wird gemeldet); FV@0x9300c0
Träger eines LZMA-komprimierten Ami-Blobs (GUID 7bb28b99, freeform) — 26 719 B komprimierter
Stream; Zweck
weiterhin unbestimmt (E), jetzt aber dekodierbar und Phase-5-Extraktionsziel. Extractor-Selektoren
sehen Depth-0-Index → residual dokumentiert. -->

## 2026-10-26 — K2-Fix rea: `ce3233f5` = EFI_GUIDED_SECTION_ZLIB_AMD (roh, Nach-Fix-Scan FId)

**Identifikation (UEFITool-Quellen, `/run/media/julian/ML4/coreboot/coreboot/UEFITool/`):**
- GUID `ce3233f5-2cd6-4d87-9152-4a238bb6d1c4` = EFI_GUIDED_SECTION_ZLIB_AMD (`common/ffs.h:451`);
  Begleiter `991efac0-e260-416b-a4b8-3b153072b804` = ZLIB_AMD2.
- Parse-Pfad `ffsparser.cpp` @2859: `dataOffset += sizeof(EFI_AMD_ZLIB_SECTION_HEADER)` (=0x100);
  Decode @3389 `zlibDecompress(body)`; `utility.cpp` @543 `inflateInit2(&stream, 15U)` —
  zlib-WRAP, nicht raw-deflate (raw −15 schlägt mit „invalid stored block lengths" fehl).
- Header-Mapping am FId-Rohbild verifiziert: Section-Basis @0xe41fe8 (Basis = pos−4 im GUID-Block),
  GUID @+4, DataOffset u16 @+16 (=0x18), Attributes @+18 (=0x0001); EFI_AMD_ZLIB_SECTION_HEADER
  ab Payload: 256 B = 0×14 Null + `CompressedSize` u32 LE @0x14 + 0×E8 Footer; zlib-Stream
  ab Payload-Offset 0x100 (`78 da`).
- Ground truth: Section size 0xf94c0 = 24 + 256 + 1 020 840 exakt (`msgInvalidCompressedSize`-Bedingung
  von UEFITool erfüllt); Decode (`wbits 15`) → 3 932 192 B (0x3C0020) = RAW-Section (28 B, 0x19) +
  FVI (0x3c0004, 0x17) + FV @0x20 (FvLength 0x3C0000, FFS2, Checksumme i. O., ext-header @0x60) —
  `scratches/k2_peifv.bin`, sha256 d9a7e8dcbe4b2731…; FV-Angel 0xe41fe8+0x18+0x20 = 0xe42020.

**rea-Change (Schema-Change → Katalog regeneriert):** kind `ami-zlib` in
`FfsSections.ts` (Union + `AMD_ZLIB_HEADER_LENGTH = 0x100` + `peelAmiZlibPayload`) und
`UefiCodeTables.ts` (GUID-Map); Enums in `domain/uefi/uefiFirmwareAnalysis.ts` (compression kind +
files source `decompressed-zlib`); `UefiImageScan.ts`: `UefiLzmaDecodeRequest.format: "lzma"|"zlib"`,
Gate `isDecodableKind` (ami-zlib dazukommen), `resolveDecodedSection` peelt 0×100 (Limitations bei
zu kurzem Payload; bei CompressedSize-Mismatch bleibt Dekodierung laufen), Pfad-Element `/zlib`,
physicalRange = Stream-Start; `UefiAnalysisProvider.ts`: `#decodeStream` — zlib synchron via
node:zlib inflateSync (Budget `lzmaOutputBytes`, RangeError → output-limit-Meldung;
decoderVersion = `process.versions.zlib`), LZMA unverändert über Worker; `stageLzmaSection` peelt,
Gap-Texte format-bewusst, Passthrough = voller Carrier (inkl. AMD-Header); `stagedDecoded` parametriert
(source `decompressed-zlib`/`decompressed-lzma`, Handler `node-zlib@…`/`lzma-purejs@…`);
Extraktions-Gating nimmt ami-zlib auf. Diagnostics-Wording „decode attempt(s)" (war „LZMA …").

**roh Nach-Fix-Scan FId (`scratches/k2_fid_after.json`):**
- firmware_volumes: **11** (vorher 10) — neu
  `flash/FV@0xe40000/FFS:3e3b6dc0-064d-4b01-9203-7836c9b498e7/section[0]/zlib/FV@0xe42020`,
  offset 15036448 (0xe42020), length 3932160 (0x3C0000), depth 1, parent_offset 0xe40000,
  FvLength == Prediction aus Hand-Dekodier.
- PEI-FV-Inhalt (Walkable, Auszug): pad; freeform `1b45cc0a` (a-priori-Art) 172 B; freeform
  `5b85965c` 60 B; **pei-core `52c05b14-0b98-496c-bc3b-04b50211d680`** (ui „P") 0x5f0e;
  peim `7eb7126d` (ui „R") 0x34da; peim `c779f6d8` (ui „C"); peim `86d70125` (ui „D");
  peim `ae265864` (ui „C"); … (je depex/te/ui/version-Sections; vollständige Liste im Scratch-JSON).
- Limitations: 4× „_FVH hit under …/zlib at … not confirmed: header-unparseable" (konservative
  Kandidaten-Verwerfungen im dekodierten Stream, 0xe42fef/0xe46f58/0xfc9ed1/0xfe0a89);
  keine zlib-Decode-Failure; coverage **complete**.

**roh Extract FId** (`scratches/k2_extract.json`, Outdir `k2_extract_3e3b6dc0/`):
`--file-offset 0xe41fd0` → 1 staged File
`section-0xe41fe8.decoded.bin`, source **decompressed-zlib**, size 3 932 192,
original_file_range 0xe42000+0xf94a8 (voller Carrier inkl. AMD-Header),
derivation handler **node-zlib@1.3.2**; sha256 == `k2_peifv.bin` (Hand-Dekodier) — md5/Vergleich EQUAL;
coverage **complete**, extraction_gaps: 0.

**Tests:** `FfsSections.test.ts` 6/6 (+Klassifikation +Peel, Short-Payload → null);
`UefiImageScan.test.ts` 11/11 (+ami-zlib-Lane-Test: format „zlib", g peeled Stream, Pfad `/zlib/FV@`);
`UefiAnalysisProvider.test.ts` 9/9 (+End-to-End mit echtem zlib.deflateSync: inspect 2 Volumes,
extract → decompressed-zlib + node-zlib@-Derivation, coverage complete, 0 Gaps);
uefi+acceptance **46/46**. MCP-Katalog `ami-zlib` + `decompressed-zlib` nachgewiesen.
(Voll-Suite-Lauf `npm test` separat geloggt.)

## 2026-10-27 — P-1 Forensik SecSMIFlash 3370a4bd (roh)

- Quelle: `…/lzma/FV@0xa1eeb8/FFS:3370a4bd…/section-0x1277f88.payload.bin` (23 552 B PE32 x64),
  MCP-Ghidra-Session + Offline-Objdump (`scratches/smf_text.dis`, `smf_hooks.dis`). VA = FO+0xC00
  (.text) / FO+0x1A00 (.data); Entry RVA 0x1300 (aus OptionHeader).
- Kette dekompiliert: 0x27e0 (HandleInit: gBS/gRT/ST; Flash-Wrapper-Protokoll) → 0x241c (Main-Init:
  Staging 0x1004000 B, Digest-Tabelle 0x20000 B (4096×32-B = 4-KB-Pages, Fill 0xdb), 0x7c-Descriptor,
  Crypto-Protokoll DAT_6b80 via GUID@0x6090 (+embedded-Key-Load), **Flash-Device-Protokoll gehookt
  [1]/[2]/[3] → 0x21c8/0x2148/0x2188, Originals gesichert (6bc8/6bd8/6bc0; 6bd0 von 0x2bf0)**,
  Disposition @0x61d0 {0x1d68, 0x1988, 0x1a1c, 0x321c}, SW-Dispatch 7739f24c-…) → 0x1a1c (SMI-Cmd
  1/2/4/8: Staging, Dual-Capsule @+2 MB, per-4-KB-Page-SHA256, $BAD-Toleranz für 2|8) → 0x321c
  (Verify: 0x2e6c/0x2cd8 RomLayout-Hash, 0x3038 RSA2048/SHA256-Zertifikatskette, 0x2900/0x29a8
  Version/Rollback) → 0x175c (Write-Trigger: Descriptor + SetVariable "CapsuleUpdateData"
  GID@0x6160, del→Attr 7 size 8; **NVRAM-Handoff, Write-Engine = Boot-Phase**) / 0x18a4 (Cmd 1:
  "AmiFlashUpd" @GUID 0x61b8, 0x1d-B-Block). 0x4574 = FCH-Reset (`out 0xb2, 0xbe`).
- Hooks (Objdump-Beleg): identisches Wrapper-Pattern FUN_2024-Gate → Original-Fallthrough; Gate
  0x2024 = RomLayout-Zugriff (Allow-Bit-4, Bypass-States 0x12/0x20, **Capsule-Schmuggel-Scan**
  0x2b84 ±0x102c/+0x1000, Flag ↑ 0x200 nach Scan-Treffer).
- **K6-D-Entscheid (Falsifikator ausgeführt, negativer Arm):** die Prüfung hasht via RomLayout fast
  den ganzen Chip — inkl. DXE-Haupt-FV [0x87000,0x92f000) und Content-FVs [0x9500c0,0xe3f000); die
  414d94ad-Capsule enthält die Regionliste (17 Einträge à 24 B, Flag&0x200 = Hash; Offsets
  chip-absolut, ItemOffset 0x1000 == HeaderSize). **L2/L3 im Covert-Bereich nicht machbar ohne
  Prüfstellen-Mitführung; K6-Tabu verlängert sich.** Löcher dokumentiert (K9): 128-KB-Loch-FV,
  64-KB-Erase, PSP-[0,0x37000), 4-KB-FV@0xe3f010 + Selbst-Ausschluss des 414d94ad-Körpers.
- GUID-Constanten python-geparst (autoritativ): 0x6020 = gEfiHashAlgorithmSha256 (51aa59de-…),
  0x60b0 = Capsule-GUID, 0x6090 Crypto, 0x6010 Flash-Hook-Protokoll (ecb867ab-…), 0x6160/0x61b8 =
  NVRAM-Var-GUIDs, 0x61a8 = 414d94ad-Konstante, 0x6210 = 5a88641b, 0x6220 = $FID-Block 2ebe0275-…;
  Strings: "CapsuleUpdateData", "AmiFlashUpd", "MonotonicCounter", "%s%d" + Plattform-Codenamen
  "Taishan"/"Sandstone"/"Huashan"/"Shasta"/"Unknown" @0x6b70.. (Codename-Selektion, B).
- Neue Kandidaten registriert: **K8** (Hash-Scope verhindert L2/L3 im Covert-Bereich — Analyse-
  Ergebnis, K6-Tabu-Verlängerung), **K9** (Flash-Hook-Gate: Löcher default-schreibbar + Anti-
  Smuggling-Scan), **K10** (Anti-Rollback-Floor 9.04 ⇒ Rollback via QFlash-ISP, nicht NVRAM).
- Residual: 0x2cd8-Digest-Quelle (vermutlich 29a8-$FID-Block/WinCert), 0x1d68/0x1988
  (Disposition-Slots ohne Ghidra-Prozedur, nur Disasm-Gerüst), exact Codename-Referenzstätte
  Taishan/…-Selektion; 0x4d5c/0x4878-Basis-Reader unausgelotet.

## 2026-10-27 — P-2 K3-Schalter benannt: doppelte IOMMU-Frage (roh)

- Quelle: Setup-PE32 (FFS-GUID `899407d7-99fe-43d8-9a21-79ec328cac21`) je Release — FG/FH
  hartverdrahtet in `scratches/k3_q.py` (FIXED_PE), FIb gecarvt aus
  `extracted/fib-fvmain/…/section-0xa1ee90.decoded.bin` (FFS @0x3288b0, Type 0x07 @+0x12),
  FId = `…FV@0xa1eeb8/FFS:899407d7…/section-0xd47950.payload.bin` (0x144a00 B; die drei
  anderen 899407d7-Sektionen = 0x5a-Header + UCS2 „Setup"/„1.0"). HII-Package-List je Release:
  FG/FH @0x2a8a0+0x119dbc/0x119d80, FIb/FId @0x2a8e0+0x119bf9/0x119c85; Forms-Typ-2-Paket
  @+0x14, je 19/18 Pakete (FG 19, FH 19, FIb/FId 18 — FId +1 Typ-0xDF-Paket).
- IFR-Walk (`k3_ifr.py`, EDK-II `UefiInternalFormRepresentation.h`-Semantik): FG stop@0x34dff
  6679 Records/812 Fragen; FH stop@0x34dc3 6668/811; FIb 6666/811; FId 6666/811 — 0 fails
  über alle vier.
- **Befund:** FG = zwei IOMMU-Steuerungen auf zwei Setup-Varstore-Slots (EC87D643-…, vid 1):
  qid `0x01a6` @vo `0x025F` (Disabled=00/Enabled=01/Auto=FF; zusätzlich gepostet als qid
  `0x0251` am gleichen Slot) **+** qid `0x01a7` @vo `0x0271` (Prompt/Help sid 0x052b/0x052c =
  „IOMMU"/„Enable/Disable IOMMU Support"; Optionen Auto=`0x0F`/Disabled=`0x00`/Enabled=`0x01`.
  Keine IFR-DEFAULT-Records an dieser Frage). FH entfernt die vo-0x271-Instanz: −60 B Forms-
  Paket (0xA54B→0xA50F), Setup-Varstore 0x283→0x282, Varoffsets>0x271 und qids>0x01a7 je −1;
  String-Pool byte-identisch (en-US 3327 beide). FIb/FId = FH-Stand (Forms 0xA50B, Records
  6666; FId-PE-Bump +160 B, en-Pool 3329 = FIb; IOMMU-sid dort 0x052d, Postings 2 @0x25F).
- **NVRAM↔IFR (A):** Setup-StdDefaults-Daten = IFR-Varstore-Layout 1:1 (Datenoffset =
  Varoffset, Basis 0). Verifiziert über verschiene Slots: FH/FId `Daten[0x271]` = `0x0F` =
  IG-Post-Frage qid `0x2a2a` (DEFAULT-Record Value 0x0F), `[0x272]` = UMA-Mode-Auto, `[0x273..]`
  = `FF FF FF FF` = UMA Frame Buffer Size (u32, Factory FFFFFFFF = Auto), `[0x277]/[0x278]` =
  Display-Res `FF` / SATA `02` — alle = die geparsten IFR-Defaults. FG-Daten[0x271..0x273] =
  `0F 0F 0F` (IOMMU#2-Auto + IG-Post-Auto + UMA-Mode-Auto); FH verliert das IOMMU#2-Byte.
  Byte-genau liegt das Loch in der Dreier-Reihe (Shift-Check mit 0x297 = Daten 0x273 = gültiges
  Run-Mitglied); semantisch eindeutig = **Slot `0x0271`**. K3's „Datenoffset 0x273" korrigiert
  als Slot-Eigentümer auf `0x271` (`differential.md` §7/§7.1, `bug_candidates.md` K3-Ergebnis).
- Scratch-Ergebnisse: `k3_q_{fg,fh,fib,fid_raw}.json` (je Release Fragen + Options + Defaults;
  `k3_q.py`'s qdefault liest DefaultId/Value vertauscht — real EFI_IFR_DEFAULT = DefaultId u16
  @+2 zuerst; Inline-Neulesung korrekt, File bleibt unkorrigiert da Auswertung daten-getrieben
  erfolgte).

<!-- Interpretationsschicht: Dekompressor-Befund aufgelöst — kein unbekannter Algorithmus, sondern
AMD-spezifische zlib-Verpackung mit 256-B-Header; PEI-Phase (PeiCore+PeiM) jetzt im rea-Modell.
K1+K2 schließen „Session-Integration" von bug_candidates.md ab; verbleibende Gaps sind
Observation-Level (false-positive FVH-Kandidaten im dekodierten Stream). Extractor-Work-Around
über --file-offset des physisch gemappten Träger-FFS funktioniert; Depth-1-Selektoren bleiben
Phase-5-residual (wie K1). -->

## 2026-10-27 — P-3 WPBT-Builder WpbtDxe 0996199f (roh)

- Modul im DXE-Layer je Release lokalisiert (FFS-Name-GUID raw `9f199609e22c974d830b077a7b28588a`):
  FG @0x524d68 · FH @0x524d28 · FIb @0x5252e8 · FId @0x525508; Type 0x07, State 0xf8, Size
  0xb1a (FG/FH) / 0xb3a (FIb/FId); 4 Sections (DEPEX 0x13/0x3a · PE32 0x10/0xac4 · UI 0x15
  „WpbtDxe" · VERSION 0x14 „1.0"). ⚠ eine erste Same-Day-Messung las den FFS-Size u24 @+4
  statt @+0x14 und erzeugte ungültige Körper-Hashes/Riesenschnipsel — ersetzt durch
  `p3_hashfix.py` (size @+0x14).
- Cross-Release (`p3_hashfix.py`/`p3_pe_delta.py`; sha256 16-B-Präfix): FFS FG `348f76cd…` ·
  FH `a0dcd50e…` · FIb==FId `5f643556…`; PE FG `624a78b7…` (2720 B) · FH `afac2e93…`
  (2720 B) · FIb==FId `4f4c4218d849780c…` (2752 B, FId-Bau `…/lzma/FV@0xa1eeb8/FFS:0996199f…/
  section-0xf44404.payload.bin`). FG↔FH = exakt 1 Byte @PE-0x4bc (`83`→`82`): FG
  `48 c7 44 24 30 83 02 00 00` = MOV qword ptr [RSP+0x30], **0x283**; FH/FId = **0x282**
  (FId-Bau @0x491). FH↔FIb separater Rebuild (+32 B, e_lfanew 0xd0→0xd8 @0x3c, 1779 Diffs im
  2720-B-Overlap, common suffix 0x16; FG↔FH common suffix 0x5e3). FIb↔FId byte-identisch.
- Ghidra (FId-PE, 6 Prozeduren: 0x2e0 Entry / 0x360 FV2-Read / 0x478 Builder / 0x688
  ReadyToBoot-Cb / 0x6ac StrLen16 / 0x6e0 strcpy16): Entry → CreateEventEx(0x200
  EVT_NOTIFY_SIGNAL, 0x10 TPL_CALLBACK, 0x688, EventGroup gEfiEventReadyToBootGuid @0x930) →
  je Boot → 0x478 → CloseEvent.
- 0x478: GetVariable(L"Setup" @0x950, GUID @0x900 = EC87D643-EBA4-4BB5-A1E5-3F3E36B20DA9,
  DataSize 0x282 FId / 0x283 FG, 0x282-B-Buffer) → Gate `cmp byte [RBP+0x1b4], r14b`
  (RBP = RSP+0x100 → SetupData[0x264]): 0 ⇒ EFI_UNSUPPORTED (-0x7ffffffffffffffd); sonst
  LocateProtocol(gEfiAcpiTableProtocolGuid @0x8f0) + FUN_360 (LocateHandleBuffer FV2 @0x8e0 →
  HandleProtocol → +0x18 = FV2→Read(GUIDs @0x910 = [aeb1671d-019c-4b3b-ba00-35a2e6280436,
  NULL @0x920], SectionType 0x10)) → AllocatePages(MemType 9 = EfiACPIReclaimMemory,
  ceil((size+0x34)/0x1000)) → WPBT-Header: Sig „WPBT", Rev 1, Length 0x34, OemId „ALASKA"
  (@0x940), OemTableId „A M I" (@0x948/0x94c), OemRev 1, CreatorId „GBT ", CreatorRev
  0x25021100; CopyMem(EXE @Base+0x34); ImageSize @+0x24, ImageAddress @+0x28 = Base+0x34,
  word[0x30] = 0x101, word[0x32] = 0; InstallAcpiTable(0x34-B-Buffer).
- Statisch (A): Args-Feld nie beschrieben — FUN_6e0(src=R8=0) → EFI_INVALID_PARAMETER
  (NULL-Guard); inlined StrLen16-Tail @0x611 liest `cmp word [r14], r14w` mit R14 = 0
  (NULL-Read-Branch, D).
- IFR/NVRAM (`p3_wpbt.py` → `p3_wpbt_out.json`, alle 4 Releases): Gate qid `0x019c` ONE_OF
  „APP Center Download & Install" (FG/FH Prompt-sid 0x0920, FIb/FId 0x0922), Optionen
  Disabled/Enabled 0x0922/0x0923 bzw. 0x0924/0x0925, DefaultId-0x0000-Default = 0x01,
  kein Suppress/Disable/Gray am Frage-Knoten (Kontext-Check; vorstehende GRAY_OUT_IF
  @0x317d2 gehört zur Nachbarfrage 0x019b). NVRAM FG/FH/FId Setup[0x264] = 01, Kontext
  [0x260..0x26e] = ffff27000100000000030021ff00; FIb-StdDefaults nicht materialisiert
  (Glob unter fib-fvmain → []), §7-FH-Identität übernommen. Nachbarn: vo 0x260 Remote
  Display Feature (FG qid 0x0252 → FH/FIb/FId 0x0251), 0x261 Gnb Hd Audio, 0x262 Above 4GB
  MMIO Limit, 0x265 Preferred Operating Mode; 8-fach-Familie qids 0x2821–0x2828 @vo 0x263
  „Output Select" („Unknown Device"-Strings mehrfach).
- npm test (User-Auftrag): erster background-Lauf (btyawncnf) wurde abgebrochen (killed),
  output-file leer; Lauf neu gestartet (b55empjnl) — Ergebnis offen.

<!-- Interpretationsschicht: „WPBT" @Layer-0x525905 gehört zu 0996199f (WpbtDxe), nicht zu
aeb1671d — die Tabelle wird je Boot nach ReadyToBoot gebaut, gekoppelt an den Setup-Schalter
0x264 („APP Center Download & Install", Default Enabled). FG↔FH-1-Byte-Delta =
DataSize-Immediate → §7.1-Varstore-Schrumpfung über zwei Module bestätigt. K4-Level L3→L0/L1.
Details `differential.md` §9. -->