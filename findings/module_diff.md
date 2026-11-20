# Module-Differential FG ↔ FH ↔ FIb ↔ FId (aus rea-Kartografie)

Join: (depth, parent-FV-Offset, FFS-GUID, Ordinal). Geändert = sha256-Differenz.
Layer-Längen sind Join-fremd (sie ändern sich je Version) → eigene Sektion.

## Layer-Längen (Depth-1, joined parent_offset + Ordinal)

| parent | # | FS-GUID | own offset (FG→FId) | length FG / FH / FIb / FId |
|---|---|---|---|---|
| 0x92f000 | 0 | 8c8ce578 | 0x950110→0x950110 | 4096 / 4096 / 4096 / 4096 |
| 0x92f000 | 1 | 8c8ce578 | 0x951160→0x951160 | 94208 / 94208 / 94208 / 94208 |
| 0x92f000 | 2 | 8c8ce578 | 0x95b4c8→0x95b4c0 | 1994752 / 1994752 / 1994752 / 1994752 |
| 0x92f000 | 3 | 8c8ce578 | 0xa0bf58→0xa0bf70 | 253952 / 253952 / 253952 / 253952 |
| 0x92f000 | 4 | 8c8ce578 | 0xa1ee98→0xa1eeb8 | 13484032 / 13484032 / 13185024 / 13205504 **Δ** |

## FG ↔ FH
- gemeinsame Module: 518, **geändert: 97**, neu: 0, entfernt: 0

