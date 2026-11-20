"""
toolkit/advisor.py - Unified Epistemic AM4/B550 Advisor & Linux Compatibility Engine
Coordinates Hardware Detection, Live NVRAM Audit, Multi-Vendor Translation,
Linux Kernel Telemetry, UEFI Profile Export, and Linux OS Runtime Profile Management.
"""

import sys
import subprocess
from pathlib import Path
from .hardware import PlatformDetector
from .nvram import NvramManager
from .profiles import ProfileGenerator
from .vendor_maps import VendorResolver
from .linux_audit import LinuxKernelAudit
from .linux_runtime import LinuxRuntimeManager

class BiosAdvisorSuite:
    def __init__(self, image_path=None, linux_mode=False):
        self.hw = PlatformDetector.get_profile(image_path=image_path)
        self.nvram = NvramManager(dump_path=image_path)
        self.board_key = self.hw.board.get("vendor_key", "gigabyte")
        self.taxonomy = VendorResolver.get_taxonomy(self.hw.board.get("vendor"), self.board_key)
        self.linux_mode = linux_mode

    def print_banner(self):
        print("=" * 100)
        print(f" [AM4 / B550 BIOSTOOLKIT: HARDWARE DETECTION & TARGET PLATFORM]")
        print("=" * 100)
        print(f" CPU            : {self.hw.cpu.get('model')} ({self.hw.cpu.get('architecture')}, {self.hw.cpu.get('threads')} Threads)")
        print(f" Detected Board : {self.hw.board.get('vendor')} {self.hw.board.get('name')} (BIOS {self.hw.board.get('bios_version')})")
        print(f" Target Layout  : {self.taxonomy['display_name']} [Key Mode: {self.taxonomy['menu_mode_toggle']}]")
        for g in self.hw.gpu:
            print(f" GPU            : {g}")
        
        print(f" Installed RAM  : {len(self.hw.memory)} modules ({self.hw.total_memory_gb} GiB Total)")
        for idx, m in enumerate(self.hw.memory, 1):
            rank_str = "Dual-Rank (2R)" if m.get("rank") == "2" else "Single-Rank (1R)"
            print(f"   * Slot {idx} ({m.get('locator')}): {m.get('size_gb')} GiB | {m.get('part')} ({rank_str}) | Rated XMP: {m.get('rated_speed')} MT/s -> Active: {m.get('active_speed')} MT/s")

        print("\n" + "-" * 100)
        print(" [ACTIVE BOTTLENECK ANALYSIS FROM LIVE NVRAM]")
        print("-" * 100)

        xmp_val = self.nvram.get_byte(0x157)
        if xmp_val == 0:
            print(f" [!] RAM THROTTLED: XMP/DOCP is Disabled (0x00). Modules running at JEDEC {self.hw.active_memory_speed} MT/s instead of {self.hw.rated_xmp_speed} MT/s (-33% bandwidth loss!).")
        else:
            print(f" [+] RAM OPTIMAL: XMP/DOCP active ({self.hw.rated_xmp_speed} MT/s @ 1:1 FCLK).")

        cpb_val = self.nvram.get_byte(0x146)
        if cpb_val == 0:
            print(f" [!] CPU BOOST CAPPED: Core Performance Boost is Disabled (0x00). CPU locked at {self.hw.cpu.get('base_mhz')/1000:.2f} GHz base clock!")
        else:
            print(f" [+] CPU BOOST ACTIVE: Precision Boost 2 scaling up to {self.hw.cpu.get('boost_target_mhz')/1000:.2f} GHz.")

        bar_val = self.nvram.get_byte(0x27F)
        above4g_val = self.nvram.get_byte(0x27E)
        if bar_val == 0 or above4g_val == 0:
            print(" [!] GPU VRAM CONSTRAINED: Re-Size BAR / Above 4G Decoding is Disabled (0x00).")

        wpbt_val = self.nvram.get_byte(0x264)
        if wpbt_val == 1:
            dropper_name = "ASUS Armoury Crate" if self.board_key == "asus" else "Gigabyte APP Center"
            print(f" [!] FIRMWARE DROPPER: {dropper_name} (WPBT) is Enabled (0x01).")

        print("=" * 100 + "\n")

    def print_linux_audit(self):
        telemetry, findings = LinuxKernelAudit.audit_nvram_for_linux(self.nvram)
        print("=" * 100)
        print(" [LINUX KERNEL & DRIVER COMPATIBILITY AUDIT (--linux)]")
        print("=" * 100)
        print(f" Kernel Version : {telemetry['kernel_version']}")
        print(f" CPUFreq Driver : {telemetry['scaling_driver']} " + ("(Optimal: Hardware Autonomous CPPC)" if telemetry['has_amd_pstate'] else "(Legacy)"))
        print(f" Kernel Cmdline : {telemetry['cmdline']}")
        if telemetry['has_iommu_soft']:
            print(" [!] KERNEL NOTICE: 'iommu=soft' active -> Linux using slow software bounce buffers (SWIOTLB) instead of hardware IOMMU!")
        print("-" * 100 + "\n")

        crit = [f for f in findings if f["severity"] == "CRITICAL"]
        warn = [f for f in findings if f["severity"] in ("WARNING", "PERFORMANCE", "HYGIENE")]
        opt  = [f for f in findings if f["severity"] == "OPTIMAL"]

        if crit:
            print("🚨 CRITICAL LINUX STABILITY RISKS:")
            for f in crit:
                print(f"  * {f['param']} (Live: {f['live_val']} -> Target: {f['target_val']})")
                for line in f["impact"].splitlines():
                    print(f"      {line}")
            print()

        if warn:
            print("⚠️  LINUX PERFORMANCE & DRIVER OPTIMIZATIONS:")
            for f in warn:
                print(f"  * [{f['severity']}] {f['param']} (Live: {f['live_val']} -> Target: {f['target_val']})")
                for line in f["impact"].splitlines():
                    print(f"      {line}")
            print()

        if opt:
            print("✅ ALREADY OPTIMAL FOR LINUX:")
            for f in opt:
                print(f"  * {f['param']}: {f['impact']}")
            print()

        print("=" * 100 + "\n")

    def print_delta(self, profile_name="balanced"):
        deltas = ProfileGenerator.get_profile_deltas(profile_name, self.hw, linux_mode=self.linux_mode)
        mode_label = "LINUX-OPTIMIZED " if self.linux_mode else ""
        print("=" * 100)
        print(f" [STEP-BY-STEP BIOS WALKTHROUGH: {mode_label}{profile_name.upper()} PROFILE]")
        print(f" Target Board : {self.hw.board.get('vendor')} {self.hw.board.get('name')} ({self.taxonomy['display_name']})")
        print(f" Keyboard Mode: {self.taxonomy['menu_mode_toggle']}")
        print("=" * 100 + "\n")

        needed_deltas = []
        for d in deltas:
            live_val = self.nvram.get_byte(d["offset"])
            if live_val is None or live_val != d["target_val"]:
                needed_deltas.append(d)

        if not needed_deltas:
            print("✅ All parameters already match the target values for this profile!\n")
            return

        for idx, item in enumerate(needed_deltas, 1):
            live_val = self.nvram.get_byte(item["offset"])
            live_str = f"0x{live_val:02X}" if live_val is not None else "Unknown"
            translated = VendorResolver.translate_delta(item, self.taxonomy)

            print(f"STEP {idx}: {translated['name']}")
            print(f"  Category   : {translated['category']}")
            print(f"  Menu Path  : {translated['menu_path']}")
            print(f"  Live Value : {live_str}")
            print(f"  Action     : {translated['action']}")
            print(f"  Rationale  :")
            for w_line in translated['why'].splitlines():
                print(f"     {w_line}")
            print("-" * 100)

        print("\n" + "=" * 100)
        print(f" [SAVE CHANGES & EXIT]")
        print("=" * 100)
        print(f" 1. Press {self.taxonomy['save_and_exit_key']} ({self.taxonomy['save_and_exit_menu']}).")
        print(" 2. Confirm with 'Yes' / 'Enter'.")
        print("=" * 100 + "\n")

    def print_delta_balanced(self):
        self.print_delta("balanced")

    def print_comparison(self):
        deltas = ProfileGenerator.build_balanced_deltas(self.hw, linux_mode=self.linux_mode)
        mode_label = "LINUX " if self.linux_mode else ""
        print("=" * 100)
        print(f" [3-WAY COMPARISON: LIVE NVRAM vs. {mode_label}BALANCED PROFILE vs. TARGET]")
        print("=" * 100)
        print(f"{'PARAMETER':<36} | {'LIVE VALUE':<12} | {'BALANCED TARGET':<24} | {'STATUS'}")
        print("-" * 100)
        for d in deltas:
            live = self.nvram.get_byte(d["offset"])
            live_str = f"0x{live:02X}" if live is not None else "N/A"
            target_str = f"0x{d['target_val']:02X} ({d['target_str'][:16]})"
            status = "MATCH" if live == d["target_val"] else "DELTA"
            print(f"{d['name']:<36} | {live_str:<12} | {target_str:<24} | {status}")
        print("=" * 100 + "\n")

    def export_profiles(self, target_dir="/boot/efi/BIOS_PROFILES"):
        from .profile_exporter import ProfileExporter
        dest = target_dir or "/boot/efi/BIOS_PROFILES"
        print("=" * 100)
        print(f" [AMITSE BIOS PROFILE GENERATOR & FAT32 EFI EXPORTER]")
        print("=" * 100)
        print(f" Target Board    : {self.hw.board.get('vendor')} {self.hw.board.get('name')} (BIOS {self.hw.board.get('bios_version')})")
        print(f" Target Directory: {dest}")
        print(f" Export Scope    : Standard Profiles + Dedicated Linux Kernel 6.x Editions")
        print("-" * 100 + "\n")

        results, write_allowed = ProfileExporter.export_all(dest, self.hw, linux_only=False)

        for r in results:
            status_icon = "🐧" if r.get("is_linux") else "✅"
            print(f" {status_icon} Profile Generated: {r['filename']:<22} ({r['size']} Bytes)")
            print(f"    * Description : {r['description']}")
            print(f"    * AMITSE Hdr  : Magic 0x1964 | Checksum 0x{r['checksum']:02x} | Model: {r['model_id']} | Version: {r['bios_version']}")
            print(f"    * Validation  : {r['status_msg']}")
            print(f"    * Local Path  : {r['local_path']}")
            if r['dest_path']:
                print(f"    * EFI Path    : {r['dest_path']}")
            print()

        print("-" * 100)
        if write_allowed:
            print(f" [+] All profiles successfully written directly to the FAT32 EFI Partition ({dest})!")
            print(" [i] How to load in BIOS:")
            print(f"     1. Reboot PC and press 'Del' / 'F2' to enter BIOS Setup.")
            print(f"     2. Press 'F4' (Load Profile) or navigate to 'Save & Exit' -> 'Select File in HDD/FDD/USB'.")
            print(f"     3. Select the EFI system partition and open folder '{Path(dest).name}'.")
            print(f"     4. Choose 'BALANCED_LINUX.PRO' (or STABILITY_LINUX / PERFORMANCE_LINUX) and press Enter.")
            print(f"     5. All settings will load cleanly into the setup forms!")
        else:
            print(f" [!] Writing to '{dest}' requires root privileges (current permissions: non-root).")
            print(f" [+] All profiles verified and generated locally in './profiles/':")
            for r in results:
                print(f"       * {r['local_path']}")
            print(f"\n [>] To copy profiles to the EFI partition, run:")
            print(f"       sudo mkdir -p {dest} && sudo cp ./profiles/*.PRO {dest}/")
            print(f"     Or run the advisor with sudo:")
            print(f"       sudo ./am4_advisor.py --export-profiles {dest}")
        print("=" * 100 + "\n")

    def manage_linux_runtime(self, target_profile=None):
        LinuxRuntimeManager.print_status_and_profiles(target_apply=target_profile)
