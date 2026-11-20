# Differential: FG ↔ FH ↔ FIb ↔ FId (B550 AORUS Elite V2)

Quellen: roher Byte-Diff über die 16-MiB-Images + rea-Kartografie (`cartography/{fg,fh,fib}.json`). GUID-Struktur: siehe Cross-Check (`findings/crosscheck.md`) —
die UEFIExtract-`guids.csv` aller drei Versionen ist byte-identisch.

## 1. Strukturvergleich (Depth-0-FFS per GUID, aus rea-JSON)

File-Anzahl (Depth-0): FG=23, FH=23, FIb=23

| Änderung | FV | GUID | Typ | Größe |
|---|---|---|---|---|
| Größenänderung FG→FH | FV@92f000 | 84366c9e-cd61-4b6e-8bc7-384541382842 | firmware-volume-image | 41826 → 41831 (+5 B) |
| Größenänderung FG→FH | FV@92f000 | 1df36ff9-c7ea-47a3-bd5b-426c250db776 | firmware-volume-image | 77644 → 77651 (+7 B) |
| Größenänderung FG→FH | FV@92f000 | 9e21fd93-9c72-4c15-8c4b-e77f1db2d792 | firmware-volume-image | 4219057 → 4218909 (-148 B) |
| Größenänderung FG→FH | FV@e40000 | 3e3b6dc0-064d-4b01-9203-7836c9b498e7 | firmware-volume-image | 1020853 → 1020898 (+45 B) |
| Größenänderung FG→FIb | FV@92f000 | 84366c9e-cd61-4b6e-8bc7-384541382842 | firmware-volume-image | 41826 → 41820 (-6 B) |
| Größenänderung FG→FIb | FV@92f000 | c0492c7f-75e2-487c-b2dd-000e6cf7b905 | firmware-volume-image | 723600 → 723629 (+29 B) |
| Größenänderung FG→FIb | FV@92f000 | 1df36ff9-c7ea-47a3-bd5b-426c250db776 | firmware-volume-image | 77644 → 77651 (+7 B) |
| Größenänderung FG→FIb | FV@92f000 | 9e21fd93-9c72-4c15-8c4b-e77f1db2d792 | firmware-volume-image | 4219057 → 3913887 (-305170 B) |
| Größenänderung FG→FIb | FV@e40000 | 3e3b6dc0-064d-4b01-9203-7836c9b498e7 | firmware-volume-image | 1020853 → 1020813 (-40 B) |
| Größenänderung FH→FIb | FV@92f000 | 84366c9e-cd61-4b6e-8bc7-384541382842 | firmware-volume-image | 41831 → 41820 (-11 B) |
| Größenänderung FH→FIb | FV@92f000 | c0492c7f-75e2-487c-b2dd-000e6cf7b905 | firmware-volume-image | 723600 → 723629 (+29 B) |
| Größenänderung FH→FIb | FV@92f000 | 9e21fd93-9c72-4c15-8c4b-e77f1db2d792 | firmware-volume-image | 4218909 → 3913887 (-305022 B) |
| Größenänderung FH→FIb | FV@e40000 | 3e3b6dc0-064d-4b01-9203-7836c9b498e7 | firmware-volume-image | 1020898 → 1020813 (-85 B) |

## 2. Roh-Byte-Differenzen

### FG ↔ FIb: 96 coalesced ranges, 6295680 B differieren

| range | length | class |
|---|---|---|
| 0x37094 | 0x721 | FV@37000/FFS:cef5b9a3:raw |
| 0x24100c | 0x5 | outside-mapped-volumes |
| 0x24300c | 0x5 | outside-mapped-volumes |
| 0x24500c | 0x5 | outside-mapped-volumes |
| 0x24700c | 0x5 | outside-mapped-volumes |
| 0x3b000c | 0x5 | outside-mapped-volumes |
| 0x3b200c | 0x5 | outside-mapped-volumes |
| 0x3b400c | 0x5 | outside-mapped-volumes |
| 0x3b600c | 0x5 | outside-mapped-volumes |
| 0x3df960 | 0xf44d | outside-mapped-volumes |
| 0x3f0280 | 0x300 | outside-mapped-volumes |
| 0x3f7960 | 0x90 | outside-mapped-volumes |
| 0x405890 | 0x1 | outside-mapped-volumes |
| 0x407ad0 | 0x100 | outside-mapped-volumes |
| 0x449200 | 0x661 | outside-mapped-volumes |
| 0x44bb40 | 0x100 | outside-mapped-volumes |
| 0x450760 | 0x90 | outside-mapped-volumes |
| 0x45a50c | 0x1 | outside-mapped-volumes |
| 0x45d80c | 0x9c | outside-mapped-volumes |
| 0x46a760 | 0x730 | outside-mapped-volumes |
| 0x528fa0 | 0x261 | outside-mapped-volumes |
| 0x52d030 | 0x261 | outside-mapped-volumes |
| 0x535490 | 0x261 | outside-mapped-volumes |
| 0x539860 | 0x261 | outside-mapped-volumes |
| 0x53dab0 | 0x261 | outside-mapped-volumes |
| 0x544570 | 0x261 | outside-mapped-volumes |
| 0x54b120 | 0x2f0 | outside-mapped-volumes |
| 0x54f55b | 0x3d6 | outside-mapped-volumes |
| 0x55a450 | 0x261 | outside-mapped-volumes |
| 0x55f6f0 | 0x261 | outside-mapped-volumes |
| 0x56c5e0 | 0x261 | outside-mapped-volumes |
| 0x56f0f0 | 0x261 | outside-mapped-volumes |
| 0x571f50 | 0x261 | outside-mapped-volumes |
| 0x579460 | 0x261 | outside-mapped-volumes |
| 0x5856a0 | 0x261 | outside-mapped-volumes |
| 0x590840 | 0x261 | outside-mapped-volumes |
| 0x596320 | 0x261 | outside-mapped-volumes |
| 0x59db10 | 0x261 | outside-mapped-volumes |
| 0x5a4900 | 0x261 | outside-mapped-volumes |
| 0x5a76f0 | 0x261 | outside-mapped-volumes |
| 0x5add90 | 0x200 | outside-mapped-volumes |
| 0x5e000c | 0x5 | outside-mapped-volumes |
| 0x5e400c | 0x1005 | outside-mapped-volumes |
| 0x5f400c | 0x5 | outside-mapped-volumes |
| 0x5f800c | 0x1005 | outside-mapped-volumes |
| 0x610460 | 0x10e90 | outside-mapped-volumes |
| 0x6352e8 | 0x1 | outside-mapped-volumes |
| 0x63a470 | 0x100 | outside-mapped-volumes |
| 0x67bb00 | 0x100 | outside-mapped-volumes |
| 0x68bd60 | 0x1 | outside-mapped-volumes |
| 0x68dd00 | 0x100 | outside-mapped-volumes |
| 0x695a60 | 0x90 | outside-mapped-volumes |
| 0x69f210 | 0x1 | outside-mapped-volumes |
| 0x6a46e8 | 0x1 | outside-mapped-volumes |
| 0x6b3a60 | 0x710 | outside-mapped-volumes |
| 0x6b7490 | 0x161 | outside-mapped-volumes |
| 0x6bb470 | 0x161 | outside-mapped-volumes |
| 0x6c0ee0 | 0x161 | outside-mapped-volumes |
| 0x6c4db0 | 0x161 | outside-mapped-volumes |
| 0x6c8790 | 0x161 | outside-mapped-volumes |
| 0x6cf260 | 0x4011 | outside-mapped-volumes |
| 0x6ddb90 | 0x161 | outside-mapped-volumes |
| 0x6e1100 | 0x161 | outside-mapped-volumes |
| 0x6edf90 | 0x161 | outside-mapped-volumes |
| 0x6f4140 | 0x161 | outside-mapped-volumes |
| 0x6ff640 | 0x161 | outside-mapped-volumes |
| 0x7080c0 | 0x161 | outside-mapped-volumes |
| 0x70e720 | 0x161 | outside-mapped-volumes |
| 0x714ca0 | 0x161 | outside-mapped-volumes |
| 0x71a2f0 | 0x161 | outside-mapped-volumes |
| 0x71f0c0 | 0x161 | outside-mapped-volumes |
| 0x724730 | 0x161 | outside-mapped-volumes |
| 0x7278d0 | 0x100 | outside-mapped-volumes |
| 0x73d800 | 0x100 | outside-mapped-volumes |
| 0x77100c | 0x5 | outside-mapped-volumes |
| 0x77500c | 0x1005 | outside-mapped-volumes |
| 0x790460 | 0x10e90 | outside-mapped-volumes |
| 0x7b52e8 | 0x1 | outside-mapped-volumes |
| 0x7ba470 | 0x100 | outside-mapped-volumes |
| 0x80d960 | 0x1 | outside-mapped-volumes |
| 0x80f901 | 0xff | outside-mapped-volumes |
| 0x817a60 | 0x90 | outside-mapped-volumes |
| 0x821210 | 0x1 | outside-mapped-volumes |
| 0x8266e8 | 0x1 | outside-mapped-volumes |
| 0x835a60 | 0x710 | outside-mapped-volumes |
| 0x8b5800 | 0x100 | outside-mapped-volumes |
| 0x8f100c | 0x5 | outside-mapped-volumes |
| 0x8f500c | 0x1005 | outside-mapped-volumes |
| 0x92f1ec | 0x310 | FV@92f000/FFS:414d94ad:freeform |
| 0x951120 | 0x19 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0x952654 | 0x3 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0x95377c | 0x3722 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0x9581e9 | 0x4ccd20 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0xe402c3 | 0x231 | FV@e40000/FFS:3fd1d3a2:freeform |
| 0xe41fe0 | 0x35 | FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) |
| 0xe4bb06 | 0xef87f | FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) |