| join | GUID(ui) | Typ | Größe A→B | layer-offset A | layer length A→B |
|---|---|---|---|---|---|
| d0 p:37000 n1 | cef5b9a3 | raw | 130952 → 130952 (+0 B) | 0x37078 | 20000→20000 |
| d0 p:92f000 n7 | 1df36ff9 | firmware-volume-image | 77644 → 77651 (+7 B) | 0xa0bf08 | 510000→510000 |
| d0 p:92f000 n1 | 414d94ad | freeform | 4140 → 4140 (+0 B) | 0x92f078 | 510000→510000 |
| d0 p:92f000 n5 | 84366c9e | firmware-volume-image | 41826 → 41831 (+5 B) | 0x951110 | 510000→510000 |
| d0 p:92f000 n8 | 9e21fd93 | firmware-volume-image | 4219057 → 4218909 (-148 B) | 0xa1ee58 | 510000→510000 |
| d0 p:e40000 n9 | 3e3b6dc0 | firmware-volume-image | 1020853 → 1020898 (+45 B) | 0xe41fd0 | 1c0000→1c0000 |
| d0 p:e40000 n2 | 3fd1d3a2 | freeform | 164 → 164 (+0 B) | 0xe40270 | 1c0000→1c0000 |
| d0 p:e40000 n5 | 56e14f88 | freeform | 1132 → 1132 (+0 B) | 0xe404a8 | 1c0000→1c0000 |
| d1 p:92f000 n5 | 0718ad81 (T) | driver | 68614 → 68614 (+0 B) | 0xa15eb0 | 3e000→3e000 |
| d1 p:92f000 n300 | 0948381e (F) | smm | 22210 → 22210 (+0 B) | 0x1187368 | cdc000→cdc000 |
| d1 p:92f000 n171 | 0996199f (W) | driver | 2842 → 2842 (+0 B) | 0xf43bf0 | cdc000→cdc000 |
| d1 p:92f000 n158 | 164e5590 (A) | driver | 3354 → 3354 (+0 B) | 0xef8fd8 | cdc000→cdc000 |
| d1 p:92f000 n151 | 16d0a23e (A) | driver | 10474 → 10474 (+0 B) | 0xe8c1b8 | cdc000→cdc000 |
| d1 p:92f000 n33 | 17119241 (S) | driver | 32214 → 32214 (+0 B) | 0xa97028 | cdc000→cdc000 |
| d1 p:92f000 n409 | 1807040d (N) | driver | 68202 → 68202 (+0 B) | 0x14f4c38 | cdc000→cdc000 |
| d1 p:92f000 n430 | 196ca3d8 (T) | driver | 3754 → 3754 (+0 B) | 0x1563750 | cdc000→cdc000 |
| d1 p:92f000 n220 | 1ae033de (G) | driver | 23606 → 23606 (+0 B) | 0xfd5bb0 | cdc000→cdc000 |
| d1 p:92f000 n147 | 1dfb7bfa (A) | driver | 2638 → 2638 (+0 B) | 0xd42ca0 | cdc000→cdc000 |
| d1 p:92f000 n360 | 281dd072 (G) | smm | 8362 → 8362 (+0 B) | 0x12a38c8 | cdc000→cdc000 |
| d1 p:92f000 n329 | 2ad511c7 (C) | smm | 60542 → 60542 (+0 B) | 0x121bbe8 | cdc000→cdc000 |
| d1 p:92f000 n294 | 2fe607a1 (F) | smm | 22210 → 22210 (+0 B) | 0x11677d8 | cdc000→cdc000 |
| d1 p:92f000 n431 | 3115c2ac (A) | driver | 1942 → 1942 (+0 B) | 0x1564600 | cdc000→cdc000 |
| d1 p:92f000 n344 | 3370a4bd (S) | smm | 23790 → 23790 (+0 B) | 0x12728a8 | cdc000→cdc000 |
| d1 p:92f000 n14 | 39045756 (T) | driver | 68270 → 68270 (+0 B) | 0xa37a98 | 3e000→3e000 |
| d1 p:92f000 n206 | 397b1bef (G) | driver | 30786 → 30754 (-32 B) | 0xfab5c8 | cdc000→cdc000 |
| d1 p:92f000 n28 | 399a229d (P) | driver | 8926 → 8926 (+0 B) | 0xa891e0 | cdc000→cdc000 |
| d1 p:92f000 n23 | 399a229d (P) | driver | 8990 → 8990 (+0 B) | 0xa82468 | cdc000→cdc000 |
| d1 p:92f000 n357 | 39add8a6 (G) | smm | 10438 → 10438 (+0 B) | 0x129d6b0 | cdc000→cdc000 |
| d1 p:92f000 n364 | 3a1aa6f8 (A) | smm | 10926 → 10926 (+0 B) | 0x12abb78 | cdc000→cdc000 |
| d1 p:92f000 n25 | 3b4d59ec (P) | driver | 8926 → 8926 (+0 B) | 0xa85738 | cdc000→cdc000 |
| d1 p:92f000 n239 | 3b87cd35 (C) | driver | 233154 → 232610 (-544 B) | 0x1011b00 | cdc000→cdc000 |
| d1 p:92f000 n248 | 3c1de39f (P) | driver | 77054 → 77054 (+0 B) | 0x1072a88 | cdc000→cdc000 |
| d1 p:92f000 n199 | 3f79bee2 (P) | driver | 3606 → 3606 (+0 B) | 0xfa0a40 | cdc000→cdc000 |
| d1 p:92f000 n258 | 447a1b58 (N) | smm | 67286 → 67286 (+0 B) | 0x10d3120 | cdc000→cdc000 |
| d1 p:92f000 n428 | 4551f2f5 (S) | driver | 5574 → 5574 (+0 B) | 0x1560f30 | cdc000→cdc000 |
| d1 p:92f000 n13 | 4c9509df (I) | driver | 2162 → 2162 (+0 B) | 0xa744a0 | cdc000→cdc000 |
| d1 p:92f000 n229 | 510df6a1 (S) | driver | 9478 → 9478 (+0 B) | 0xfeb198 | cdc000→cdc000 |
| d1 p:92f000 n355 | 534a6a34 (R) | smm | 9422 → 9422 (+0 B) | 0x1299118 | cdc000→cdc000 |
| d1 p:92f000 n168 | 580dd900 (U) | driver | 70146 → 70146 (+0 B) | 0xf14eb8 | cdc000→cdc000 |
| d1 p:92f000 n210 | 5b2f7f08 (G) | driver | 2418 → 2418 (+0 B) | 0xfbc548 | cdc000→cdc000 |
| d1 p:92f000 n205 | 5f098347 (G) | driver | 2414 → 2414 (+0 B) | 0xfaac58 | cdc000→cdc000 |
| d1 p:92f000 n219 | 615e1d36 (G) | driver | 7314 → 7314 (+0 B) | 0xfd3f18 | cdc000→cdc000 |
| d1 p:92f000 n211 | 62ec4bab (G) | driver | 25142 → 25142 (+0 B) | 0xfbcec0 | cdc000→cdc000 |
| d1 p:92f000 n208 | 63d00dc9 (G) | driver | 33298 → 33234 (-64 B) | 0xfb3aa0 | cdc000→cdc000 |
| d1 p:92f000 n224 | 69b5a7e7 (P) | driver | 2426 → 2426 (+0 B) | 0xfdf460 | cdc000→cdc000 |
| d1 p:92f000 n361 | 6e9c745f (G) | smm | 8358 → 8358 (+0 B) | 0x12a5978 | cdc000→cdc000 |
| d1 p:92f000 n401 | 709e6472 | freeform | 184 → 184 (+0 B) | 0x132a640 | cdc000→cdc000 |
| d1 p:92f000 n234 | 77eb6c06 (C) | driver | 59994 → 59994 (+0 B) | 0xff6160 | cdc000→cdc000 |
| d1 p:92f000 n424 | 80d7491a (F) | driver | 5258 → 5258 (+0 B) | 0x15572c0 | cdc000→cdc000 |
| d1 p:92f000 n163 | 80e66e0a (P) | driver | 30558 → 30558 (+0 B) | 0xefd7f8 | cdc000→cdc000 |
| d1 p:92f000 n288 | 82adb73c (F) | smm | 25282 → 25282 (+0 B) | 0x114ebc8 | cdc000→cdc000 |
| d1 p:92f000 n411 | 8835d63e (G) | driver | 144378 → 144378 (+0 B) | 0x15092b0 | cdc000→cdc000 |
| d1 p:92f000 n150 | 899407d7 (S) | driver | 1330042 → 1329978 (-64 B) | 0xd47638 | cdc000→cdc000 |
| d1 p:92f000 n129 | 8e09c390 (A) | driver | 1706 → 1706 (+0 B) | 0xd13290 | cdc000→cdc000 |
| d1 p:92f000 n363 | 8eff1fd5 (G) | smm | 8362 → 8362 (+0 B) | 0x12a9ac8 | cdc000→cdc000 |
| d1 p:92f000 n166 | 8f3f1de2 (R) | driver | 5786 → 5786 (+0 B) | 0xf130e8 | cdc000→cdc000 |
| d1 p:92f000 n4 | 8f4b8f82 (B) | driver | 92050 → 92050 (+0 B) | 0xa2bc70 | cdc000→cdc000 |
| d1 p:92f000 n437 | 9221315b | freeform | 623 → 623 (+0 B) | 0x158efa0 | cdc000→cdc000 |
| d1 p:92f000 n359 | 9557dfca (G) | smm | 7334 → 7334 (+0 B) | 0x12a1c20 | cdc000→cdc000 |
| d1 p:92f000 n35 | 99c062a1 (S) | driver | 6010 → 6010 (+0 B) | 0xaa0560 | cdc000→cdc000 |
| d1 p:92f000 n427 | 9b3ada4f (P) | peim | 11818 → 11818 (+0 B) | 0x155e100 | cdc000→cdc000 |
| d1 p:92f000 n264 | 9caa3071 (G) | smm | 156866 → 156866 (+0 B) | 0x10ef308 | cdc000→cdc000 |
| d1 p:92f000 n217 | 9d02cfb9 (G) | driver | 25554 → 25554 (+0 B) | 0xfcd2b0 | cdc000→cdc000 |
| d1 p:92f000 n262 | 9dd14bca (I) | smm | 11502 → 11502 (+0 B) | 0x10e8580 | cdc000→cdc000 |
| d1 p:92f000 n3 | a062cf1f (C) | driver | 51118 → 51118 (+0 B) | 0x953d90 | 17000→17000 |
| d1 p:92f000 n420 | a59a0056 | freeform | 170 → 170 (+0 B) | 0x1553258 | cdc000→cdc000 |
| d1 p:92f000 n32 | a7119441 (S) | driver | 29754 → 29754 (+0 B) | 0xa8fbe8 | cdc000→cdc000 |
| d1 p:92f000 n350 | aca87ea5 (B) | smm | 19102 → 19102 (+0 B) | 0x128b330 | cdc000→cdc000 |
| d1 p:92f000 n16 | add70a4d (T) | driver | 1386 → 1386 (+0 B) | 0xa49440 | 3e000→3e000 |
| d1 p:92f000 n207 | b05fce34 (G) | driver | 3214 → 3214 (+0 B) | 0xfb2e10 | cdc000→cdc000 |
| d1 p:92f000 n418 | b13edd38 (S) | driver | 38910 → 38910 (+0 B) | 0x15490c8 | cdc000→cdc000 |
| d1 p:92f000 n438 | b1da0adf | driver | 220196 → 220181 (-15 B) | 0x158f210 | cdc000→cdc000 |
| d1 p:92f000 n193 | b7246c46 (C) | driver | 21918 → 21918 (+0 B) | 0xf84b60 | cdc000→cdc000 |
| d1 p:92f000 n29 | b7d19491 (S) | driver | 10374 → 10374 (+0 B) | 0xa8b4c0 | cdc000→cdc000 |
| d1 p:92f000 n160 | b7ee4835 (H) | driver | 6294 → 6294 (+0 B) | 0xefaf18 | cdc000→cdc000 |
| d1 p:92f000 n204 | c2a7dc45 (G) | driver | 14794 → 14794 (+0 B) | 0xfa7288 | cdc000→cdc000 |
| d1 p:92f000 n213 | c3704a22 (G) | driver | 6990 → 6990 (+0 B) | 0xfc3990 | cdc000→cdc000 |
| d1 p:92f000 n16 | c7dd8530 (S) | driver | 2530 → 2530 (+0 B) | 0xa79b78 | cdc000→cdc000 |
| d1 p:92f000 n194 | d20d5c9f (Q) | driver | 69634 → 69634 (+0 B) | 0xf8a100 | cdc000→cdc000 |
| d1 p:92f000 n183 | d4395796 (A) | driver | 15238 → 15238 (+0 B) | 0xf65830 | cdc000→cdc000 |
| d1 p:92f000 n145 | d60cf145 (A) | driver | 2250 → 2250 (+0 B) | 0xd37828 | cdc000→cdc000 |
| d1 p:92f000 n30 | d9ea74e6 (S) | driver | 3946 → 3946 (+0 B) | 0xa8dd48 | cdc000→cdc000 |
| d1 p:92f000 n429 | daf4bf89 | freeform | 4690 → 4690 (+0 B) | 0x15624f8 | cdc000→cdc000 |
| d1 p:92f000 n20 | dd9d5646 (P) | driver | 8830 → 8830 (+0 B) | 0xa7e7e8 | cdc000→cdc000 |
| d1 p:92f000 n405 | deadbeef | freeform | 47064 → 47064 (+0 B) | 0x14d9520 | cdc000→cdc000 |
| d1 p:92f000 n216 | debb5070 (G) | driver | 6818 → 6818 (+0 B) | 0xfcb808 | cdc000→cdc000 |
| d1 p:92f000 n14 | e03abadf (C) | driver | 17018 → 17018 (+0 B) | 0xa74d18 | cdc000→cdc000 |
| d1 p:92f000 n297 | e048749b (F) | smm | 24258 → 24258 (+0 B) | 0x11784c8 | cdc000→cdc000 |
| d1 p:92f000 n362 | e1309fe9 (G) | smm | 8358 → 8358 (+0 B) | 0x12a7a20 | cdc000→cdc000 |
| d1 p:92f000 n223 | e52aff5c (D) | driver | 5810 → 5810 (+0 B) | 0xfddda8 | cdc000→cdc000 |
| d1 p:92f000 n353 | e83e1c68 (I) | smm | 9934 → 9934 (+0 B) | 0x1293b60 | cdc000→cdc000 |
| d1 p:92f000 n358 | ecd933b3 (G) | smm | 7334 → 7334 (+0 B) | 0x129ff78 | cdc000→cdc000 |
| d1 p:92f000 n34 | eecc1363 (S) | driver | 5978 → 5978 (+0 B) | 0xa9ee00 | cdc000→cdc000 |
| d1 p:92f000 n10 | f80697e9 (S) | driver | 39974 → 39974 (+0 B) | 0xa69870 | cdc000→cdc000 |
| d1 p:92f000 n214 | fbeb378e (G) | driver | 23186 → 23186 (+0 B) | 0xfc54e0 | cdc000→cdc000 |
| d1 p:92f000 n8 | fd93f9e1 (T) | smm | 6830 → 6830 (+0 B) | 0xa2a4b8 | 3e000→3e000 |
| d1 p:92f000 n439 | fe612b72 | freeform | 19063 → 19277 (+214 B) | 0x15c4e38 | cdc000→cdc000 |

