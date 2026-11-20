# AM4 / B550 Linux Kernel & Treiber-Kompatibilitäts-Audit
**Ziel-Architektur:** AMD AM4 (Zen 2 / Zen 3) auf B550 / X570 Chipsätzen  
**Geprüfte Kernel-Version:** Linux 6.x LTS (`amd-pstate-epp`, `amdgpu`, `nvidia`, `amd_iommu`)  
**Toolkit-Schalter:** `./am4_advisor.py --linux`

---

## 1. Übersicht: Die 7 kritischen Linux-Parameter im AM4-BIOS

Linux interagiert über ACPI, cpuidle, cpufreq und das PCI-Subsystem direkt mit den BIOS-Registern. Falsche Werkseinstellungen führen unter Linux häufiger zu Abstürzen oder Performanceverlusten als unter Windows.

| Parameter / BIOS-Schalter | Linux-Optimalwert | Relevanter Kernel-Treiber | Konsequenz bei falscher Einstellung unter Linux |
|---|---|---|---|
| **Power Supply Idle Control** | **`Typical Current Idle`** | `cpuidle` / `acpi_idle` / `mce` | **Spontane Kernel-Panics & MCE-Freezes** im Leerlauf oder beim Browsen durch Spannungsabfall unter 0.05A. |
| **Core Performance Boost (CPB)** | **`Auto`** | `amd-pstate-epp` / `cpufreq` | **CPU bleibt auf Basistakt (3,7 GHz)** fixiert. Kein dynamischer Boost auf 4,65 GHz. |
| **CPPC & CPPC Preferred Cores** | **`Enabled`** | `amd-pstate-epp` / scheduler | Kernel fällt auf den langsamen Legacy-Treiber `acpi-cpufreq` zurück. |
| **Above 4G Decoding** | **`Enabled`** | `pci` / `drm` / `nvidia` | Treiber meldet `No more than 256MB for BAR1`. Zwingende Voraussetzung für Re-Size BAR. |
| **Re-Size BAR Support** | **`Auto`** | `drm` / `amdgpu` / `nvidia` | Voller 12GB VRAM-Direktzugriff. Steigert minimale Frameraten unter Proton/Vulkan um 5–15%. |
| **AMD IOMMU** | **`Enabled`** | `amd_iommu` / `vfio` | Kernel fällt auf langsame Software-Bounce-Buffer (`iommu=soft` / SWIOTLB) zurück. PCI-Passthrough in KVM scheitert. |
| **CSM Support** | **`Disabled`** | `efifb` / `simpledrm` | Legacy 16-Bit VESA Option ROMs kollidieren mit Kernel-GOP-Framebuffer. Suspend/Resume-Probleme. |
| **Fast Boot** | **`Disabled`** | `nvme` / `ahci` | NVMe-SSDs werden bei Warmstart gelegentlich nicht erkannt (`device not ready`). Dual-Boot-Dateisystemschäden. |
| **APP Center / Armoury (WPBT)**| **`Disabled`** | `acpi` | Unnötige ACPI WPBT-Fehlermeldungen im Kernel-Log (`dmesg`). |

---

## 2. Detaillierte Kernel-Befunde & Ursachenforschung

### 2.1 C6-State Idle Freeze (`Power Supply Idle Control`)
* **Hintergrund:** Der Linux-Kernel schaltet ungenutzte Zen-Kerne aggressiver in tiefe Ruhezustände (`C6`). Bei Netzteilen, die minimale Restströme (< 0.05A) nicht vollkommen glätten, bricht die Spannung am Core-VRM kurzzeitig ein.
* **Symptom:** Der Rechner friert ohne Bluescreen ein oder startet neu, meist bei geringer Last (z. B. YouTube-Video im Browser, Leerlauf im Terminal).
* **Lösung:** `Power Supply Idle Control = Typical Current Idle`. Verhindert das Absinken des Ruhestroms unter den kritischen Schwellenwert.

### 2.2 Moderner CPU-Governor: `amd-pstate-epp` vs. `acpi-cpufreq`
* **Hintergrund:** Seit Linux 5.17 / 6.0 unterstützt Linux den nativen `amd-pstate-epp` (Energy-Performance Preference) Treiber, der die Autonomie des CPU-internen Power-Managements nutzt.
* **Bedingung:** `CPPC` (Collaborative Power and Performance Control) und `Core Performance Boost` müssen im BIOS aktiv sein.
* **Prüfung:** `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver` muss `amd-pstate-epp` melden.

### 2.3 IOMMU Hardware-Remapping vs. `iommu=soft` (SWIOTLB)
* **Hintergrund:** Wenn IOMMU im BIOS auf `Auto` steht und nicht forciert wird, startet Linux oft mit `iommu=soft` (wie auf diesem System festgestellt).
* **Nachteil:** Daten müssen durch Software-Bounce-Buffer (SWIOTLB) im Hauptspeicher kopiert werden, was Latenz erzeugt und KVM-Gerätedurchreichung (VFIO) blockiert.
* **Lösung:** `AMD IOMMU = Enabled` im BIOS.

---

## 3. Kombinations-Aufrufe mit dem Toolkit

```bash
# Standardmäßiger Linux-Audit auf aktuellem Board:
./am4_advisor.py --linux

# 3-Wege-Vergleich inklusive Linux-Sollwerten:
./am4_advisor.py --compare --linux

# Linux-Delta übersetzt auf ASUS B550 (TUF / PRIME):
./am4_advisor.py --board asus --linux

# Schneller Neustart direkt ins BIOS:
./am4_advisor.py --reboot
```