Aggregation nach Klasse (96 ranges, 6295680 B gesamt):

| class | ranges | bytes |
|---|---|---|
| FV@92f000/FFS:9e21fd93:firmware-volume-image (compressed layer) | 1 | 0x4ccd20 (5033248 B) |
| FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) | 2 | 0xef8b4 (981172 B) |
| outside-mapped-volumes | 87 | 0x4070c (263948 B) |
| FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) | 3 | 0x373e (14142 B) |
| FV@37000/FFS:cef5b9a3:raw | 1 | 0x721 (1825 B) |
| FV@92f000/FFS:414d94ad:freeform | 1 | 0x310 (784 B) |
| FV@e40000/FFS:0dca793a:freeform | 1 | 0x231 (561 B) |

### FG ↔ FH: 27 coalesced ranges, 5303261 B differieren

| range | length | class |
|---|---|---|
| 0x37094 | 0x721 | FV@37000/FFS:cef5b9a3:raw |
| 0x24100c | 0x5 | outside-mapped-volumes |
| 0x24300c | 0x5 | outside-mapped-volumes |
| 0x24500c | 0x5 | outside-mapped-volumes |
| 0x24700c | 0x5 | outside-mapped-volumes |
| 0x3b000c | 0x5 | outside-mapped-volumes |
| 0x3b200c | 0x5 | outside-mapped-volumes |
| 0x3b400c | 0x5 | outside-mapped-volumes |
| 0x3b600c | 0x5 | outside-mapped-volumes |
| 0x5e000c | 0x5 | outside-mapped-volumes |
| 0x5e400c | 0x1005 | outside-mapped-volumes |
| 0x5f400c | 0x5 | outside-mapped-volumes |
| 0x5f800c | 0x1005 | outside-mapped-volumes |
| 0x77100c | 0x5 | outside-mapped-volumes |
| 0x77500c | 0x1005 | outside-mapped-volumes |
| 0x8f100c | 0x5 | outside-mapped-volumes |
| 0x8f500c | 0x1005 | outside-mapped-volumes |
| 0x92f1ec | 0x310 | FV@92f000/FFS:414d94ad:freeform |
| 0x951120 | 0x19 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0x952654 | 0x3 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0x95377c | 0x3722 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0x9581e6 | 0x3291 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0xa0bf18 | 0x19 | FV@92f000/FFS:1df36ff9:firmware-volume-image (compressed layer) |
| 0xa112a7 | 0x413c62 | FV@92f000/FFS:1df36ff9:firmware-volume-image (compressed layer) |
| 0xe402c3 | 0x231 | FV@e40000/FFS:3fd1d3a2:freeform |
| 0xe41fe0 | 0x35 | FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) |
| 0xe4bb06 | 0xef8ac | FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) |

Aggregation nach Klasse (27 ranges, 5303261 B gesamt):

| class | ranges | bytes |
|---|---|---|
| FV@92f000/FFS:9e21fd93:firmware-volume-image (compressed layer) | 1 | 0x413c62 (4275298 B) |
| FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) | 2 | 0xef8e1 (981217 B) |
| FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) | 4 | 0x69cf (27087 B) |
| outside-mapped-volumes | 16 | 0x4050 (16464 B) |
| FV@37000/FFS:cef5b9a3:raw | 1 | 0x721 (1825 B) |
| FV@92f000/FFS:414d94ad:freeform | 1 | 0x310 (784 B) |
| FV@e40000/FFS:0dca793a:freeform | 1 | 0x231 (561 B) |
| FV@92f000/FFS:1df36ff9:firmware-volume-image (compressed layer) | 1 | 0x19 (25 B) |

### FH ↔ FIb: 93 coalesced ranges, 6110871 B differieren

| range | length | class |
|---|---|---|
| 0x24100c | 0x5 | outside-mapped-volumes |
| 0x24300c | 0x5 | outside-mapped-volumes |
| 0x24500c | 0x5 | outside-mapped-volumes |
| 0x24700c | 0x5 | outside-mapped-volumes |
| 0x3b000c | 0x5 | outside-mapped-volumes |
| 0x3b200c | 0x5 | outside-mapped-volumes |
| 0x3b400c | 0x5 | outside-mapped-volumes |
| 0x3b600c | 0x5 | outside-mapped-volumes |
| 0x3df960 | 0xf44d | outside-mapped-volumes |
| 0x3f0280 | 0x300 | outside-mapped-volumes |
| 0x3f7960 | 0x90 | outside-mapped-volumes |
| 0x405890 | 0x1 | outside-mapped-volumes |
| 0x407ad0 | 0x100 | outside-mapped-volumes |
| 0x449200 | 0x661 | outside-mapped-volumes |
| 0x44bb40 | 0x100 | outside-mapped-volumes |
| 0x450760 | 0x90 | outside-mapped-volumes |
| 0x45a50c | 0x1 | outside-mapped-volumes |
| 0x45d80c | 0x9c | outside-mapped-volumes |
| 0x46a760 | 0x730 | outside-mapped-volumes |
| 0x528fa0 | 0x261 | outside-mapped-volumes |
| 0x52d030 | 0x261 | outside-mapped-volumes |
| 0x535490 | 0x261 | outside-mapped-volumes |
| 0x539860 | 0x261 | outside-mapped-volumes |
| 0x53dab0 | 0x261 | outside-mapped-volumes |
| 0x544570 | 0x261 | outside-mapped-volumes |
| 0x54b120 | 0x2f0 | outside-mapped-volumes |
| 0x54f55b | 0x3d6 | outside-mapped-volumes |
| 0x55a450 | 0x261 | outside-mapped-volumes |
| 0x55f6f0 | 0x261 | outside-mapped-volumes |
| 0x56c5e0 | 0x261 | outside-mapped-volumes |
| 0x56f0f0 | 0x261 | outside-mapped-volumes |
| 0x571f50 | 0x261 | outside-mapped-volumes |
| 0x579460 | 0x261 | outside-mapped-volumes |
| 0x5856a0 | 0x261 | outside-mapped-volumes |
| 0x590840 | 0x261 | outside-mapped-volumes |
| 0x596320 | 0x261 | outside-mapped-volumes |
| 0x59db10 | 0x261 | outside-mapped-volumes |
| 0x5a4900 | 0x261 | outside-mapped-volumes |
| 0x5a76f0 | 0x261 | outside-mapped-volumes |
| 0x5add90 | 0x200 | outside-mapped-volumes |
| 0x5e000c | 0x5 | outside-mapped-volumes |
| 0x5e400c | 0x1005 | outside-mapped-volumes |
| 0x5f400c | 0x5 | outside-mapped-volumes |
| 0x5f800c | 0x1005 | outside-mapped-volumes |
| 0x610460 | 0x10e90 | outside-mapped-volumes |
| 0x6352e8 | 0x1 | outside-mapped-volumes |
| 0x63a470 | 0x100 | outside-mapped-volumes |
| 0x67bb00 | 0x100 | outside-mapped-volumes |
| 0x68bd60 | 0x1 | outside-mapped-volumes |
| 0x68dd00 | 0x100 | outside-mapped-volumes |
| 0x695a60 | 0x90 | outside-mapped-volumes |
| 0x69f210 | 0x1 | outside-mapped-volumes |
| 0x6a46e8 | 0x1 | outside-mapped-volumes |
| 0x6b3a60 | 0x710 | outside-mapped-volumes |
| 0x6b7490 | 0x161 | outside-mapped-volumes |
| 0x6bb470 | 0x161 | outside-mapped-volumes |
| 0x6c0ee0 | 0x161 | outside-mapped-volumes |
| 0x6c4db0 | 0x161 | outside-mapped-volumes |
| 0x6c8790 | 0x161 | outside-mapped-volumes |
| 0x6cf260 | 0x4011 | outside-mapped-volumes |
| 0x6ddb90 | 0x161 | outside-mapped-volumes |
| 0x6e1100 | 0x161 | outside-mapped-volumes |
| 0x6edf90 | 0x161 | outside-mapped-volumes |
| 0x6f4140 | 0x161 | outside-mapped-volumes |
| 0x6ff640 | 0x161 | outside-mapped-volumes |
| 0x7080c0 | 0x161 | outside-mapped-volumes |
| 0x70e720 | 0x161 | outside-mapped-volumes |
| 0x714ca0 | 0x161 | outside-mapped-volumes |
| 0x71a2f0 | 0x161 | outside-mapped-volumes |
| 0x71f0c0 | 0x161 | outside-mapped-volumes |
| 0x724730 | 0x161 | outside-mapped-volumes |
| 0x7278d0 | 0x100 | outside-mapped-volumes |
| 0x73d800 | 0x100 | outside-mapped-volumes |
| 0x77100c | 0x5 | outside-mapped-volumes |
| 0x77500c | 0x1005 | outside-mapped-volumes |
| 0x790460 | 0x10e90 | outside-mapped-volumes |
| 0x7b52e8 | 0x1 | outside-mapped-volumes |
| 0x7ba470 | 0x100 | outside-mapped-volumes |
| 0x80d960 | 0x1 | outside-mapped-volumes |
| 0x80f901 | 0xff | outside-mapped-volumes |
| 0x817a60 | 0x90 | outside-mapped-volumes |
| 0x821210 | 0x1 | outside-mapped-volumes |
| 0x8266e8 | 0x1 | outside-mapped-volumes |
| 0x835a60 | 0x710 | outside-mapped-volumes |
| 0x8b5800 | 0x100 | outside-mapped-volumes |
| 0x8f100c | 0x5 | outside-mapped-volumes |
| 0x8f500c | 0x1005 | outside-mapped-volumes |
| 0x92f1ec | 0x310 | FV@92f000/FFS:414d94ad:freeform |
| 0x951120 | 0x19 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0x9581e6 | 0x4ccc97 | FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) |
| 0xe402c3 | 0x231 | FV@e40000/FFS:3fd1d3a2:freeform |
| 0xe41fe0 | 0x35 | FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) |
| 0xe74e4d | 0xc6565 | FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) |