## FH ↔ FIb
- gemeinsame Module: 518, **geändert: 55**, neu: 0, entfernt: 0

| join | GUID(ui) | Typ | Größe A→B | layer-offset A | layer length A→B |
|---|---|---|---|---|---|
| d0 p:92f000 n1 | 414d94ad | freeform | 4140 → 4140 (+0 B) | 0x92f078 | 510000→510000 |
| d0 p:92f000 n5 | 84366c9e | firmware-volume-image | 41831 → 41820 (-11 B) | 0x951110 | 510000→510000 |
| d0 p:92f000 n8 | 9e21fd93 | firmware-volume-image | 4218909 → 3913887 (-305022 B) | 0xa1ee60 | 510000→510000 |
| d0 p:92f000 n6 | c0492c7f | firmware-volume-image | 723600 → 723629 (+29 B) | 0x95b478 | 510000→510000 |
| d0 p:e40000 n9 | 3e3b6dc0 | firmware-volume-image | 1020898 → 1020813 (-85 B) | 0xe41fd0 | 1c0000→1c0000 |
| d0 p:e40000 n2 | 3fd1d3a2 | freeform | 164 → 164 (+0 B) | 0xe40270 | 1c0000→1c0000 |
| d0 p:e40000 n5 | 56e14f88 | freeform | 1132 → 1132 (+0 B) | 0xe404a8 | 1c0000→1c0000 |
| d1 p:92f000 n171 | 0996199f (W) | driver | 2842 → 2874 (+32 B) | 0xf43bb8 | cdc000→c93000 |
| d1 p:92f000 n435 | 16271fca (C) | driver | 3638 → 3638 (+0 B) | 0x157a408 | cdc000→c93000 |
| d1 p:92f000 n409 | 1807040d (N) | driver | 68202 → 68202 (+0 B) | 0x14f4980 | cdc000→c93000 |
| d1 p:92f000 n146 | 1a1e4886 (C) | driver | 43942 → 43974 (+32 B) | 0xd38100 | cdc000→c93000 |
| d1 p:92f000 n120 | 29d40f30 (A) | driver | 1378 → 1378 (+0 B) | 0xc8cde8 | cdc000→c93000 |
| d1 p:92f000 n329 | 2ad511c7 (C) | smm | 60542 → 60542 (+0 B) | 0x121b930 | cdc000→c93000 |
| d1 p:92f000 n344 | 3370a4bd (S) | smm | 23790 → 23790 (+0 B) | 0x12725f0 | cdc000→c93000 |
| d1 p:92f000 n239 | 3b87cd35 (C) | driver | 232610 → 232610 (+0 B) | 0x1011a68 | cdc000→c93000 |
| d1 p:92f000 n75 | 41ef54ad (A) | driver | 35438 → 35406 (-32 B) | 0xb701f8 | cdc000→c93000 |
| d1 p:92f000 n258 | 447a1b58 (N) | smm | 67286 → 67286 (+0 B) | 0x10d2e68 | cdc000→c93000 |
| d1 p:92f000 n428 | 4551f2f5 (S) | driver | 5574 → 5574 (+0 B) | 0x1560c78 | cdc000→c93000 |
| d1 p:92f000 n102 | 4d3708a0 (A) | driver | 46518 → 46550 (+32 B) | 0xc53170 | cdc000→c93000 |
| d1 p:92f000 n168 | 580dd900 (U) | driver | 70146 → 70178 (+32 B) | 0xf14e80 | cdc000→c93000 |
| d1 p:92f000 n250 | 5fecef6b (P) | driver | 20730 → 20826 (+96 B) | 0x1085b48 | cdc000→c93000 |
| d1 p:92f000 n401 | 709e6472 | freeform | 184 → 184 (+0 B) | 0x132a388 | cdc000→c93000 |
| d1 p:92f000 n162 | 76d5cf91 (O) | driver | 2626 → 4130 (+1504 B) | 0xefcd78 | cdc000→c93000 |
| d1 p:92f000 n234 | 77eb6c06 (C) | driver | 59994 → 59994 (+0 B) | 0xff60c8 | cdc000→c93000 |
| d1 p:92f000 n74 | 828c017b (A) | driver | 29230 → 29198 (-32 B) | 0xb68fc8 | cdc000→c93000 |
| d1 p:92f000 n411 | 8835d63e (G) | driver | 144378 → 144378 (+0 B) | 0x1508ff8 | cdc000→c93000 |
| d1 p:92f000 n150 | 899407d7 (S) | driver | 1329978 → 1329658 (-320 B) | 0xd47640 | cdc000→c93000 |
| d1 p:92f000 n264 | 9caa3071 (G) | smm | 156866 → 156866 (+0 B) | 0x10ef050 | cdc000→c93000 |
| d1 p:92f000 n3 | a062cf1f (C) | driver | 51118 → 51118 (+0 B) | 0x953d90 | 17000→17000 |
| d1 p:92f000 n326 | a3ff0ef5 (P) | smm | 41626 → 41626 (+0 B) | 0x120bbb0 | cdc000→c93000 |
| d1 p:92f000 n420 | a59a0056 | freeform | 170 → 170 (+0 B) | 0x1552fa0 | cdc000→c93000 |
| d1 p:92f000 n90 | acdea335 (S) | driver | 59214 → 59278 (+64 B) | 0xbe4e68 | cdc000→c93000 |
| d1 p:92f000 n451 | aeb1671d | freeform | 712518 → 409471 (-303047 B) | 0x15d8b68 | cdc000→c93000 |
| d1 p:92f000 n309 | b1bac051 (A) | smm | 46286 → 46286 (+0 B) | 0x11ba0b0 | cdc000→c93000 |
| d1 p:92f000 n438 | b1da0adf | driver | 220181 → 220187 (+6 B) | 0x158ef58 | cdc000→c93000 |
| d1 p:92f000 n193 | b7246c46 (C) | driver | 21918 → 21918 (+0 B) | 0xf84b28 | cdc000→c93000 |
| d1 p:92f000 n160 | b7ee4835 (H) | driver | 6294 → 6294 (+0 B) | 0xefaee0 | cdc000→c93000 |
| d1 p:92f000 n6 | b95e9fda (U) | driver | 64682 → 64682 (+0 B) | 0x977f18 | 1e7000→1e7000 |
| d1 p:92f000 n130 | bbb77cb9 (A) | driver | 42214 → 42214 (+0 B) | 0xd13948 | cdc000→c93000 |
| d1 p:92f000 n97 | d14ea3f9 (A) | driver | 41966 → 42030 (+64 B) | 0xc2e4e0 | cdc000→c93000 |
| d1 p:92f000 n194 | d20d5c9f (Q) | driver | 69634 → 69634 (+0 B) | 0xf8a0c8 | cdc000→c93000 |
| d1 p:92f000 n183 | d4395796 (A) | driver | 15238 → 15238 (+0 B) | 0xf657f8 | cdc000→c93000 |
| d1 p:92f000 n85 | d7908ec2 (A) | driver | 42494 → 42494 (+0 B) | 0xba8068 | cdc000→c93000 |
| d1 p:92f000 n222 | d9f0c1cf (G) | driver | 7458 → 7362 (-96 B) | 0xfdbfe8 | cdc000→c93000 |
| d1 p:92f000 n429 | daf4bf89 | freeform | 4690 → 4691 (+1 B) | 0x1562240 | cdc000→c93000 |
| d1 p:92f000 n405 | deadbeef | freeform | 47064 → 47694 (+630 B) | 0x14d9268 | cdc000→c93000 |
| d1 p:92f000 n88 | e1db609a (A) | driver | 74574 → 74574 (+0 B) | 0xbc7ab8 | cdc000→c93000 |
| d1 p:92f000 n325 | e21f35a8 (P) | smm | 5798 → 5798 (+0 B) | 0x120a508 | cdc000→c93000 |
| d1 p:92f000 n201 | e68c55b8 (G) | driver | 2254 → 2286 (+32 B) | 0xfa2008 | cdc000→c93000 |
| d1 p:92f000 n95 | e74ca1e2 (A) | driver | 41530 → 41594 (+64 B) | 0xc1c600 | cdc000→c93000 |
| d1 p:92f000 n71 | ecadbbb6 (A) | driver | 23822 → 23886 (+64 B) | 0xb58548 | cdc000→c93000 |
| d1 p:92f000 n10 | f80697e9 (S) | driver | 39974 → 39974 (+0 B) | 0xa69878 | cdc000→c93000 |
| d1 p:92f000 n196 | fb11f8fe (D) | driver | 14726 → 14854 (+128 B) | 0xf9bf88 | cdc000→c93000 |
| d1 p:92f000 n443 | fbf95065 | freeform | 5118 → 6943 (+1825 B) | 0x15d4ff8 | cdc000→c93000 |
| d1 p:92f000 n439 | fe612b72 | freeform | 19277 → 19045 (-232 B) | 0x15c4b70 | cdc000→c93000 |

