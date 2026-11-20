# Bug-Kandidaten (Phase 4)

**Datum:** 2026-10-26 · **Zielkorpus:** `B550AORUSELITEV212.{FG,FH,FIb}` (eigene Images)
**Basis:** `differential.md` §3/§4 · `crosscheck.md` §3/§4 · `module_diff.md` · `module_inspect.md` ·
Layer-String-Scans (roh: `session-log.md`, Phase-4-Abschnitt) · Community-Wissen.
**Disziplin:** Beobachtungs-Korpus — hier nur Kandidaten mit prä-registrierten Falsifikatoren;
keine Korrektur vor der User-Abstimmung und vor Phase-5-Ritual (Backup/Rollback).

**Grade:** A = exakt gemessen (Bytes/zwei Tools) · B = ein Tool, reproduzierbar · C = Community-Konsens ·
D = Struktur-Inferenz · E = Spekulation.
**Korrektur-Level (Pyramide):** L0 = nur Tool/Analyse (kein Image-Eingriff) · L1 = Datenregion-Swap ·
L2 = Modul-Content-Swap (Checksummen neu) · L3 = Modul-Entfernung/Neutralisierung + Referenzpflege ·
L4 = AGESA/Microcode/PSP (höchstes Risiko, PSP-Signaturregionen tabu).

