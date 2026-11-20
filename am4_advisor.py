#!/usr/bin/env python3
"""
am4_advisor.py - Universal AM4 / B550 Epistemic BIOS Engineering Suite
Multi-Board Support: Gigabyte, ASUS, MSI, ASRock
Integrated Linux Kernel Audit Engine (--linux)
AMITSE UEFI Binary Profile Generator & EFI Exporter (--export-profiles)
Linux OS Runtime Profile Engine (--linux-profile)

Usage Examples:
  ./am4_advisor.py                                # Default: Full Balanced delta walkthrough for detected board
  ./am4_advisor.py --linux                        # Balanced delta with Linux kernel & driver audit
  ./am4_advisor.py --export-profiles              # Generates verified AMITSE .PRO files (incl. Linux editions)
  ./am4_advisor.py --linux-profile                # Displays active Linux CPU governor / EPP / GPU status
  ./am4_advisor.py --linux-profile balanced       # Switches Linux kernel runtime to balanced (amd-pstate-epp)
  ./am4_advisor.py --linux-profile performance    # Switches Linux runtime to unthrottled maximum performance
  ./am4_advisor.py --reboot                       # Reboots PC directly into BIOS setup
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Add repo root to module search path
sys.path.insert(0, str(Path(__file__).parent))

from toolkit.advisor import BiosAdvisorSuite

def main():
    parser = argparse.ArgumentParser(
        description="Universal AM4 / B550 Epistemic BIOS Advisor Suite (Autonomous Board Detection, Linux Engine & Profile Exporter)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Autonomous Board Detection & Linux Control:
  The suite automatically identifies the motherboard vendor (Gigabyte, ASUS, MSI, ASRock)
  and adapts menu paths directly from live DMI/NVRAM or from an image file (--image).
  With --export-profiles, both standard and Linux-hardened AMITSE profiles (.PRO)
  are exported for direct import from FAT32 EFI partitions in BIOS Setup.
  With --linux-profile, the active Linux OS runtime can be switched in real time.

Examples:
  ./am4_advisor.py                                # Default: Complete Balanced delta for live board
  ./am4_advisor.py --linux                        # Includes Linux kernel audit (amd-pstate, BAR1, C6-freeze)
  ./am4_advisor.py --export-profiles              # Builds STABILITY, BALANCED, PERFORMANCE (+ Linux editions)
  ./am4_advisor.py --linux-profile performance    # Sets Linux EPP and GPU to maximum performance
  ./am4_advisor.py --reboot                       # Boots directly into UEFI BIOS setup
"""
    )
    parser.add_argument("--delta", "-d", action="store_true", default=False,
                        help="Outputs the step-by-step delta walkthrough for the target profile (default action)")
    parser.add_argument("--compare", "-c", action="store_true", default=False,
                        help="Displays 3-way comparison matrix against live NVRAM")
    parser.add_argument("--linux", "-l", action="store_true", default=False,
                        help="Enables Linux kernel & driver audit (checks amd-pstate-epp, C6 freezes, IOMMU, Re-Size BAR)")
    parser.add_argument("--image", "-i", type=str, default=None,
                        help="Path to a BIOS ROM file (.CAP, .bin, .rom, .FIb) for static analysis and vendor derivation")
    parser.add_argument("--profile", "-p", choices=["stability", "balanced", "performance"], default="balanced",
                        help="Selects the target profile for delta output (default: balanced)")
    parser.add_argument("--export-profiles", "-e", nargs="?", const="/boot/efi/BIOS_PROFILES", default=None,
                        help="Generates verified AMITSE profile binaries (.PRO incl. Linux editions) for FAT32 EFI partitions")
    parser.add_argument("--linux-profile", "-lp", nargs="?", const="status", default=None,
                        choices=["status", "stability", "balanced", "performance"],
                        help="Manages Linux OS runtime profile (CPU EPP, governor, GPU persistence). Without value: show status.")
    parser.add_argument("--detect", action="store_true", default=False,
                        help="Executes hardware and bottleneck detection only")
    parser.add_argument("--reboot", action="store_true", default=False,
                        help="Reboots PC directly into BIOS setup (systemctl reboot --firmware-setup)")

    args = parser.parse_args()

    suite = BiosAdvisorSuite(
        image_path=args.image,
        linux_mode=args.linux
    )

    if args.reboot:
        print("[*] Rebooting system directly into BIOS setup...")
        try:
            subprocess.run(["systemctl", "reboot", "--firmware-setup"], check=True)
        except Exception as e:
            print(f"[-] Reboot failed: {e}. Execute 'sudo systemctl reboot --firmware-setup' manually.")
        return

    # Print banner
    suite.print_banner()

    # If linux mode is requested, print Linux kernel audit
    if args.linux:
        suite.print_linux_audit()

    if args.linux_profile is not None:
        target = None if args.linux_profile == "status" else args.linux_profile
        suite.manage_linux_runtime(target_profile=target)
        return

    if args.export_profiles is not None:
        suite.export_profiles(target_dir=args.export_profiles)
        return

    if args.detect:
        return

    if args.compare:
        suite.print_comparison()
        return

    # Default action: full delta for selected profile
    suite.print_delta(args.profile)

if __name__ == "__main__":
    main()
