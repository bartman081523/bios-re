#!/usr/bin/env python3
"""
scripts/bios_config_advisor.py - Compatibility Shim pointing to toolkit
All logic is unified in toolkit/ and am4_advisor.py.
"""

import sys
from pathlib import Path

# Add repo root to search path
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from toolkit.advisor import BiosAdvisorSuite
import am4_advisor

if __name__ == "__main__":
    am4_advisor.main()
