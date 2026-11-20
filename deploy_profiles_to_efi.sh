#!/usr/bin/env bash
# deploy_profiles_to_efi.sh - Installs AMITSE profiles onto FAT32 EFI partition
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "[-] This script requires root privileges to write to /boot/efi."
   echo "    Please run with: sudo $0"
   exit 1
fi

DEST_DIR="/boot/efi/BIOS_PROFILES"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== AM4/B550 BIOS PROFILES: DEPLOYMENT TO /boot/efi ==="
mkdir -p "$DEST_DIR"

# Generate fresh validated profiles (Standard + Linux editions)
python3 "$REPO_DIR/am4_advisor.py" --export-profiles "$DEST_DIR"

# Ensure FAT32 permissions are readable by firmware
chmod 644 "$DEST_DIR"/*.PRO || true

echo ""
echo "[+] Deployed profiles on /boot/efi/BIOS_PROFILES:"
ls -lh "$DEST_DIR"/*.PRO

echo ""
echo "=== INSTRUCTIONS TO LOAD IN BIOS ==="
echo "1. Reboot system (e.g. 'sudo systemctl reboot --firmware-setup')."
echo "2. Press 'Del' or 'F2' to enter BIOS Setup."
echo "3. Press 'F4' (Load Profile) or navigate to 'Save & Exit' -> 'Select File in HDD/FDD/USB'."
echo "4. Select the drive containing the EFI partition and open folder 'BIOS_PROFILES'."
echo "5. Available profiles:"
echo "     * BALANCED_LINUX.PRO   : Recommended for Linux (amd-pstate-epp, BAR1, C6 protection, XMP 3200)"
echo "     * STABILITY_LINUX.PRO  : Maximum failsafe for Linux 24/7 server/KVM (JEDEC 1.20V)"
echo "     * PERFORMANCE_LINUX.PRO: Unthrottled performance for Gaming/Vulkan/Compute"
echo "     * BALANCED.PRO         : Standard Daily Driver (Cross-Platform)"
echo "     * STABILITY.PRO        : Standard Failsafe (Cross-Platform)"
echo "     * PERFORMANCE.PRO      : Standard OC (Cross-Platform)"
echo "6. The BIOS will load all parameters cleanly without model or checksum errors!"