Aggregation nach Klasse (93 ranges, 6110871 B gesamt):

| class | ranges | bytes |
|---|---|---|
| FV@92f000/FFS:9e21fd93:firmware-volume-image (compressed layer) | 1 | 0x4ccc97 (5033111 B) |
| FV@e40000/FFS:3e3b6dc0:firmware-volume-image (compressed layer) | 2 | 0xc659a (812442 B) |
| outside-mapped-volumes | 87 | 0x4070c (263948 B) |
| FV@92f000/FFS:414d94ad:freeform | 1 | 0x310 (784 B) |
| FV@e40000/FFS:0dca793a:freeform | 1 | 0x231 (561 B) |
| FV@92f000/FFS:84366c9e:firmware-volume-image (compressed layer) | 1 | 0x19 (25 B) |

## 3. Interpretation (Grade markiert)

Beobachtet (A — zwei unabhängige Quellen: rea-JSON-Größen + roher Byte-Diff):

1. **Die Differenzen konzentrieren sich auf komprimierte Layer.** Der Großeil (4–5 MB) liegt in
   - `9e21fd93-…` (FVMAIN-Compressed-Layer, 4,22 MB → 3,92 MB in FIb: −305 kB),
   - `3e3b6dc0-…` (PEI-Layer, `ce3233f5`, ±45 kB),
   - `84366c9e`, `c0492c7f`, `1df36ff9` (kleinere FVI-Layer, im Bereich 5–29 B).
   Kompression kaskadiert Änderungen — **roher Byte-Diff beweist nicht, welche Module innen geändert
   wurden**; das ist in §4 über die dekodierten Layer je Version aufgelöst (`module_diff.md`/
   `module_inspect.md`).