## FIb ↔ FId
- gemeinsame Module: 518, **geändert: 40**, neu: 0, entfernt: 0

| join | GUID(ui) | Typ | Größe A→B | layer-offset A | layer length A→B |
|---|---|---|---|---|---|
| d0 p:92f000 n1 | 414d94ad | freeform | 4140 → 4140 (+0 B) | 0x92f078 | 510000→510000 |
| d0 p:92f000 n5 | 84366c9e | firmware-volume-image | 41820 → 41823 (+3 B) | 0x951110 | 510000→510000 |
| d0 p:92f000 n8 | 9e21fd93 | firmware-volume-image | 3913887 → 3922969 (+9082 B) | 0xa1ee78 | 510000→510000 |
| d0 p:e40000 n9 | 3e3b6dc0 | firmware-volume-image | 1020813 → 1021144 (+331 B) | 0xe41fd0 | 1c0000→1c0000 |
| d0 p:e40000 n2 | 3fd1d3a2 | freeform | 164 → 164 (+0 B) | 0xe40270 | 1c0000→1c0000 |
| d0 p:e40000 n5 | 56e14f88 | freeform | 1132 → 1132 (+0 B) | 0xe404a8 | 1c0000→1c0000 |
| d1 p:92f000 n91 | 15e4c005 (S) | driver | 42546 → 42674 (+128 B) | 0xbf3610 | c93000→c98000 |
| d1 p:92f000 n435 | 16271fca (C) | driver | 3638 → 3638 (+0 B) | 0x157ad18 | c93000→c98000 |
| d1 p:92f000 n409 | 1807040d (N) | driver | 68202 → 68202 (+0 B) | 0x14f5290 | c93000→c98000 |
| d1 p:92f000 n120 | 29d40f30 (A) | driver | 1378 → 1378 (+0 B) | 0xc8cee0 | c93000→c98000 |
| d1 p:92f000 n329 | 2ad511c7 (C) | smm | 60542 → 60542 (+0 B) | 0x121bfc8 | c93000→c98000 |
| d1 p:92f000 n344 | 3370a4bd (S) | smm | 23790 → 23790 (+0 B) | 0x1272c88 | c93000→c98000 |
| d1 p:92f000 n239 | 3b87cd35 (C) | driver | 232610 → 232610 (+0 B) | 0x10120a0 | c93000→c98000 |
| d1 p:92f000 n199 | 3f79bee2 (P) | driver | 3606 → 3670 (+64 B) | 0xfa1080 | c93000→c98000 |
| d1 p:92f000 n258 | 447a1b58 (N) | smm | 67286 → 67286 (+0 B) | 0x10d3500 | c93000→c98000 |
| d1 p:92f000 n428 | 4551f2f5 (S) | driver | 5574 → 5574 (+0 B) | 0x1561588 | c93000→c98000 |
| d1 p:92f000 n433 | 601f27e3 | freeform | 55340 → 57388 (+2048 B) | 0x1565de8 | c93000→c98000 |
| d1 p:92f000 n401 | 709e6472 | freeform | 184 → 184 (+0 B) | 0x132aa20 | c93000→c98000 |
| d1 p:92f000 n234 | 77eb6c06 (C) | driver | 59994 → 59994 (+0 B) | 0xff6700 | c93000→c98000 |
| d1 p:92f000 n36 | 87c3e993 (S) | smm | 10894 → 10894 (+0 B) | 0xaa1d00 | c93000→c98000 |
| d1 p:92f000 n411 | 8835d63e (G) | driver | 144378 → 144410 (+32 B) | 0x1509908 | c93000→c98000 |
| d1 p:92f000 n150 | 899407d7 (S) | driver | 1329658 → 1329818 (+160 B) | 0xd47758 | c93000→c98000 |
| d1 p:92f000 n4 | 8f4b8f82 (B) | driver | 92050 → 92114 (+64 B) | 0xa2bc90 | c93000→c98000 |
| d1 p:92f000 n3 | a062cf1f (C) | driver | 51118 → 51118 (+0 B) | 0x953d90 | 17000→17000 |
| d1 p:92f000 n420 | a59a0056 | freeform | 170 → 170 (+0 B) | 0x15538b0 | c93000→c98000 |
| d1 p:92f000 n90 | acdea335 (S) | driver | 59278 → 59278 (+0 B) | 0xbe4e80 | c93000→c98000 |
| d1 p:92f000 n438 | b1da0adf | driver | 220187 → 219937 (-250 B) | 0x158f868 | c93000→c98000 |
| d1 p:92f000 n193 | b7246c46 (C) | driver | 21918 → 22014 (+96 B) | 0xf85120 | c93000→c98000 |
| d1 p:92f000 n160 | b7ee4835 (H) | driver | 6294 → 6294 (+0 B) | 0xefaeb8 | c93000→c98000 |
| d1 p:92f000 n417 | ba28936b (S) | driver | 7914 → 8202 (+288 B) | 0x1547830 | c93000→c98000 |
| d1 p:92f000 n130 | bbb77cb9 (A) | driver | 42214 → 42214 (+0 B) | 0xd13a40 | c93000→c98000 |
| d1 p:92f000 n267 | c99e42d0 (S) | smm | 14514 → 14514 (+0 B) | 0x11180b8 | c93000→c98000 |
| d1 p:92f000 n194 | d20d5c9f (Q) | driver | 69634 → 69762 (+128 B) | 0xf8a6c0 | c93000→c98000 |
| d1 p:92f000 n183 | d4395796 (A) | driver | 15238 → 15238 (+0 B) | 0xf65df0 | c93000→c98000 |
| d1 p:92f000 n255 | d9fd094f (R) | driver | 151110 → 171334 (+20224 B) | 0x109f1d0 | c93000→c98000 |
| d1 p:92f000 n429 | daf4bf89 | freeform | 4691 → 4691 (+0 B) | 0x1562b50 | c93000→c98000 |
| d1 p:92f000 n405 | deadbeef | freeform | 47694 → 47694 (+0 B) | 0x14d9900 | c93000→c98000 |
| d1 p:92f000 n228 | e23f86e1 (S) | driver | 16978 → 16978 (+0 B) | 0xfe74e0 | c93000→c98000 |
| d1 p:92f000 n10 | f80697e9 (S) | driver | 39974 → 40166 (+192 B) | 0xa69890 | c93000→c98000 |
| d1 p:92f000 n154 | fa20568b (B) | driver | 34434 → 34434 (+0 B) | 0xe99ab8 | c93000→c98000 |

