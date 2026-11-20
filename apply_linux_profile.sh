#!/usr/bin/env bash
# apply_linux_profile.sh - Switches Linux CPU EPP, Governors, and GPU Power Management
set -euo pipefail

TARGET="${1:-status}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$TARGET" == "status" ]]; then
    python3 "$REPO_DIR/am4_advisor.py" --linux-profile status
    exit 0
fi

if [[ $EUID -ne 0 ]]; then
    echo "[!] Modifying sysfs CPU and GPU parameters requires root privileges."
    echo "    Restarting script with sudo..."
    exec sudo "$0" "$TARGET"
fi

python3 "$REPO_DIR/am4_advisor.py" --linux-profile "$TARGET"
