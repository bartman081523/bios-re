# ASUS B550-PLUS BIOS-Architektur & Tuning-Analyse
**Ziel-Hardware:** ASUS TUF GAMING B550-PLUS / ASUS PRIME B550-PLUS / ROG STRIX B550-F  
**Firmware-Grundlage:** AMI Aptio V (ASUS UEFI BIOS Utility mit EZ Mode / Advanced Mode)  
**Kapsel-Format:** ASUS `.CAP` (2048-Byte RSA Security Header vor dem 16MB/32MB UEFI-ROM-Body)

---

## 1. Systemische Gegenüberstellung: Gigabyte B550 vs. ASUS B550-PLUS

Obwohl beide Mainboard-Hersteller auf den **AMD B550 Chipsatz** und den **AMI Aptio V** Kern setzen, unterscheidet sich die Menüführung und Nomenklatur im UEFI deutlich.

| Funktion / Subsystem | Gigabyte B550 AORUS ELITE V2 | ASUS TUF / PRIME B550-PLUS | Technische Bedeutung & Epistemische Wirkung |
|---|---|---|---|
| **Speicher-Übertaktung** | `M.I.T.` $\rightarrow$ `Extreme Memory Profile (X.M.P.)` | `Ai Tweaker` $\rightarrow$ `Ai Overclock Tuner` $\rightarrow$ **`D.O.C.P.`** | ASUS nennt XMP auf AMD-Boards **D.O.C.P.** (Direct OverClock Profile). Lädt SPD-Timings & 1.35V. |
| **Infinity Fabric Takt** | `Advanced Memory Settings` $\rightarrow$ `FCLK Frequency` | `Ai Tweaker` $\rightarrow$ **`FCLK Frequency`** | Taktet den AMD Interconnect synchron 1:1 ($FCLK = MCLK$). |
| **Re-Size BAR Schnelltaste**| Nicht vorhanden (nur im Menü) | **`[F4] Re-Size BAR`** (obere Statusleiste) | ASUS bietet einen direkten 1-Tasten-Umschalter im BIOS-Header. |
| **Re-Size BAR Menüpfad** | `Peripherals` $\rightarrow$ `Re-Size BAR Support` | `Advanced` $\rightarrow$ `PCI Subsystem Settings` $\rightarrow$ `Re-Size BAR Support` | Vollzugriff der CPU auf den VRAM (z. B. 12 GB RTX 2060). |
| **Above 4G Decoding** | `Peripherals` $\rightarrow$ `Above 4G Decoding` | `Advanced` $\rightarrow$ `PCI Subsystem Settings` $\rightarrow$ `Above 4G Decoding` | 64-Bit MMIO-Adressierung oberhalb der 4GB-Grenze. |
| **CPU Boost (PB2)** | `Advanced CPU Settings` $\rightarrow$ `Core Performance Boost` | `Ai Tweaker` $\rightarrow$ `Precision Boost Overdrive` / `AMD CBS` | Schaltet die 3,7 GHz Basistakt-Deckelung auf bis zu 4,65 GHz frei. |
| **Anti-Freeze Ruhestrom**| `Advanced CPU Settings` $\rightarrow$ `Power Supply Idle Control` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common Options` $\rightarrow$ `Power Supply Idle Control` | Verhindert C6-Niedrigstrom-Spannungsabfälle unter 0.05A. |
| **Firmware-Dropper (WPBT)**| `Peripherals` $\rightarrow$ `APP Center Download & Install` | `Tool` $\rightarrow$ **`ASUS Armoury Crate`** $\rightarrow$ `Download & Install ARMOURY CRATE app` | Schaltet die ACPI WPBT-Tabelle ab; verhindert Windows-Dienstinjektion. |
| **UEFI-Modus / CSM** | `BIOS` $\rightarrow$ `CSM Support` | `Boot` $\rightarrow$ `CSM (Compatibility Support Module)` $\rightarrow$ **`Launch CSM`** | Muss auf `Disabled` stehen für reines UEFI GOP und Re-Size BAR. |
| **IOMMU / DMA-Schutz** | `Peripherals` $\rightarrow$ `AMD IOMMU` | `Advanced` $\rightarrow$ `AMD CBS` $\rightarrow$ `NBIO Common Options` $\rightarrow$ **`IOMMU`** | Hardware-Isolation für KVM, VFIO, Docker und WSL2. |
| **Fast Boot** | `BIOS` $\rightarrow$ `Fast Boot` | `Boot` $\rightarrow$ **`Fast Boot`** | Unter Linux zwingend auf `Disabled` (verhindert NVMe-Kaltstartfehler). |

---

## 2. ASUS-spezifische Besonderheiten bei der Konfiguration

### 2.1 Das D.O.C.P.-Verfahren (ASUS X.M.P.)
Auf AMD-Plattformen lizenziert ASUS den Namen „XMP“ oft nicht direkt, sondern implementiert den Standard als **D.O.C.P. (Direct OverClock Profile)**:
1. Im Reiter **`Ai Tweaker`** den Punkt **`Ai Overclock Tuner`** anwählen.
2. Von `Auto` auf **`D.O.C.P.`** umstellen.
3. Das BIOS blendet daraufhin das Feld `D.O.C.P.` ein (z. B. `D.O.C.P. DDR4-3200 16-18-18-38-1.35V`).
4. **Wichtig:** ASUS setzt dabei die `DRAM Voltage` im Menü `Ai Tweaker` automatisch auf `1.350V` und passt die primären Subtimings an.

### 2.2 Der ASUS F4 Re-Size BAR Shortcut
Im Gegensatz zu Gigabyte besitzt das ASUS UEFI in der oberen Menüleiste einen Schnellschalter:
* Durch Drücken der Taste **`F4`** auf der Tastatur kann `Above 4G Decoding` und `Re-Size BAR Support` mit einem Tastendruck zwischen `Disabled` und `Enabled/Auto` umgeschaltet werden.
* Alternativer manueller Pfad: `Advanced` $\rightarrow$ `PCI Subsystem Settings` $\rightarrow$ `Above 4G Decoding = Enabled` $\rightarrow$ `Re-Size BAR Support = Auto`.

### 2.3 Das ASUS Armoury Crate Dropper-Modul (WPBT)
Analog zum Gigabyte `WpbtDxe`-Dropper besitzt ASUS das **Armoury Crate** Push-Modul:
* **Pfad:** `Tool` $\rightarrow$ `ASUS Armoury Crate` $\rightarrow$ `Download & Install ARMOURY CRATE app` $\rightarrow$ **`Disabled`**.
* **Wirkung:** Verhindert, dass das BIOS beim Booten eine ACPI WPBT-Tabelle generiert, die Windows veranlasst, beim Start den ASUS Update-Dienst ungefragt herunterzuladen.

---

## 3. Schritt-für-Schritt Anleitung: Balanced-Profil auf ASUS B550-PLUS

1. **Starten:** PC einschalten, wiederholt **`Entf`** oder **`F2`** drücken.
2. **Modus:** Falls im vereinfachten EZ Mode gestartet, Taste **`F7`** drücken (Advanced Mode).
3. **RAM & Fabric (D.O.C.P.):**
   * Gehe zu **`Ai Tweaker`**.
   * `Ai Overclock Tuner` $\rightarrow$ auf **`D.O.C.P.`** stellen.
   * `FCLK Frequency` $\rightarrow$ auf **`1600MHz`** (bzw. halber RAM-Takt) stellen.
4. **Grafik (Re-Size BAR):**
   * Entweder Taste **`F4`** drücken und aktivieren ODER:
   * Gehe zu **`Advanced`** $\rightarrow$ `PCI Subsystem Settings`.
   * `Above 4G Decoding` $\rightarrow$ **`Enabled`**.
   * `Re-Size BAR Support` $\rightarrow$ **`Auto`**.
5. **CPU Boost & C6 Anti-Freeze:**
   * Gehe zu **`Advanced`** $\rightarrow$ `AMD CBS` $\rightarrow$ `CPU Common Options`.
   * `Core Performance Boost` $\rightarrow$ **`Auto`**.
   * `Power Supply Idle Control` $\rightarrow$ **`Typical Current Idle`**.
   * `Global C-state Control` $\rightarrow$ **`Enabled`**.
6. **Firmware-Hygiene (Dropper aus):**
   * Gehe zu **`Tool`** $\rightarrow$ `ASUS Armoury Crate`.
   * `Download & Install ARMOURY CRATE app` $\rightarrow$ **`Disabled`**.
7. **CSM & Fast Boot:**
   * Gehe zu **`Boot`** $\rightarrow$ `CSM (Compatibility Support Module)` $\rightarrow$ `Launch CSM` $\rightarrow$ **`Disabled`**.
   * Gehe zu **`Boot`** $\rightarrow$ `Fast Boot` $\rightarrow$ **`Disabled`** (für Linux-Stabilität).
8. **Speichern:**
   * Taste **`F10`** drücken und mit **`Enter`** (Save Changes & Reset) bestätigen.