| ID | Kandidat | Quelle (Grad) | Schadenshypothese (TT) | Falsifikator (EE) | Modul / Bytes | Level | Aufwand |
|---|---|---|---|---|---|---|---|
| K1 | rea-Parser: FV @0x9300c0 fehlt (Bogus-Zero-Length-Section) | A (`crosscheck.md` §3) | Kartografie unvollständig; Korrekturen im 0x9300c0-Areal unmöglich/ablenkend | Test-Fixture „FFS mit eingebettetem FV (Zero-Vector + gültige Header-Checksumme + blockmap)"; nach Fix muss `inspect_uefi_firmware` das 6-te FV melden — sonst Fix falsch | FFS `05ca020b` @0x9300a8, FV-Bereich 0x9300c0..0x9500c0 (26 684 non-FF-Bytes) | L0 | M |
| K2 | Dekompressor `ce3233f5` unbekannt (PEI-FV 44a2d731 unsichtbar) | A (`crosscheck.md` §4) | PEI-Phase (PeiCore, CapsulePei, RomLayoutPei) fehlt im rea-Modell | Hand-Dekodierung des 20-B-Präfix + `5d 92 0f 00`-Streams; wenn trotzdem Fail → UEFIExtract-Quelle lesen (Bios2gpio-amd-Klon hat Sourcen) | FFS `3e3b6dc0` @0xe41fd0/0xe41fe8, Section ~0xf939d B | L0 | M |
| K3 | Setup-Defaults `cef5b9a3`: 415 Bytes FG→FH (FH==FIb) | A (exakte Byte-Zählung, `differential.md` §3#2) | Default-Wert-Änderung zwischen FG und FH — kann User-sichtbare Defaults (Power/SATA/fTPM-Display) betreffen; ggf. der „sichtbare Bugfix“ des Releases | HII-Formset-Decodierung FG↔FH: wenn die 415 Bytes nur Padding/Alignment sind (keine Namens-Wert-Paare), entfällt TT | FV@37000, FFS @0x37078 (raw 130 952 B), Diff verteilt über 415 B | L2 | S (Analyse) / M (Fix) |
| K4 | WPBT-Modul `aeb1671d` = Gigabyte-Download-Assistant-.NET-EXE | A (PDB, Strings, −303 047 B) · C (bekanntes Gigabyte-Verhalten) | Firmware-injizierte Windows-AutoStart-EXE (WPBT): Start/Tel­emetrie/Auto-Update-Programm jedes Windows-Boots — das Community-bekannte „Störverhalten“; FIb-Rebuild 2026-03-16 zeigt: aktiv gepflegt | WPBT-Tabelle im Boot nachweisen (Windows: `GetSystemFirmwareTable("WPBT")` / Task-Manager-Sichtbarkeit des Programms); wenn keine WPBT-Tabelle gebaut wird → TT entfällt | DXE-Layer `aeb1671d` (dekodiert 906 584→595 944 B; FFS 712 518→409 471); WPBT-Code-Ref @Layer-0x525905 (Tabelle wird zur Laufzeit gebaut) | L3 | M |
| K5 | AGESA-Bump nur FG/FH→FIb: **1.2.0.F → 1.2.0.11** (+ ~264 kB PSP/Non-FVS-Region) | A (Layer-Strings, Roh-Diff) | AGESA-Update = wahrscheinlicher Träger der fTPM/PPM-Stutter- und SOC-Power-Fixes; „bekannte Fehler“-Klasse im AGESA-Anteil | AGESA-String je Version nachweisen (erledigt: `ComboAm4v2PI %s` + Literal 1.2.0.F/1.2.0.11); geographisch deckungsgleich mit der 264-kB-Region bestätigt | 0x57000–0x92f000 (PSP-File-Bereich) + Layer-Codestück @0x34c78c | L4 (Fix) / L (Analyse) | L→X |
| K6 | Opaker Blob `414d94ad` (Subtyp 5A88641B, 4 096 B Daten) | A (Bytes) · E (Bedeutung) | Unbenannter je-Release-Blob (~511/509 B @0x158..0x467) — solange unidentifiziert ist er ein Korrektur-Tabu-Bereich | Struktur-Decodierung (AMI-Tools/UEFITool + Byte-Vergleich gegen bekannten Subtypen); Dekodierung schlägt TT fehl | FFS @0x92f078 (FV@92f000, depth 0), Section 4 116 B, Fenster 0x158..0x467 | L0 (erst analysieren) | S |
| K7 | Microsoft-Zertifikat-Bundle `fbf95065` (+1 825 B in FIb) | A (Strings + EFI_TIME) | Aktualisierte Secure-Boot-/Option-ROM-CAs (`…UEFI CA 2023`, `…Root CA 2021`) — kein Bug; Korrektur-Relevant nur bei Custom-Cert-Enrollment | Bundle-Struktur dekodieren und gegen offizielle Microsoft-Zertifikat-Pakete (uefi.sigdb/DBX) vergleichen | DXE-Layer, RAW/0x18-Section, EFI_TIME 2024-01-25 → 2026-03-09 | L1/L2 (mit Signatur-Vorsicht) | M |

## Release-Notes-Spur (Plan-Schritt 1, negatives Ergebnis)

- Keine „Release Note“-Strings im Image (ASCII/UTF-16, Layer + Raw) — **A (negativ)**.
- Release-Identität stattdessen: Versions-Block in `56e14f88` (`8ARNR302{FG,FH,FIb}`, 3–5 B/Version),
  `$FID`-Dates in `3fd1d3a2` (2025-09-26 / 2025-10-28 / 2026-04-14), „Released Date:"-Setup-String
  (Layer @0x69de30/0x69db70 — FG/FH-Wert nur via `%s` zur Laufzeit).

## Empfehlungsspur (vor der Abstimmung)

- **Analyse-First (K3+K6, L0):** billig, kein Image-Eingriff, schärft K4/K5-Entscheidungen.
- **K4** ist der unmittelbare „bekannte Fehler“-Kandidat mit sauber identifiziertem Modul.
- **K1/K2** vervollständigen die Session-Integration (User-Entscheidung #2) — Tool-only.
- **K5** als Beobachtungs-/Falsifikate-Spur weiterführen (L4-Korrekturanstrengung ausdrücklich
  abgeraten, außer mit AGESA-Quellbasis).

## Abstimmungs-Ergebnis (2026-10-26)

**Fixiert für Phase 4a/5-Vorarbeit:** **K3 + K6** (Analyse-First, L0) und **K1 + K2** (Parser-Gaps
in rea, L0). **Zurückgestellt:** K4 (WPBT/GDA-Korrektur, L3), K5 (AGESA-Spur, Beobachtung), K7.
Das Kandidaten-Differential läuft ab sofort mit **vierter Release**: FId (neueste, 2026-08-18,
`images/reference/`, sha256 `38784c23…`) ergänzt FG/FH/FIb — K3/K6-Fenster werden mit FId als
vierten Datenpunkt verifiziert.

## K6-Ergebnis (Phase 4a-2, 2026-10-26 — Analyse erledigt)

`414d94ad` decodiert über 4 Releases (Struktur A, details `differential.md` §6): Subtyp-5A88641B-
Payload = **AMI-Aptio-signed-capsule + WIN_CERTIFICATE (RSA2048/SHA256; GUIDs `4a3ca68b`
APTIO_SIGNED_CAPSULE_GUID / `a7717414` / `51aa59de`) + lückenlose ROM-Area-Tabelle (17 Einträge
à 24 B, ganzer Chip, alle Versionen identisch)**. 256-B-PubKey über alle Releases konstant
(PubKey1 == PubKey2); je Release ändern sich **ausschließlich Sig1 (0x148..0x248) + Sig2
(0x358..0x458)** — Rest 0 geänderte Bytes. TT aufgelöst: kein unbekannter Blob mehr, sondern
Secure-Flash-Verifikationszertifikat (C: modierte flashes → „Secure Flash check fail").
**Konsequenz: K6-Fenster bleibt Korrektur-Tabu (L4-Äquivalent)** — Signaturerneuerung ohne
Private Key unmöglich; Phase 5 muss zusätzlich klären (D-offen), ob Content-Edits im
RomLayout-Umfang (ganzer Chip) von derselben Prüfung erfasst werden.

## K3-Ergebnis (Phase 4a-3, 2026-10-26 — Analyse erledigt)

`cef5b9a3` = **AMI-StdDefaults-NVRAM-Store** (Factory-Defaults): 11 Variablen-Kette
(`Setup 0x293 B · PlatformLang · AMITSESetup · XhciDID · GcSensorVarName · PCI_COMMON ·
SioSetupData · UsbSupport · NetworkStackVar · SecureBootSetup · Setup²`), Struktur
{u32 Blocklänge · `NVRAM` · u16 Size · Attr 0x83FFFFFF · State · Name · Daten} (details
`differential.md` §7). **Falsifikator ausgeführt:** die 415 B sind **keine Padding-/Ausrichtungs-
Artefakte** — Shift-Check (A): FG ohne Byte 0x297 vs FH → nur 2 verbleibende Diffs (beide
Längenfelder). TT **bestätigt**: Gigabyte löschte FG→FH **exakt einen Default-Wert 0x0F (15)**
aus dem großen `Setup`-Entry (Datenoffset 0x273, Liste `0F 0F 0F` → `0F 0F`) und zog die zwei
Längenfelder (u32@0 0x725→0x724, Setup-Size 0x294→0x293) nach; FH/FIb/FId unverändert.
**Offen (D):** Benennung des Schalters (`Setup`-Datenoffset 0x273 → IFR-Frage) braucht den
Setup-Treiber aus dem DXE-Layer — Vorschlag für Phase 5, nicht Teil des fixierten Scopes.

### K3-Ergebnis — Schalter benannt (Phase-5 P-2, 2026-10-27 — A)

Der gelöschte Default `0x0F` = Factory-Default der **doppelten IOMMU-Frage**: FG Setup-Varstore
(EC87D643-…) trägt zwei IOMMU-Steuerungen auf zwei getrennten Slots — qid `0x01a6` @Varoffset
`0x025F` (Optionswerte 00/01/FF, auf 2 Forms gepostet: auch qid `0x0251`) und qid `0x01a7`
@Varoffset `0x0271` (Prompt/Help sid `0x052b`/`0x052c` = „IOMMU"/„Enable/Disable IOMMU
Support", Optionen Auto=`0x0F`/Disabled=`0x00`/Enabled=`0x01`) — derselben AGESA-Funktion zwei
Setup-Bytes = Vendor-/AMI-Autoriserungs-Duplizierung, nicht AGESA. FH löscht die zweite Instanz
komplett (−1 Frage, Forms-Paket −60 B→0xA50F, Setup-Varstore 0x283→0x282, alle Varoffsets>0x271
und qids>0x01a7 −1, String-Pool unverändert 3327); FIb/FId übernehmen FH. NVRAM↔IFR-Koordination:
Setup-Daten des StdDefaults = IFR-Varstore-Layout 1:1 (**Datenoffset = Varoffset, Basis 0**),
verifiziert über IG-Post (Std-Default `0x0F` @0x271 in FH/FId), UMA-Mode (`0x0F` @0x272), UMA-FB
(`FFFFFFFF` u32 @0x273..). Byte-genau liegt das Loch in der FG-Dreier-Reihe `0x271/272/273`
(§7's „0x273" = gültiges Run-Mitglied); semantisch eindeutig = **Slot `0x0271`** (IOMMU#2);
dort stand `0x0F` = dessen Auto-Factory. Details + Vier-Release-Matrix: `differential.md` §7.1
(Alle-Datenpunkte inkl. FId, FId-IFR = FH-Fund — FId-PE nur Bump +160 B, Pool +2 Strings,
IOMMU-sid 0x052d).
**Korrektur-Relevanz:** L2 mit Doppel-Nachzug (Blocklänge + Entry-Size) + IFR-Konsistenz.

## K1-Ergebnis (Phase 4a-4, 2026-10-26 — Parser-Fix erledigt)

rea-Parser-Fix umgesetzt (`UefiImageScan.ts`, `walkSectionChain`): RAW-FFS-Bodies mit leerer oder
nur-Bogus-Section-Kette werden einmal auf eingebettete FVs geprüft (`scanVolumesInRegion`, depth+1,
`/embedded`-Pfad); Zulassung unverändert über Alignment/FvLength/Header-Checksumme/Blockmap + Budgets,
kein Schema-/Katalog-Änderung. **Falsifikator erfüllt (A):** nach Fix meldet `inspect_uefi_firmware`
auf FId **10/10** Volumes, inkl. `…/FFS:05ca020b…/embedded/FV@0x9300c0` (0x20000, depth 1, parent
0x92f000, sha256 `c2dd2665…`); Bogus-Zero-Length-Section-Record beseitigt; FV-Inhalt erstmals
walkbar (pad + freeform `7bb28b99-…` 26 767 B mit **LZMA-custom-Section `ee4e5898`**, 26 719 B
komprimierter Stream). Tests: 2 neue Fixture-Tests (positives 0x9300c0-Muster/Negativ:
unframed-body bleibt unverändert), uefi+acceptance 43/43, Coverage bleibt `complete`.
**Residual:** Extractor-Selektoren (`--volume-offset/--file-offset`) verwenden einen Depth-0-Index
und lehnen das neue FV noch ab → Phase-5-Extraktion über Dekoder-Lane; cartography-Snapshots
(9 FVs) bleiben als Pre-Fix-Stand, Nach-Fix-Report `scratches/k1_fid_after.md`.

## K2-Ergebnis (Phase 4a-5, 2026-10-26 — Dekompressor identifiziert, Parser-Fix erledigt)

`ce3233f5-2cd6-4d87-9152-4a238bb6d1c4` = **EFI_GUIDED_SECTION_ZLIB_AMD** (UEFITool `ffs.h:451`).
Der Scan-Befund „LZMA-alone-artig, Dekodierung scheitert" war ein Interpretationsfehler: hinter dem
GUID-Header (data_offset 24) sitzt der **EFI_AMD_ZLIB_SECTION_HEADER** (256 B: 0×14 Null,
`CompressedSize` u32 LE @0x14, 0×E8 Null), ab Payload-Offset **0x100** folgt ein zlib-wrapped
Stream (`78 da …`). FId-Ground truth: Section @0xe41fe8, CompressedSize 1 020 840 == Stream exakt,
Decode → 3 932 192 B = RAW+FVI+**PEI-FV** (FvLength 0x3C0000), FV-Angel 0xe41fe8+0x18+0x20 =
0xe42020. **rea-Fix (L0):** kind `ami-zlib` + Scan-Lane `format:"zlib"` mit 0×100-Peel + Provider
node:zlib (Budget-gebunden, Handler `node-zlib@…`), Extraktion `decompressed-zlib`; Schema-Enums +
MCP-Katalog regeneriert. **Falsifikator erfüllt (A):** FId 11/11 Volumes inkl.
`…/section[0]/zlib/FV@0xe42020`; PeiCore `52c05b14` + PeiM-Inventar erstmals gemappt;
Extraktion `--file-offset 0xe41fd0` liefert `.decoded.bin` 3 932 192 B mit sha256 == Hand-Dekodier
(d9a7e8dc…), handler node-zlib@1.3.2, 0 Gaps. Tests 46/46 (+3). TT aufgelöst: PEI-Phase ist im
rea-Modell; kein „unbekannter Dekompressor" mehr. Residual: 4 konservative `_FVH`-false-positives
im dekodierten Stream (Observation).

## Phase-5-Kandidaten K8+ (2026-10-27 — Dekompilierungs-Beleg P-1 SecSMIFlash 3370a4bd, registriert vor Messung)

Kontext: `differential.md` §8 (P-1-Kette, RomLayout-Tabelle, Gate/FALSE-Arme). Kandidatespaltenschema
wie K1–K7 (Quelle/Grad, TT, EE, Modul/Bytes, Level, Aufwand).

**K8 — Secure-Flash-Hash-Scope verhindert L2/L3 im gecoverten Bereich.**
Quelle/Grad: **A** (Ghidra-Dekompilierung 0x2cd8 + python-geparste RomLayout im shipped-ROM-Capsule;
`differential.md` §8.2). TT: Jeder Content-Edit in einer `flag&0x200`-Region (DXE-Haupt-FV
[0x87000,0x92f000), Content-FV [0x9500c0,0xe3f000), PSP `_PT_` [0x90f000,0x92f000), …) wird beim
nächsten Secure-Flash-Flow (Cmd 2/4/8 → 0x2cd8/0x321c) als Hash-Verstoß entdeckt — Re-Flash-Update
bricht ab bzw. verweigert ($BAD-Pfad → 0x…19); zusätzlich bleibt der Edit beim **normalen
QFlash-Tool-Reflash** nur deshalb unsichtbar, weil QFlash das ganze Chip-Image überschreibt
(Original-Release-Image hat korrekte Hashes) — d. h. der Edit überlebt keinen offiziellen
Reflash-Cycle. EE (preregistriert, statisch + Sandbox): (a) Statisch — die 0x200-Selektion in
0x2cd8 und die Regionliste §8.2 sind Byte-Belegt; ein Test-Edit in [0xa00000,0xa00020) (Covert-) mit
unverändertem 414d94ad-Capsule müsste in der ML4/coreboot-Sandbox eine Verify-Fail-Spur zeigen
(SMI-Cmd 4 mit dem Original-Capsule). (b) Falsifikation des TT-Kerns: wenn die Prüfung nur bei
NVRAM-getriggertem Secure-Update greift und normale Boots NICHT verifizieren (kein PEI-Call-Pfad
gefunden), wäre der L2-Edit trotzdem dauerhaft „unsichtbar" — dann schwächt sich die TT zu
„Update-Nachweisbar" (nicht Boot-Abbruch). **Level:** K6-Tabu-Verlängerung (keine Korrektur-Lane
vorgesehen; dokumentiert). Aufwand: 0 (Analyse-Ergebnis).

**K9 — Flash-Hook-Gate erlaubt Write in hash-freie Löcher und scannt auf Capsule-Schmuggel.**
Quelle/Grad: **A** (Ghidra 0x2024/0x2b84 + Objdump 0x21c8/0x2148/0x2188). TT: Das
Flash-Device-Protokoll (GUID@0x6010) hat gehookte Write-Pfade; erlaubt sind ohne Layout-Gate nur
Regionen mit Allow-Bit-4 (im shipped-Image: DAT_61a0/61a1 = 0x07 je ⇒ 0x400-Regionen default
zugelassen); hash-freie Löcher ([0x9300c0,0x9500c0), [0x77000,0x87000), [0,0x37000),
[0xe3f000,0xe40000)) sind **dauerhaft schreibbar** ohne Capsule-Verifizierung (bzw. via Bypass-
States 0x12/0x20), aber jeder Schreib-Puffer wird ±4 KB auf frisches Capsule gescannt (Anti-
Smuggling). TT-Hypothese: der 128-KB-Loch-FV (K1-FV@0x9300c0) ist exakt deshalb hash-frei, weil er
Vendor-/NV-Daten trägt, die AMI bei jedem Update umschreibt. EE: statisch (Beleg liegt vor);
Sandbox-Messung der 0x2024-Rückwerte bei Schreib-Fenster in Covert-Bereichen. **Level:** Analyse/
Observation — Korrektur-Potenzial: die Löcher sind die **einzigen dokumentierten schreibbaren
L2-Nischen** (mit Anti-Smuggel-Ausschluss). Aufwand: niedrig.

**K10 — Anti-Rollback-Floor 9.04 begrenzt die Rollback-Richtung.**
Quelle/Grad: **A** (Ghidra 0x2900; Konstante 0x388 = 904). TT: Secure-Flash verweigert Updates
mit Version < 9.04 (v1*100+v2-Formel @0x2900) — für das Korrektur-Ritual (plan §5.5) heißt das:
ein Rollback auf eine Release-Version unter der Schwelle schafft der NVRAM-/Capsule-Fluss nicht;
der Weg führt über QFlash-ISP (Chip-Umschreibung). Welche Releases unter der Schwelle liegen,
bleibt offen — je-Version aus dem je-Release-$FID-Block (3fd1d3a2) bestimmen, nicht behaupten.
EE: (a) Byte-Beleg liegt (0x2900, Konstante 0x388); (b) Sandbox: Cmd 2 mit Version-String unter
904 muss 0x…19 produzieren, „≥ 904" nicht — **preregistriert, nicht gemessen.** **Level:**
Analyse — betrifft Ritual-Design (keine BIOS-Korrektur). Aufwand: 0.

## K4-Ergebnis (Phase 5 P-3, 2026-10-27 — Analyse erledigt; Details `differential.md` §9)

Der WPBT-Builder ist ein eigenes Modul — **WpbtDxe `0996199f-2ce2-4d97-830b-077a7b28588a`**
(DXE-Layer; die K4-EE-Referenz „WPBT-Code-Ref @Layer-0x525905" ist dessen ASCII-String, kein
aeb1671d-Code). Vollständig dekompiliert (FIb/FId-PE byte-identisch, 2 752 B): Entry →
CreateEventEx(**gEfiEventReadyToBootGuid**) → je Boot einmalig →
GetVariable(**„Setup"**, EC87D643-…-Varstore, volle Variablen-Größe — FG 0x283 / FH+ 0x282;
**das FG↔FH-Delta des PEs ist exakt dieses DataSize-Immediate** 0x83→0x82 @0x4bc — der
WpbtDxe-Rebuild zwischen FG und FH = Anpassung an die Varstore-Schrumpfung durch die
IOMMU#2-Entfernung §7.1) → **Gate `SetupData[0x264] == 0` ⇒ EFI_UNSUPPORTED, keine WPBT-
Tabelle** → sonst FV2→Read(**aeb1671d**, PE32-Section) → WPBT-Kopf (Sig „WPBT", Rev 1,
Length 0x34, OemId „ALASKA", OemTableId „A M I", CreatorId „GBT ", CreatorRev 0x25021100)
+ EXE-Copy @Base+0x34 (ImageSize @+0x24, ImageAddress @+0x28) → InstallAcpiTable
(EfiACPIReclaimMemory).

**Gate-Frage benannt (A):** qid `0x019c`, ONE_OF **„APP Center Download & Install"**,
Optionen Disabled=`00`/Enabled=`01`, **IFR-Default = Enabled (0x01)**, kein
Suppress/Disable/Gray am Frage-Knoten (sichtbare Setup-Option), NVRAM-Factory
Setup[0x264] = `01` (FG/FH/FId gemessen; FIb per §7 FH-identisch) — unverändert über alle
vier Releases.

**Level-Neubewertung (L3 → L0/L1):** der Injektionspfad liegt hinter einem Setup-Schalter.
- **L0:** Setup-Option „APP Center Download & Install" auf Disabled → `Setup[0x264] = 0` ⇒
  EFI_UNSUPPORTED ⇒ keine WPBT-Tabelle ab dem nächsten Boot (kein Image-Eingriff).
- **L1:** StdDefaults-Byte 0x264 in `cef5b9a3` 01→00 (Einzelbyte; Byte < 0x271 ⇒ keine der
  §7-Längen-/Shift-Nachzüge betroffen; IFR-Default-Record bleibt 01 — Kosmetik-Diskrepanz,
  nicht funktional).
- **L3** (WpbtDxe/aeb1671d-Entfernung) nur noch nötig, wenn die Tabelle grundsätzlich nie
  existieren darf — und ein solcher Edit läge ohnehin im K8-Hash-Scope (secure-flash-gefährdet).

**Verfeinerter EE (bleibt prä-registriert):** WPBT-Tabellen-Nachweis auf dem Board — Windows
`GetSystemFirmwareTable("WPBT")` / Task-Manager-Sichtbarkeit des GDA-Programms; dieselbe
Messung entscheidet die §9-NULL-Read-Beobachtung (statisch: inlined StrLen16-Tail liest
word @R14=0; das Args-Feld wird nie geschrieben — FUN_6e0-NULL-Guard): entweder läuft der
Zweig auf echter Hardware (Tabellen-Nachweis + Verhalten beobachtbar) oder er ist tot.
Nebenbefund (A): 8-fach-Multi-Post-Familie qids 0x2821–0x2828 @vo 0x263 „Output Select" —
AMI-Duplizier-Muster wie IOMMU#2 (§7.1). Keine Korrektur ohne 5.4-Abstimmung.