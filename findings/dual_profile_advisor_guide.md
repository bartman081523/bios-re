# Epistemischer 3-in-1 BIOS Advisor: Stabilität, Balanced & Performance
**System-Ausrichtung:** AMD Ryzen 5 5600X | 32 GiB (2×16 GiB) G.Skill Aegis DDR4-3200 | NVIDIA GeForce RTX 2060 12GB | Gigabyte B550 AORUS Elite V2 (FIb)  
**Skript:** [scripts/bios_config_advisor.py](file:///run/media/julian/ML6/bios-re/scripts/bios_config_advisor.py)  
**Hardware-Profil:** [findings/system_hardware.json](file:///run/media/julian/ML6/bios-re/findings/system_hardware.json)  
**Live NVRAM Variable:** [findings/live_setup_var.bin](file:///run/media/julian/ML6/bios-re/findings/live_setup_var.bin)

---

## 1. Hardware-Erkennung & Status Quo (Live NVRAM Audit)

Das System wurde über `/proc/cpuinfo`, DMI-Sysfs, PCI-Bus und das Live-NVRAM (`/sys/firmware/efi/efivars/Setup-*`) vollständig analysiert:

* **Prozessor:** AMD Ryzen 5 5600X (Vermeer Zen 3, 6 Kerne / 12 Threads, Sockel AM4)
* **Mainboard:** Gigabyte B550 AORUS ELITE V2 (BIOS-Version FIb)
* **Grafikkarte:** NVIDIA GeForce RTX 2060 12GB (TU106, VBIOS mit Re-Size BAR Unterstützung)
* **Arbeitsspeicher:** 2 Module à 16 GiB (32 GiB Gesamt), **Dual-Rank (2R)**, G.Skill Aegis (`F4-3200C16-16GIS`).
  - *Nennspezifikation laut Hersteller:* DDR4-3200 CL16-18-18-38 bei 1.35V.
  - *Aktueller Zustand im Live-NVRAM:* **2133 MT/s JEDEC Fallback bei 1.20V!**

### 🚨 Befunde & Handlungsbedarf:
1. **Speicher-Bottleneck (-33% Durchsatz):** Da XMP im BIOS deaktiviert ist (`0x00`), läuft das System auf 2133 MT/s. Dadurch wird auch die AMD Infinity Fabric auf $FCLK = 1066\,\text{MHz}$ ausgebremst!
2. **GPU-Bottleneck (-5% bis -15% Min-FPS):** Re-Size BAR und Above 4G Decoding sind im BIOS deaktiviert (`0x00`), wodurch die RTX 2060 12GB nicht den gesamten VRAM für Direct Memory Access freigeben kann.
3. **Firmware-Dropper aktiv:** Die Gigabyte APP Center Download Funktion (WPBT `0x264`) steht auf `0x01` (Aktiv) und injiziert Treiber-Dropper in Windows.
4. **Anti-Freeze Idle:** Power Supply Idle Control steht auf `Auto` (`0x0F`), was bei Zen 3 vereinzelt zu C6-State Idle-Reboots führen kann.

---

## 2. Direkter 3-Wege-Profilvergleich

| Parameter / BIOS-Schalter | Live NVRAM (Aktuell) | Profil 1: STABILITÄT (Failsafe) | Profil 2: BALANCED (Empfohlenes Optimum) | Profil 3: PERFORMANCE (1:1 OC) |
|---|---|---|---|---|
| **Extreme Memory Profile (0x157)** | **Disabled (0)** | **Disabled (0)** | **Profile 1 (1)** *(G.Skill 3200 CL16)* | **Profile 1 (1)** *(als Basis)* |
| **Speichertakt / Teiler (0x159)** | Auto (2133 MT/s) | Auto (2133-3200 MT/s) | **Auto / 32.00 (DDR4-3200 MT/s)** | **36.00 (DDR4-3600 MT/s)** |
| **Infinity Fabric (FCLK)** | 1066 MHz | 1066 - 1600 MHz | **1600 MHz (Synchron 1:1)** | **1800 MHz (Synchron 1:1)** |
| **Gear Down Mode (0x166)** | Auto | **Enabled (1)** | **Enabled (1)** *(Pflicht bei 2R)* | **Enabled (1)** |
| **Command Rate (0x165)** | Auto | **2T** | **1T (mit GDM)** | **1T** |
| **VCORE SOC (0x1F2)** | Auto | Normal / 1.000V - 1.025V | **Normal / 1.025V - 1.050V** | **1.080V - 1.100V** |
| **DRAM Voltage (0x200)** | Auto (1.20V) | **1.200V (JEDEC)** | **1.350V (Hersteller XMP)** | **1.360V - 1.380V** |
| **CPPC (0x155) & Preferred Cores** | Auto | Auto | **Enabled (1)** | **Enabled (1)** |
| **Power Supply Idle (0x14F)** | Auto | **Typical Current Idle (0)** | **Typical Current Idle (0)** | **Typical Current Idle (0)** |
| **PBO / Curve Optimizer** | Stock | Disabled (Stock AMD) | **Auto (Stock PB2 bis 4.65 GHz)** | **Advanced / Negative Offset** |
| **Above 4G Decoding (0x27E)** | **Disabled (0)** | **Enabled (1)** | **Enabled (1)** | **Enabled (1)** |
| **Re-Size BAR Support (0x27F)** | **Disabled (0)** | Disabled / Auto | **Auto (1)** *(VRAM Aperture)* | **Auto (1)** |
| **CSM Support (0x218)** | **Disabled (0)** | **Disabled (0)** | **Disabled (0)** | **Disabled (0)** |
| **APP Center Download (0x264)** | **Enabled (1)** | **Disabled (0)** | **Disabled (0)** | **Disabled (0)** |
| **IOMMU (0x25F)** | Auto | **Enabled (1)** | **Enabled (1)** | **Enabled (1)** |

---

## 3. Die 3 Profile im Detail

### Profil 1: Maximale Stabilität (Failsafe / 24/7 Dauerbetrieb)
* **Zielgruppe:** Home-Server, ununterbrochene Kompilierläufe, Null-Fehlertoleranz.
* **Philosophie:** Verzicht auf jegliche Übertaktung. Betrieb der Module mit JEDEC-Standard (1.20V). Der 12nm I/O-Die bleibt bei ~1.00V eiskalt. Command Rate 2T schließt Timing-Verletzungen auf den Daisy-Chain-Leiterbahnen vollkommen aus.

### Profil 2: BALANCED (Gold Standard Daily Driver – Empfohlen)
* **Zielgruppe:** Der perfekte Alltags- und Gaming-PC für dieses spezifische System.
* **Philosophie:** Aktiviert die **exakte Nennspezifikation des verbauten G.Skill Aegis Kits** (DDR4-3200 CL16 @ 1.35V). Der Speichercontroller läuft im perfekten synchronen 1:1 Modus ($FCLK = 1600\,\text{MHz} : UCLK = 1600\,\text{MHz} : MCLK = 1600\,\text{MHz}$).
* **Sicherheits-Puffer:** Gear Down Mode bleibt aktiv, was bei zwei Dual-Rank-Modulen essenziell für dauerhafte Stabilität ist. PBO bleibt auf AMD-Standardgrenzen (keine Überhitzung).

### Profil 3: Maximale Performance (1:1 AM4 Sweet-Spot OC)
* **Zielgruppe:** Enthusiasten und Benchmarking.
* **Philosophie:** Erzwingt 1800 MHz Fabric-Takt (DDR4-3600 MT/s). 
* **Wichtiger Hinweis für dieses System:** Da die verbauten G.Skill Aegis Riegel für 3200 MT/s spezifiziert sind, erfordert dieses Profil eine Übertaktung der RAM-Chips mit manueller Erhöhung von VDIMM auf 1.36V–1.38V und VSOC auf 1.08V–1.10V.

---

## 4. Konkrete Klickanleitung im BIOS (für das Balanced-Profil)

Beim Neustart die Taste `Entf` (Delete) drücken, um ins BIOS zu gelangen.

### Schritt 1: XMP Profil 1 aktivieren
* Pfad: `M.I.T.` $\rightarrow$ `Advanced Memory Settings`
* Einstellung: `Extreme Memory Profile(X.M.P.)` $\rightarrow$ von **Disabled** auf **Profile 1** stellen.
* *(Effekt: RAM schaltet von 2133 MT/s auf 3200 MT/s @ 1.35V; FCLK springt auf 1600 MHz).*

### Schritt 2: Re-Size BAR & Above 4G Decoding aktivieren
* Pfad: `Peripherals`
* Einstellung 1: `Above 4G Decoding` $\rightarrow$ von **Disabled** auf **Enabled** stellen.
* Einstellung 2: `Re-Size BAR Support` $\rightarrow$ von **Disabled** auf **Auto** stellen.
* *(Effekt: Volle GPU-Speicherbeschleunigung für die RTX 2060 12GB).*

### Schritt 3: Power Supply Idle Control setzen
* Pfad: `M.I.T.` $\rightarrow$ `Advanced Frequency Settings` $\rightarrow$ `Advanced CPU Settings`
* Einstellung: `Power Supply Idle Control` $\rightarrow$ von **Auto** auf **Typical Current Idle** stellen.
* *(Effekt: Schützt vor seltenen C6-State Reboots im Leerlauf).*

### Schritt 4: Gigabyte APP Center Download deaktivieren
* Pfad: `Peripherals` $\rightarrow$ `APP Center Download & Install Configuration`
* Einstellung: `APP Center Download & Install` $\rightarrow$ von **Enabled** auf **Disabled** stellen.
* *(Effekt: Sauberes System ohne automatische Firmware-Dienst-Injektion).*

### Speichern & Beenden
* Taste `F10` drücken und mit `Enter` (Save & Exit Setup) bestätigen.