2. **Konstant über FG↔HF geänderte kleine RAW-Inhalte** (Phase-4-Anker; A — exakte Positionsanalyse):
   - `FV@37000/FFS:cef5b9a3` (raw = Setup-Defaults-Variables-Blob, Strings ‚StdDefaults/AMITSESetup/
     SecureBootSetup/…'): **415 exakte Bytes** ändern sich FG→FH (identisch FG→FIb; FH→FIb **0**) — die
     Default-Werte, nicht die Namen, ändern sich zwischen FG und FH/FIb.
   - `FV@92f000/FFS:56e14f88` (freeform, Payload 1104 B): enthält `8ARNR302{FG,FH,FIb}` + „B550 AORUS
     ELITE V2" + „ALASKA AM I" (Version-Block); pro Version ändern sich **3–5 Bytes** @0xe404ed–0xf3 =
     Payload+0x29 — genau der Version-Suffix. **(0dca793a selbst ändert sich nicht** — die 561-B-Diff-
     Tabelle oben ist ein Coalesce-Hull, der die sparsamen Bytes @0xe404ed… und den File-Kopf von
     `0dca793a` in eine Range zusammenfasst; Midpoint-Klassifikation fiel versehentlich auf 0dca793a.)
   - `FV@92f000/FFS:414d94ad` (komprimiert, 511 geänderte Bytes im Blob FG→FH).
3. **~264 kB außerhalb der gemappten Volumes ändern sich nur FG/FH ↔ FIb** (87 ranges) — das ist der
   PSP-Dateibereich (Mikrocode/PMU/AGESA-Blobs) + PSP-Tabelle; FG↔FH nur ~16 kB. Passt zur Erwartung:
   FIb bringt einen AGESA/PSP-Update-Schub, FG↔FH ein kleineres Update. → Phase-4-Kandidat
   „Mikrocode-/PMU-Region-Version" (Bereich 0x57000–0x92f000, PSP-Tabellenstruktur via `$PSP`).
4. **Größenprofile:** `9e21fd93` FG 4 219 057 → FH 4 218 909 → FIb 3 913 887 B — FIb hält −305 kB am
   komprimierten Layer — die einzige große Größenänderung; **in §4.2 aufgelöst: aeb1671d-Rebuild (GDA).**
   23 FFS-Files (Depth-0) bleiben identisch in Anzahl und Reihenfolge über alle Versionen — nur Größen
   von 5 FVIs ändern sich. Struktur stabil ⇒ Differential-Disziplin „Byte-Ebene, nicht GUID-Ebene".

Nächste Verfeinerung (Phase 4): Release-Notes/Strings in `cef5b9a3`/`56e14f88` je Version auswerten;
die Modul-Granularität der komprimierten Layer ist jetzt bewiesen (§4). **Messmethoden-Notiz:** die
Diff-Tabellen oben sind Coalesce-Hulls über 4-KiB-Gap-Merge; die „bytes"-Spalte der Aggregation misst
Hull-Größe, nicht geänderte Positionsanzahl (exakt gezählt für `cef5b9a3`: 415, `414d94ad`: 511,
`56e14f88`: 3–5).

## 4. Modulebene — Auflösung der komprimierten Layer (2026-10-26)

Methodik: je Version den EE4E5898-LZMA-Block der `9e21fd93`-FVI dekodieren; Module über GUID-Signatur +
Sektionskopf-Validierung lokalisieren (⚠ die DXE-Apriori-Liste enthält jeden Modul-GUID — nacktes
`layer.find(guid)` liefert falsche erste Treffer); dekodierte Bodies + FFS-Shas je Paar verglichen.
Zeilendaten: `findings/module_diff.md` (Join depth+parent_offset+GUID+Ordinal, Layer-Längen-Tabelle),
`findings/module_inspect.md`; Scratches `diff_modules.py`/`module_inspect.py`/`body_delta.py`.

### Layer-Basis (A)
- dekodierte DXE-Layer: FG/FH **13 484 048 B (0xCD_C010)** · FIb **13 185 040 B (0xC93_010)**
  (Δ **−299 008 B**; komprimierte FVI-FFS: 4 219 057 → 3 913 887 = **−305 170 B**, §1).
- Layer-Layout: RAW-Section (12 B) + FVI-Section (4 B) + FV ab Offset 0x10. Depth-1-Offsets sind
  virtuelle Dekompressionsraum-Offsets (FV-Basis 0xa1ee98/0xa1eea0/0xa1eeb8 + within-layer).
- **FvNameGuid-Korrektur:** UEFIExtracts Zeile „`00CDC000 00C93000 … 5C60F367-A505-…`" nennt den
  **FvNameGuid** des DXE-Layer-FV, nicht die File-System-GUID (FS-GUID bleibt `8c8ce578-…` in allen
  drei Versionen). Frühere Notiz „FS-GUID 5c60f367" ist zurückgenommen.
- Modul-Inventar: **518 gemeinsame Module je Paar; 0 neu, 0 entfernt**; FFS-sha geändert:
  FG↔FH 97 · FG↔FIb 122 · FH↔FIb 55.

### Die −305 kB sind ein Modul: aeb1671d = „Gigabyte Download Assistant" (WPBT) — (A, dekodiert)

| | FG/FH | FIb |
|---|---|---|
| dekodierter PE | 906 584 B | 595 944 B (−310 640 B) |
| PE-mktimestamp | 2023-06-02 07:01 | 2026-03-16 03:10 |
| größte Sektion .rdata | 0xD_7050 | 0x8_B360 |
| FFS (komprimiert) | 712 518 B | 409 471 B (**−303 047 B**) |

- Identität (Strings): PDB-Pfad `…WPBT-ALL\WPBT\WPBT\GigabyteDownloadAssistant\obj\Release\…\.pdb` +
  .NET/mscorlib/Windows-Forms → Windows-.NET-EXE, per **WPBT** (Windows Platform Binary Table) ins OS
  gelegt.
- FG↔FH **byte-identisch** (0/222 4k-Blöcke; FFS-Sha identisch — deshalb nicht im FG↔FH-Changed-Raster).
  FH→FIb Total-Rebuild (146/146 Blöcke, 600 Strings nur in FIb).
- Bilanz der −305 170 B: −303 047 (GDA) + 1 825 (fbf95065-Certs) + 1 504 (76d5cf91-OA3) + 630
  (SSDT) + 0 (414d94ad, 3fd1d3a2) ≈ −299 088; Rest ≈ −6 kB über ~95 kleine Modul-Änderungen
  (±32/64-B-Alignment-Schritte). **Die größte Release-Änderung ist der GDA-Rebuild, kein
  Treiberentzug.**

### Weitere identifizierte Content-Änderungen (A — dekodierte Bodies; (E) = nur Struktur-Schlüsse)

| Modul | Identität | FG ↔ FH | FH ↔ FIb |
|---|---|---|---|
| `fbf95065` | Microsoft-Zertifikat-Bundle: EFI_TIME-Kopf 2024-01-25 10:07:15 → 2026-03-09 16:02:40; nur-FIb-Strings „Microsoft Option ROM UEFI CA 2023", „Microsoft RSA Devices Root CA 2021", CRL/CRT-URLs, Notbefore/NotAfter 2306/2310 + 3806/3810 | identisch (0/2 Blöcke) | +2 995 B dekodiert / +1 825 B komprimiert |
| `76d5cf91` (OA3) | OA3-Attestation-Treiber (native, mktimestamp 0): PE 2 496 → 4 000 B, `.text` 0x553 → 0xA53 | identisch (0/1) | +1 504 B, 1 682 Bytes @0xD5..0x9BF |
| `deadbeef` | ACPI **SSDT** (OEM-ID `GBT`, Table-ID `GSWApp`, rev 2, AML) | **2 Bytes** (+0x9 = ACPI-Checksumme, +0x10F5 AML) | Rebuild +630 B (nur-FIb-AML-String „20251215") |
| `414d94ad` | opaker Blob; Section FREEFORM_SUBTYPE_GUID **5A88641B-BBB9-4AA6-80F7-498AE407C31F** (depth-0, FFS @0x92f078, Daten 4 096 B, keine lesbaren Strings) | 511 Bytes @0x158..0x467 | 509 Bytes @0x158..0x467 |
| `3fd1d3a2` | „$FID"-Release-Metadaten („8ARNR302", „ALASKA AM I", EFI_TIME je Release: 2025-09-26 · 2025-10-28 · 2026-04-14) | Größe konstant, Date-Block geändert | ebenso |

(E)-Notizen: `5A88641B-…` ist kein PI-Spec-GUID (AMI-spezifisch), Nutzungsfunktion unbestimmt — das
Fenster 0x158..0x467 ändert sich je Release (Phase-4-Frage). `fbf95065` = plausible Secure-Boot-DB-/
Option-ROM-Zertifikatsrolle; Endverwendung nur über Strings belegt.


## 5. Differential erweitert um FId (2026-10-26) — A, aus scratches/diff_modules.py + agesa_scan.py

Korpus: FG `36c9a32a…` · FH `363e0fc9…` · FIb `d6ce0901…` · FId `38784c23…` (Zip 2026-08-18).
Modul-Ebene (module_diff.md): **518 gemeinsame Module je Paar, 0 neu, 0 entfernt**; FFS-sha geändert
FG↔FH **97** · FH↔FIb **55** · FIb↔FId **40** (Fallreihe: jeder Release berührt weniger Module als der
vorige).

### FIb ↔ FId — die 40 geänderten Module (Größenbewegung)

| Modul | Typ | Δ (FFS-Länge) | Bemerkung |
|---|---|---|---|
| `d9fd094f` (R) | driver | **+20 224 B** | dominant: 151 110 → 171 334 B @layer 0x109f1d0 |
| `601f27e3` | freeform | **+2 048 B** | 55 340 → 57 388 B @layer 0x1565de8 |
| `f80697e9` (S) | driver | +192 B | 39 974 → 40 166 B |
| `ba28936b` (S) | driver | +288 B | 7 914 → 8 202 B |
| `b7246c46` (C) | driver | +96 B | 21 918 → 22 014 B |
| `15e4c005` (S) | driver | +128 B | 42 546 → 42 674 B |
| `899407d7` (S) | driver | +160 B | 1 329 658 → 1 329 818 B |
| `8835d63e` (G) | driver | +32 B | 144 378 → 144 410 B |
| `8f4b8f82` (B) | driver | +64 B | 92 050 → 92 114 B |
| `3f79bee2` (P) | driver | +64 B | 3 606 → 3 670 B |
| `d20d5c9f` (Q) | driver | +128 B | 69 634 → 69 762 B |
| `b1da0adf` | driver | **−250 B** | 220 187 → 219 937 B |
| `414d94ad` (d0) | freeform | ±0 B | sha geändert — K6-Fenster 0x158..0x467, **512 B** (FG 511 · FH 509 · FIb 509 · FId 512) |
| `deadbeef` | freeform | ±0 B | dekodiert nur 7 Bytes @0x9..0x7a18 (Checksumme + wenige AML) |
| `3fd1d3a2`, `56e14f88` (d0, e40000) | freeform | 331 B / 164 B-Konst | $FID-/Version-Block je Release |
| `9e21fd93` (d0) | firmware-volume-image | **+9 082 B** komprimiert | dekodierter Layer 13 185 024 → **13 205 504 B (+0x5000)** |
| `84366c9e` (d0) | firmware-volume-image | +3 B | — |
| weitere ~23 | driver/smm | ±0 B | nur sha-Differenz (Timestamp-/Pebble-Rebuild) |

Bilanz: Summe der Depth-1-FFS-Längen-Deltas = **+23 174 B** vs. Layer-Delta **+20 480 B**; Differenz
≈ 2 694 B wird über FFS-Alignment-Padding absorbiert (geometrisch plausibel, nicht byte-genau
verifiziert — (E)). Dominant: `d9fd094f` allein liefert +20 224 B ≈ das gesamte Layer-Wachstum; die
FIb→FId-Freigabe ist im Kern **ein Treiber-Rebuild (`d9fd094f`, Typ R) plus Kleinkorrekturen**, nicht
der GDA-Abbau der FIb-Freigabe (aeb1671d/fbf95065/76d5cf91 dekodiert **byte-identisch** FIb↔FId).

### AGESA-Spur (A, scratches/agesa_scan.py)

| | FG | FH | FIb | FId |
|---|---|---|---|---|
| Layer (dekodiert) | 13 484 048 | 13 484 048 | 13 185 040 | 13 205 520 B |
| `AGESA Version : ComboAm4v2PI %s` (utf16) | 0x34c63c | 0x34c63c | 0x34c78c | 0x34c90c |
| Setup-Literal `1.2.0.{x}` (ascii, je 3 Treffer @ ≈0x27_0000 / 0x30_0000 / 0x34_0000) | `1.2.0.F` | `1.2.0.F` | `1.2.0.11` | **`1.2.0.12`** |
| `Released Date:` (utf16) | 0x69de30 | 0x69db70 | 0x69e1f0 | 0x6a2ac0 |

K5-Falsifikator bestätigt auch für FId: **jede Release hebt AGESA** (1.2.0.F → 1.2.0.11 → 1.2.0.12).

### K3/K6-Verifikation mit FId

- **K3 (`cef5b9a3`, FV@0x37000):** in FH↔FIb **und** FIb↔FId **nicht** im Changed-Raster — identisch
  FG→FH→FIb→FId bis auf den einen FG↔FH-Diff (415 B). TT-Stand unverändert; Decode in Phase-4a
  (K3, Punkt 3 des Plans).
- **K6 (`414d94ad`):** ändert sich in **allen drei Paaren** bei ±0 B Längenänderung, das Fenster
  0x158..0x467 bleibt konstant (jetzt 4 Datenpunkte: 511/509/509/512 geänderte B).


## 6. K6: `414d94ad` decodiert (2026-10-26) — A (Struktur), B (Namensgebung), C (Community-Rolle)

Scratches: `k6_decode.py` · `k6_regions.py` · `k6_repeat.py` · `k6_romlayout.py` · `k6_subwin.py`
(rohe Werte: `session-log.md`). Payload = 4 096 B ab FFS 0x92F078 + 44 B Header (FFS 24 +
Section 20), depth-0, in allen vier Releases (Payload-sha: FG `01bf8faf…` · FH `9785ff5f…` ·
FIb `032e3b13…` · FId `ebf315b5…`).

### Struktur (Offsets im 4-kB-Payload)

| Offset | Inhalt | je Release |
|---|---|---|
| 0x00 | GUID `4a3ca68b-7723-48fb-803d-578cc1fec44d` = **APTIO_SIGNED_CAPSULE_GUID** (UEFITool `common/ffs.h`) | konstant |
| 0x10..0x20 | u16-Kette `0x1000 · 0 · 0 · 1 · 0x1000 · 0x100 · 0x1000 · 0x0E38` (Schema unbestimmt (D); erkennbar: Payloadgröße 0x1000 und **RomLayout-Tabellenanfang 0xE38**) | konstant |
| 0x20 | `WIN_CERTIFICATE` { dwLength 0xE18 · wRevision 0x0200 · wCertificateType 0x0EF1 } — Zertifikatsblock 0x20..0xE38 | konstant |
| 0x28..0x38 | CertType `a7717414-c616-4977-9420-844712a735bf` = EFI_CERT_TYPE_RSA2048_SHA256_GUID | konstant |
| 0x38..0x48 / 0x248..0x258 | HashType `51aa59de-fdf2-4ea3-bc63-875fb7842ee9` (SHA256), je Cert-Item | konstant |
| 0x48..0x148 | PubKey1, 256 B | konstant |
| 0x148..0x248 | Sig1, 256 B | **je Release neu** |
| 0x248..0x258 | HashType (Item 2) | konstant |
| 0x258..0x358 | PubKey2, 256 B — **PubKey1 == PubKey2** | konstant |
| 0x358..0x458 | Sig2, 256 B | **je Release neu** |
| 0x458..0xE38 | 2 528 B Nullen | — |
| 0xE38..0xFD0 | **RomLayout-/ROM-Area-Tabelle**, 17 Einträge à 24 B | konstant |
| 0xFD0..0x1000 | 48 B Padding | — |

dwLength 0xE18 deckt den Zertifikatsblock 0x20..0xE38 (Ende = Tabellenanfang, deckungsgleich).
Subfenster-Test: geändert je Release-Paar **ausschließlich Sig1 + Sig2** (Sig1 255/253/256/256,
Sig2 256 in allen Paaren; Kopf/PubKeys/HashTypes/Padding/RomLayout je 0) — der §5-Fenster-Diff
0x148..0x457 erklärt sich damit vollständig; keine weiteren variablen Felder.

### RomLayout-Tabelle (17 Einträge à 24 B, identisch in allen 4 Releases)

Feldschema: { u32 `0xFF000000 | Offset`, u32 0, u32 Offset, u32 Size, u32 Flag(0|1), u32 AttrTag }.
Die Einträge partitionieren den **gesamten 16-MiB-Chip lückenlos** (max addr+size = 0x1000000):

| # | Offset | Size | Flag | AttrTag | Entsprechung |
|---|---|---|---|---|---|
| 1 | 0xE40314 | 0x1BFCEC | 0 | 0x660A | Chipschwanz bis 0x1000000 |
| 2 | 0xE402E3 | 0x31 | 0 | 0x640A | Sub-Split |
| 3 | 0xE40000 | 0x2E3 | 0 | 0x660A | FV@e40010-Region |
| 4 | 0xE3F000 | 0x1000 | 0 | 0x4008 | FV@e3f010-Region |
| 5 | 0x9500C0 | 0x4EEF40 | 0 | 0x20A | FV@950120..0xE3F000 (FVMAIN) |
| 6 | 0x9300C0 | 0x20000 | 0 | 0xA | ROM-Hole-FV @0x9300C0 |
| 7 | 0x92F000 | 0xA4 | 0 | 0x20A | FV@92F010-Kopf (inkl. 414d94ad-Header) |
| 8 | 0x90F000 | 0x20000 | 1 | 0x6200 | PSP-Region |
| 9 | 0x87000 | 0x888000 | 1 | 0x6200 | PSP-Region (bis 0x90F000) |
| 10 | 0x77000 | 0x10000 | 1 | 0 | PSP-Region |
| 11 | 0x57000 | 0x20000 | 1 | 0x6200 | PSP-Region |
| 12 | 0x37000 | 0x20000 | 0 | 0x6200 | FV@37010 |
| 13 | 0x21000 | 0x16000 | 1 | 0 | — |
| 14 | 0x20000 | 0x1000 | 1 | 0 | — |
| 15 | 0x000000 | 0x20000 | 1 | 0 | Chip-Anfang |
| 16 | 0x9300A4 | 0x1C | 0 | 0x20A | ROM-Hole-Header (@0x9300A8) |
| 17 | 0x92F0A4 | 0x1000 | 0 | 0 | **Dieser Payload selbst** |

AttrTag-Set: { 0x660A · 0x640A · 0x4008 · 0x20A · 0xA · 0x6200 · 0 }. Flag/AttrTag-Semantik
nicht verifiziert (D).

### Interpretation (A: Daten · C: Rolle)

Der Blob ist das **AMI-„Secure Flash"-Verifikationszertifikat** des Images: AMI-Aptio-signed-capsule
header + RSA2048/SHA256-WIN_CERTIFICATE (256-B-PubKey, über alle vier Releases identisch) mit zwei
Key/Sig-Items und der lückenlosen ROM-Area-Tabelle des Chips. Beide Signaturen werden mit jeder
Release neu erzeugt — das je-Release-Delta des Blob ist exakt Sig1+Sig2. Community-Rolle (C,
Win-Raid/Overclock.net zum Subtyp 5A88641B bei AMI-Aptio-B550-Boards): verborgene Secure-Flash-
Prüfung; modierte BIOS-flashes lösen dort „Secure Flash check fail" aus.

**Konsequenz für Phase 5:** das 4-kB-Fenster ist per Schlüssel gebunden → **Korrektur-Tabu**
(L4-Äquivalent: Signaturerneuerung ohne Private Key unmöglich). Offen (D): welcher Verifikator die
Signaturen liest (PSP-Checker vs. DXE-/SMM-Code), und ob Content-Edits außerhalb des Zertifikats
vom Zugehörigkeits-Umfang der Prüfung erfasst werden (RomLayout deckt ja den ganzen Chip).


## 7. K3: `cef5b9a3`-Defaults-Diff decodiert (2026-10-26) — A (Bytes + Einheitstest), A (Benennung P-2, 2026-10-27)

Scratches: `k3_decode.py` (Diff/Hexdump je Run) · `k3_shift.py` (Entry-Kette + Shift-Check).
Section-Data: FV@0x37000 → FFS `cef5b9a3` @0x37078 (raw, 130 952 B) → Section 0x52 (RAW) 4-B-Kopf →
Payload @0x37094, 0x1FF6C = 130 924 B. Payload-sha: FG `f08118a5…` · **FH == FIb == FId `6915b416…`** —
der gesamte FG↔FH-Delta ist 415 B in 43 Runs, alles unterhalb 0x720.

### Struktur der Payload (A, am Blob selbst verifiziert)

- `u32@0`: 0xFFFF0725 (FG) / 0xFFFF0724 (FH+) — Länge des **StdDefaults-Blocks**; dann `FF 83 00`,
  Name `"StdDefaults"`; darunter eine **AMI-NVRAM-Variables-Kette**, je Entry
  {ASCII `NVRAM` · u16 Size · u32 Attr 0x83FFFFFF · u8 State · ASCII-Name NUL · Daten} —
  die Kette summiert exakt auf 0x725 (FG) bzw 0x724 (FH+), Rest des Payloads bis auf die
  letzten 16 B 0xFF (erased).
- 11 Entries (identisch in allen vier Releases): `Setup` (0x293/0x294 B), `PlatformLang` (0x1E,
  `"en-US"`), `AMITSESetup` (0x68), `XhciDID` (0x15), `GcSensorVarName` (0x254), `PCI_COMMON`
  (0x1E, Attr 0x82FFFFFF = NV+BS), `SioSetupData` (0x19), `UsbSupport` (0x47), `NetworkStackVar`
  (0x23), `SecureBootSetup` (0x22), `Setup`² (0x18); danach FF-Füller bis 0x724.
  → Der Blob ist der **AMI-StdDefaults-NVRAM-Store** (Factory-Defaults aller Variablen; die
  „Setup"-Question-Defaults als flaches Feld in IFR-Fragereihenfolge).
- Payload-Schwanz: 16 nicht-FF-Bytes `6f d2 99 45 11 1a b8 49 b9 1f 85 87 45 cf f8 24` @0x1FF5C..
  (Image 0x56FEC..0x56FFB), in **allen vier Releases identisch**, unmittelbar vor Section/FFS-Ende
  @0x57000. Kein bekanntes Magic; vermutlich Teil des Image-Kopier-/Signatur-Umfelds (D, unbenannt).

### Der FG↔FH-Delta ist exakt: 1 gelöschter Default-Wert + 2 Längenfelder (A, Shift-Check)

- Run 0x0000(+1): u32@0 0x725 → 0x724. Run 0x0017(+1): Setup-Size 0x294 → 0x293.
- Run 0x0297(+1): **FG[0x297] = 0x0F gelöscht** (FH: FF-Füller); das Byte liegt im Datenkörper des
  großen `Setup`-Entry (Datenoffset 0x273), Kontext FG `…21 FF 00 01 00 01 0F 0F 0F FF …` →
  FH `…01 0F 0F FF …`.
- **Shift-Check** (`k3_shift.py`): FG mit FG[0x297] entnommen vs FH → **nur 2 Diffs** im gesamten
  Payload (0x0000 und 0x0017, die beiden Längenfelder); die übrigen 16 Abweichungen des Checks
  liegen @0x1FF5B+ und sind Artefakt der eigenen −1-Verschiebung im FF-Meer (roh FG↔FH dort 0).
  Alle übrigen 41 Runs (0x00297..0x0720) sind damit **reine 1-B-Verschiebe-Artefakte** des
  nachfolgenden Entry-Ketten-Shifts — kein weiterer Default-Wert ändert sich.

### Interpretation + Konsequenz

- **TT des Kandidaten bestätigt (nicht widerlegt):** der 415-B-Diff ist **kein Padding** — Gigabyte
  hat zwischen FG und FH **exakt einen Default-Wert 0x0F (15) aus dem „Setup"-Variablen-Defaults
  entfernt** (bzw. die Liste der Dreier-0x0F-Folge von 3 → 2 verkleinert) und die zwei Längsfelder
  nachgezogen. FH/FIb/FId sind seitdem unverändert (der Fix bleibt im Korpus).
- Residual (D, offen): welcher konkrete Setup-Schalter das ist — Zuordnung Byte 0x273 → HII-IFR-
  Frage erfordert Dekodierung des Setup-Treibers (IFR/Formset) aus dem DXE-Layer; aus dem
  Defaults-Blob allein nicht ableitbar (nur Position + Wert 15 + „Liste von 3 → 2").
  → **Aufgelöst durch P-2: §7.1.**

### 7.1 K3-Schalter benannt: doppelte IOMMU-Frage (Phase-5 P-2, 2026-10-27 — A)

Scratch: `k3_q.py` (HII-Package-List-Walk + IFR-Fragen-Extraktion FG/FH/FIb/FId, IFR-Op-Walker in
`k3_ifr.py` nach EDK-II `UefiInternalFormRepresentation.h`) · Ergebnis-JSON `k3_q_{fg,fh,fid}.json`.

**Befund (A, IFR-Formset-Bytes):** FG trägt **zwei getrennte IOMMU-Fragen auf zwei Setup-Varstore-
Slots** — qid `0x01a6` @Varoffset `0x025F` (Optionen Disabled=`00`/Enabled=`01`/Auto=`FF`, auf zwei
Forms gepostet: auch als qid `0x0251`) **und** qid `0x01a7` @Varoffset `0x0271`
(Prompt sid `0x052b` = "IOMMU", Help sid `0x052c` = "Enable/Disable IOMMU Support", Optionen
**Auto=`0x0F`**/Disabled=`0x00`/Enabled=`0x01`) — d. h. derselben AGESA-Funktion wurden zwei
Setup-Bytes zugewiesen; eine davon ist eine Autoriserungs-Duplizierung (AMI/Vendor-Bug-Klasse,
nicht AGESA). FH entfernt die zweite Instanz vollständig; FIb/FId übernehmen den FH-Stand.

**Vier-Release-Matrix (A):**

| | FG | FH | FIb | FId |
|---|---|---|---|---|
| Fragen | 812 | 811 | 811 | 811 |
| IFR-Records | 6679 | 6668 | 6666 | 6666 |
| Forms-Paket len | 0xA54B | 0xA50F | 0xA50B | 0xA50B |
| Setup-Varstore Size | 0x283 | 0x282 | 0x282 | 0x282 |
| IOMMU-Postings | 3 (0x25F×2 + 0x271) | 2 (0x25F) | 2 | 2 |
| en-String-Pool | 3327 | 3327 | 3329 | 3329 |

**NVRAM↔IFR-Mapping gelöst (A):** die Setup-Daten des StdDefaults-Stores sind **byte-genau das
IFR-Varstore-Layout (Datenoffset = Varoffset, Basis 0)** — verifiziert über die verschobenen Slots:
FH/FId `Daten[0x271]` = `0x0F` = der Std-Default der neuen `Integrated Graphics`-Post-Frage (qid
`0x2a2a`, DEFAULT-Record `Value 0x0F`), `Daten[0x272]` = UMA-Mode (Auto), `Daten[0x273..]` = `FF FF
FF FF` = UMA Frame Buffer Size (u32, Factory `FFFFFFFF` = Auto) und `Daten[0x277]` / `Daten[0x278]`
= Display-Res (`FF`) bzw. SATA (`02`) — überall exakt die geparsten IFR-Default-Werte. FG hat an
`0x271..0x273` die Dreier-`0F`-Reihe (IOMMU#2-Auto + IG-Post-Auto + UMA-Mode-Auto).

**Korrektur der §7-Koordinate:** byte-genau liegt der gelöschte 0x0F *irgendwo* in der Dreier-Reihe
FG `0x271/0x272/0x273` (jeder Run-Gleichheits-Split → derselbe Byte-Stream; der Shift-Check mit
Byte `0x297` [= Daten 0x273] ist ein gültiges Loch, aber nicht das einzige). Semantisch eindeutig
ist die Zuordnung über die IFR-Struktur: die entfernte Frage besitzt Slot **Varoffset/Datenoffset
`0x0271`** — dort stand ihr Factory-Default `0x0F` = "Auto". §7's „Datenoffset 0x273" ist als
Run-Mitglied korrekt, als Slot-Eigentümer korrigiert auf `0x271`.

**Strings (A):** der en-Pool ist FG↔FH **identisch** (3327 Strings, sid 0x0c9f = "UMA Mode",
0x0ca4 = "UMA Frame Buffer Size", 0x052b = "IOMMU" in beiden) — AMI behielt die Strings beim
Fragen-Entfernen. FIb/FId wachsen um +2 (3329) bei sids *vor* 0x052b; daraus verschiebt sich
IOMMU auf sid `0x052d` (FId-Pool verifiziert). Nicht-en-Stores je Release = 1-String-Stubs
(x-UEFI-AMI-Muster; Parse-Quirk, ohne Befund-Relevanz).

**Korrektur-Relevanz (unchanged from §7):** L2 mit drei Nachzügen (Store-Länge u32@0, Entry-Size,
IFR-Kette); die konkrete Rekonstruktion wäre: die IOMMU#2-Frage (qid 0x01a7, Varoffset 0x0271 +
Optionen + Hilfe-Text) zurücksetzen und das Setup-Byte wiederherstellen — nur per Abstimmung.
Der umgekehrte Weg (FH-Stand beibehalten) entfällt: FH ist der **Upstream-Fix**, nicht der Bug.
- Phase 5 relevant: jede Korrektur an diesem Store hat drei Nachzüge (Store-Länge, Kette-Size,
  IFR-Konsistenz); Korrektur-Level L2 mit Checksumme/IFR-Kopplung.

## 8. P-1: SecSMIFlash 3370a4bd — Secure-Flash-Prüfstelle + K6-D-Entscheid (2026-10-27) — A (Dekompilierung), B (Design-Deutung)

Modul: `extracted/fid_tree/flash/FV@0x92f000/FFS:9e21fd93…/section[0]/lzma/FV@0xa1eeb8/FFS:3370a4bd-8c23-4565-a2a2-065feede6080/section-0x1277f88.payload.bin`
(23 552 B PE32 x64). Ghidra 12.1.4; VA = FO+0xC00 (.text), VA = FO+0x1A00 (.data); Section-Tabelle
behauptet RawSize=0 (AMI-Muster — Bytes sind vorhanden). Entry RVA 0x1300. Scratches:
`smf_text.bin/dis` (Voll-Disasm), `smf_hooks.dis`, `smf_*.bin`.

### 8.1 Architektur (A — Funktionsmap, VA)

| VA | Rolle |
|---|---|
| 0x27e0 | HandleInit: ST+0x60 = gBS (DAT_6960), ST+0x58 = gRT (DAT_6968); LocateProtocol(&DAT_6290) → Wrapper-Protokoll, [1]-Methode → SMM-System-Table (DAT_6970) |
| 0x241c | Main-Init: AllocatePages(0x1004) → **0x1004000-B Capsule-Staging** (DAT_6910); SmmAllocatePool 0x20000 → **Digest-Tabelle** (DAT_6908, Fill 0xdb, 4096×32-B = exakt 4096 4-KB-Pages); 0x7c-B Write-Descriptor (DAT_6930); SmmLocate(GUID@0x6090) → **Crypto-Protokoll** DAT_6b80 (+0x18 embedded-Key-Load); SmmLocate(GUID@0x6010) → **Flash-Device-Protokoll gehookt: [1]→0x21c8, [2]→0x2148, [3]→0x2188**, Originals nach DAT_6bc8/6bd8/6bc0 (orig[0]→DAT_6bd0, Aufrufstelle 0x2bf0 in 0x2b84); SmmRegister mit Disposition @0x61d0 = {0x1d68, 0x1988, 0x1a1c, 0x321c}; SW-Dispatch-Registrierung (GUID 7739f24c-…) |
| 0x1a1c | SMI-Command-Handler (Cmd-Bytes 1/2/4/8; Allow-Maske 0x61a0/61a1 = je 0x07): 1 → 0x18a4; 2/8 → Capsule in Staging (≤0x1004000, 0x2000000 = Dual-Capsule @+2 MB) → 0x321c (0x…19-Fail für 2|8 toleriert); 4 → zusätzlich per-4-KB-Page-SHA256-Prehash (DAT_6908) + RomLayout-Kopie (DAT_61f8); Ergebnisse in 0x24-B-SMI-Block (State @+0x20, Fail-Flag @+0x1d) |
| 0x321c | VerifySignedCapsule: Capsule-Header (GUID@0x60b0 = 4a3ca68b), ItemOffset/„$BAD"-Marker-Gate (DAT_6bb8) → 0x2e6c + 0x2cd8 (Hash) + 0x3038 (RSA2048/SHA256: PubKey +0x48, Sig1 +0x148, Certs +0x248 à 0x210, Key-Slot = Flag&1+1) + 0x2900/0x29a8 (Version/Rollback) |
| 0x2cd8 | **RomLayout-Hashliste**: Tabelle @Capsule+TblOff, stride 0x18, Offset u32@+8, Size u32@+0xc, Flag u32@+0x14; wählt `Flag & 0x200`-Regionen, prüft Grenzen gegen Image-Size, hängt Capsule-Header (0x38 B) und Tabelle selbst an; Multi-Hash über Crypto-Protokoll (+0x10) |
| 0x21c8/0x2148/0x2188 | Write-Hooks (identisches Wrapper-Pattern, Objdump-Beleg): FUN_2024(Gate); Bestehen ⇒ Original-Methoden-Fallthrough (DAT_6bc8/6bd8/6bc0) |
| 0x2024 | **RomLayout-Zugriffs-Gate** (§8.3) |
| 0x2900 | Anti-Rollback: CompareMem "8ARNR302" + dezimale Versionen; Floor (v1*100+v2) ≥ **0x388 = 904 = Version 9.04** |
| 0x175c | Write-Trigger: Descriptor im 0x7c-Struct füllen → SetVariable("CapsuleUpdateData"-Name @0x65c8, GUID@0x6160, delete, dann Attr 7 / 8-B-Data) — **eigentliche Write-Engine = Boot-Phase (CapsulePei/RomLayout), NVRAM-Handoff** |
| 0x18a4 | Cmd 1: GetVariable("MonotonicCounter" @0x6620, GUID@0x6190) + SetVariable("AmiFlashUpd" @0x6608, GUID@0x61b8, 7, 0x1d, Cmd-Block) = NVRAM-Status-Handshake |
| 0x4574 | FCH-Reset: Fun-Checks, `out 0xb2, 0xbe` (SW-SMI 0xbe = Secure-Flash-Trigger), `out 0xcf9, val` / `out 0xcf9, val|6`, Spin auf DAT_fed803d2&0x40 |

GUID-Konstanten (.data, python-geparst, autoritativ): 0x6010 Flash-Device-Protokoll
(ecb867ab-8df4-492d-8150-a7fd1b9b5a75), 0x6020 = **gEfiHashAlgorithmSha256** (51aa59de-fdf2-4ea3-bc63-875fb7842ee9),
0x6090 Crypto-Protokoll (91abc830-16fc-4d9e-a189-5fc8bb411402), 0x60b0 Capsule-GUID-Konstante
(4a3ca68b-…), 0x6160 "CapsuleUpdateData"-Var-GUID (711c703f-c285-4b10-a3b0-36ecbd3c8be2),
0x61b8 "AmiFlashUpd"-Var-GUID (972431d5-bed4-44d1-8870-ce515cc14d68), 0x61a8 = FFS-GUID **414d94ad**
als Konstante, 0x6210 = 5a88641b-Subtyp, 0x6220 = $FID-Block-GUID (2ebe0275-6458-4af9-91ed-d3f4edb100aa).
UTF-16-Strings: "CapsuleUpdateData" @0x65c8, "AmiFlashUpd" @0x6608, "MonotonicCounter" @0x6620,
"%s%d" @0x65f8 + **Plattform-Codenamen "Taishan"/"Sandstone"/"Huashan"/"Shasta"/"Unknown"** @0x6b70..
(B — plausibel Key-/Modell-Selektion, exakte Referenzstelle noch offen).

### 8.2 K6-D-Entscheid: Hash-Scope (A — Falsifikator ausgeführt, negativer Arm)

ROM-Capsule = 414d94ad-FFS-Körper (`…/FFS:414d94ad…/section-0x92f090.payload.bin`, 4112 B =
16-B-Wrapper-GUID 5a88641b + EFI_CAPSULE_HEADER @+0x10: GUID 4a3ca68b-7723-48fb-803d-578cc1fec44d,
HeaderSize 0x1000, Flags 0x10000, ImageSize 0x1001000, ItemOffset 0x1000, TblOff 0xe38; Cert-Type
a7717414-… = K6-Typ, Hash-Type SHA256) mit RomLayout-Tabelle @Capsule+0xe38 (17 Einträge à 24 B,
2 Null-Slots). **ItemOffset == HeaderSize ⇒ das Item ist das 16-MiB-Flash-Image selbst; alle
Tabellen-Offsets sind CHIP-ABSOLUT.** Geparst (python `struct`, autoritativ):

| idx | Offset | Size | Flag | hash(0x200)? | End |
|---|---|---|---|---|---|
| 0 | 0x00e40314 | 0x001bfcec | 0x660a | JA | 0x1000000 |
| 1 | 0x00e402e3 | 0x31 | 0x640a | nein | 0xe40314 |
| 2 | 0x00e40000 | 0x2e3 | 0x660a | JA | 0xe402e3 |
| 3 | 0x00e3f000 | 0x1000 | 0x4008 | nein | 0xe40000 |
| 4 | 0x009500c0 | 0x004eef40 | 0x020a | JA | 0xe3f000 |
| 5 | 0x009300c0 | 0x00020000 | 0x0000000a | nein | 0x9500c0 |
| 6 | 0x0092f000 | 0xa4 | 0x020a | JA | 0x92f0a4 |
| 7 | 0x0090f000 | 0x00020000 | 0x6200 | JA | 0x92f000 |
| 8 | 0x00087000 | 0x00888000 | 0x6200 | JA | 0x90f000 |
| 9 | 0x00077000 | 0x00010000 | 0 | nein | 0x87000 |
| 10 | 0x00057000 | 0x00020000 | 0x6200 | JA | 0x77000 |
| 11 | 0x00037000 | 0x00020000 | 0x6200 | JA | 0x57000 |
| 12 | 0x00021000 | 0x00016000 | 0 | nein | 0x37000 |
| 13 | 0x00020000 | 0x00001000 | 0 | nein | 0x21000 |
| 14 | 0x00000000 | 0x00020000 | 0 | nein | 0x20000 |
| 15 | 0x009300a4 | 0x1c | 0x020a | JA | 0x9300c0 |
| 16 | 0x0092f0a4 | 0x1000 | 0 | nein | 0x9300a4 |

**Hash-Scope** ≈ [0x37000,0x77000) ∪ [0x87000,0x92f000) ∪ [0x92f000,0x92f0a4) ∪ [0x9300a4,0x9300c0)
∪ [0x9500c0,0xe3f000) ∪ [0xe40000,0xe402e3) ∪ [0xe40314,0x1000000). Darin: PSP-Codetabelle
`_PT_` @0x90f000 (idx 7) und **der gesamte DXE-/Haupt-FV-Körper** (idx 8) sowie die Content-FVs
(idx 4). **Ungehashte Löcher:** [0,0x37000) PSP/Bootloader-Zone (non-FF nur 53 B @0x20000:
aa55aa55…), [0x77000,0x87000) 64 KB komplett gelöscht, [0x92f0a4,0x9300a4) = **der 414d94ad-FFS-
Körper selbst (Selbst-Ausschluss)**, [0x9300c0,0x9500c0) 128-KB-Loch-FV (26 755 non-FF über 7
Pages), [0xe3f000,0xe40000) 4-KB-FV@0xe3f010 (135 non-FF), [0xe402e3,0xe40314) 49 B.

**Falsifikator-Entscheid (plan §5.2 P-1):** die Prüfung hasht via RomLayout **fast den ganzen
Chip** (DXE-Main-Body UND Content-FVs) ⇒ **L2/L3-Korrekturen im gecoverten Bereich nicht machbar
ohne Prüfstellen-Mitführung** (Capsule-Sig + Hash-Recompute + Neuverifikation); **K6-Tabu
verlängert sich auf den Hash-Scope.** Machbar bleiben L0/L1 (NVRAM/Setup/Defaults ⇒ K3-Mechanik)
und die dokumentierten hash-freien Löcher. Residual (C): Quelle der erwarteten Digests
(tabellenlos in der RomLayout — vermutlich im 29a8-$FID-Block 2ebe0275 oder in der WinCert-Kette)
noch nicht verortet.

### 8.3 Gate + Anti-Smuggling (A)

FUN_00002024(addr, len, out): ohne RomLayout (DAT_6900 == 0) → FUN_1e58. Sonst: Iteration über die
Regionen; das Schreibfenster muss in eine Region fallen (size==0 übersprungen); bei
`DAT_6ad8 ∈ {0x12, 0x20}` Bypass; sonst Flag-Gate (Bit 0x400) über die Allow-Manifeste
DAT_61a0/61a1-Bit 4; bei hash-freier Region (0x200==0) **Capsule-Schmuggel-Scan** (FUN_2b84, Fenster
±0x102c/+0x1000), Treffer ⇒ Region-Flag |= 0x200 (ab dann hash-gedeckt); kein Region-Treffer ⇒
0x8000000000000008. Deutung (B): der Gate ist die Umgehungslücke-Kontrolle für die hash-freien
Löcher — Schreibzugriffe auf Löcher sind erlaubt (Allow-Bit gesetzt), aber der Inhalt wird
automatisch auf Capsule-Fracht gescannt.


## 9. P-3: WpbtDxe `0996199f` — WPBT-Kette, Setup-Gate, FG↔FH-Erkenntnis (2026-10-27) — A (Dekompilierung + IFR/NVRAM), B (Deutung)

Modul: DXE-Layer FFS `0996199f-2ce2-4d97-830b-077a7b28588a`, UI „WpbtDxe", Version „1.0"
(Type 7 DRIVER, State 0xf8; Sections DEPEX 0x13/0x3a · PE32 0x10 · UI 0x15 · VERSION 0x14).
Layer-Offsets/Größen (Scratch `p3_hashfix.py`; ⚠ ersetzt eine früher am selben Tag gemessene
Tabelle, die den FFS-Size u24 @+4 statt @+0x14 las und dadurch ungültige Riesenkörper hashte):
**FG @0x524d68 (0xb1a) · FH @0x524d28 (0xb1a) · FIb @0x5252e8 (0xb3a) · FId @0x525508 (0xb3a)**
— deckungsgleich mit `module_diff.md` (2842 → 2842 / → 2874). Die K4-EE-Referenz
„WPBT-Code-Ref @Layer-0x525905" ist der ASCII-String „WPBT" im Body **dieses** Moduls
(FIb-Koordinate; FId @0x525b25) — kein aeb1671d-Code.

| | FG | FH | FIb | FId |
|---|---|---|---|---|
| FFS | 0xb1a = 2 842 B | 0xb1a | 0xb3a = 2 874 B | 0xb3a |
| FFS-sha256 (16-B-Präfix) | `348f76cd0034f3c6…` | `a0dcd50e133babcf…` | `5f643556bc3e966b…` | == FIb |
| PE32 | 2 720 B | 2 720 B | 2 752 B | 2 752 B |
| PE32-sha256 (16-B-Präfix) | `624a78b7509b2fcd…` | `afac2e9316e9bab1…` | `4f4c4218d849780c…` | == FIb |

(FId-PE voll: `4f4c4218d849780c441663b931deebf7b5814cc2967d152fe5c9acc0cc08bf7c` — das
dekompilierte `…/lzma/FV@0xa1eeb8/FFS:0996199f…/section-0xf44404.payload.bin`.)

**FG↔FH differiert exakt 1 Byte @PE-0x4bc: 0x83 → 0x82** (`p3_pe_delta.py`) — das ist das
**GetVariable-DataSize-Immediate** der Builder-Funktion: FG `48 c7 44 24 30 83 02 00 00`
(MOV qword ptr [RSP+0x30], **0x283**) → FH/FId `…82 02…` (**0x282**; FId-Bau @0x491). WpbtDxe
wurde zwischen FG und FH **ausschließlich** an die Setup-Varstore-Verkleinerung 0x283→0x282
angepasst (§7.1 — IOMMU#2-Entfernung): zwei Module (Setup `899407d7` + WpbtDxe `0996199f`)
tragen dieselbe Änderung. FH↔FIb: separater Rebuild (+32 B; e_lfanew 0xd0 → 0xd8 @0x3c,
1779 differierende Bytes im 2 720-B-Overlap, gemeinsamer Suffix nur 0x16 B; FG↔FH dagegen
gemeinsamer Suffix 0x5e3 B). FIb↔FId: **byte-identisch** (FFS und PE).

### 9.1 Code-Kette (A — rea-Ghidra 12.1.4, 6 Prozeduren vollständig dekompiliert)

| VA | Rolle |
|---|---|
| 0x2e0 | Entry: ST+0x60 → gBS (DAT_988), ST+0x58 → gRT (DAT_998); CreateEventEx(EVT_NOTIFY_SIGNAL 0x200, TPL_CALLBACK 0x10, Notify 0x688, Ctx NULL, EventGroup = **gEfiEventReadyToBootGuid** @.data 0x930) |
| 0x688 | ReadyToBoot-Callback (einmalig je Boot): FUN_478 → BootServices→CloseEvent |
| 0x478 | **WPBT-Builder** (unten) |
| 0x360 | EXE-Beschaffung: BootServices→LocateHandleBuffer(ByProtocol 2, gEfiFirmwareVolume2ProtocolGuid @0x8e0) → HandleProtocol je Handle → iface+0x18 = **FV2→Read(NameGuid = Liste @0x910 = [`aeb1671d-019c-4b3b-ba00-35a2e6280436`, NULL-Terminator @0x920], SectionType 0x10 = PE32)** — iteriert die Ein-Element-Liste; out (ptr, size) |
| 0x6ac / 0x6e0 | StrLen16 / bounded strcpy16 (src == NULL → EFI_INVALID_PARAMETER) |

Builder 0x478 (A): RuntimeServices→GetVariable(name **L"Setup"** @0x950, Guid @0x900 =
**EC87D643-EBA4-4BB5-A1E5-3F3E36B20DA9** = die K3-Varstore-GUID, Attr out, DataSize
0x282 (FH+) bzw. 0x283 (FG), Data = 0x282-B-Stackbuffer) → **Gate `CMP byte [SetupData+0x264], 0`**
(Assembly `cmp byte [RBP+0x1b4], r14b`, RBP = RSP+0x100): **0 ⇒ EFI_UNSUPPORTED — keine
WPBT-Tabelle**; sonst LocateProtocol(gEfiAcpiTableProtocolGuid FFE06BDD-… @0x8f0) → FUN_360 →
AllocatePages(AnyPages, **EfiACPIReclaimMemory 9**, pages = ceil((size+0x34)/0x1000)) →
SetMem(0) → Header-Synthese im Table-Buffer: Sig **„WPBT"**, Revision **1**, Length **0x34**
(52), OemId **„ALASKA"**, OemTableId **„A M I"**, OemRevision **1**, CreatorId **„GBT "**,
CreatorRevision **0x25021100**; CopyMem(EXE) @Base+0x34; ImageSize u32 @+0x24 (36),
ImageAddress u64 @+0x28 (40) = Base+0x34, word @+0x30 (48) = **0x101**, word @+0x32 (50) = 0;
InstallAcpiTable(Buffer 0x34 B) via Protokoll[0]. Feldschema = WPBT-Spec (ImageSize u32,
ImageAddress u64, Binary-Args-String) — Deutung (B).
.data-GUID-Tabelle (python-geparst, autoritativ): 0x8e0 FV2 (220E73B6-…), 0x8f0 AcpiTable
(FFE06BDD-…), 0x900 SetupVariable (EC87D643-…), 0x910 aeb1671d + NULL @0x920,
0x930 ReadyToBoot (7CE88FB3-…), 0x940 „ALASKA\0\0" + „A M I\0", 0x950 L"Setup"
(definierter String-Inventar des Moduls: nur „Setup").

**Beobachtung (A, statisch):** das Binary-Args-Feld wird **nie** geschrieben — FUN_6e0
(dst+0x34, src=R8=0) kehrt mit EFI_INVALID_PARAMETER zurück (NULL-Guard), und ein inlined
StrLen16-Tail @0x611 liest `cmp word [R14], r14w` mit **R14 = 0** — statisch sichtbarer
NULL-Read-Branch (#PF-Potenzial). Ob der Zweig auf echter Hardware ausgeführt wird oder tot
ist, ist statisch nicht entscheidbar (D) — der EE entscheidet gemeinsam (K4-Ergebnis).

### 9.2 Gate-Frage + NVRAM (A — scratches/p3_wpbt.py → p3_wpbt_out.json)

Gate-Byte `Setup[0x264]` = IFR-Frage **qid `0x019c`**, ONE_OF, Prompt **„APP Center Download &
Install"**: FG/FH Prompt-sid `0x0920`, Optionen „Disabled"=`00` (sid 0x0922, Flags 0x20) /
„Enabled"=`01` (0x0923); FIb/FId je **+2** (Prompt 0x0922, Optionen 0x0924/0x0925) —
deckungsgleich mit dem §7.1-Pool-Shift (en-Pool 3327 → 3329). **IFR-Default (DefaultId 0x0000,
Type|Value u16 0x0100) = Enabled (0x01)** — identisch über alle vier Releases. **Kein
SUPPRESS_IF/DISABLE_IF/GRAY_OUT_IF am Frage-Knoten** (Kontext-Check: TEXT + SUPPRESS_IF TRUE +
SUBTITLEs davor — die vorstehende GRAY_OUT_IF-Kette @0x317d2 gehört zur Nachbarfrage
qid `0x019b`) ⇒ sichtbare Setup-UI-Option. NVRAM-Factory (StdDefaults `cef5b9a3`): FG/FH/FId
**Setup[0x264] = 0x01**; Kontext [0x260..0x26e] = `ff ff 27 00 01 00 00 00 00 03 00 21 ff 00`.
FIb: das FIb-StdDefaults-Modul ist nicht separat materialisiert (Glob `fib-fvmain` → []) —
Byte übernommen aus §7 (FH == FIb, Payload-sha), nicht eigenständig gemessen.

Nachbarn (vo → Text): 0x260 „Remote Display Feature" (FG qid `0x0252` → FH/FIb/FId `0x0251`,
qid-Shift −1 nach FG-IOMMU#2-Entfernung ✓), 0x261 „Gnb Hd Audio", 0x262 „Above 4GB MMIO
Limit", 0x265 „Preferred Operating Mode". Nebenbefund: die 8-fach-Multi-Post-Familie qids
`0x2821–0x2828` @vo 0x263 „Output Select" („Unknown Device"-Options-Strings mehrfach
wiederholt) — weiteres AMI-Autorisierungs-Duplizier-Muster wie IOMMU (§7.1).

### 9.3 Konsequenz (B) → `bug_candidates.md` K4-Ergebnis

WPBT ist **setup-schaltbar** (Default Enabled): L0 (Option auf Disabled) stoppt die Tabelle
je Boot ohne Image-Eingriff; L1 = Einzelbyte 0x264 in `cef5b9a3` (01→00 — Byte < 0x271, keine
Längen-/Shift-Nachzüge). L3 (Modul-Entfernung) nur nötig, wenn die Tabelle für niemanden je
existieren darf. Verfeinerter EE: WPBT-Tabellen-Nachweis auf dem Board (Windows
`GetSystemFirmwareTable("WPBT")` / Task-Manager) — entscheidet zugleich die NULL-Read-Frage.
