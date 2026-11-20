"""
toolkit/linux_runtime.py - Linux OS Runtime Engine for Epistemic Profiles
Controls runtime CPU frequency governors, energy-performance preferences (EPP),
GPU power states, and kernel telemetry on running Linux systems.

Profiles:
- STABILITY:   Governor powersave, EPP balance_power / power (Thermal & Failsafe Priority)
- BALANCED:    Governor powersave, EPP balance_performance (AMD Zen 3 Sweet-Spot)
- PERFORMANCE: Governor performance, EPP performance, GPU Persistence Mode (Zero-Latency)
"""

import os
import subprocess
from pathlib import Path

class LinuxRuntimeManager:
    PROFILES = {
        "stability": {
            "name": "Stability / Power-Failsafe",
            "governor": "powersave",
            "epp": "balance_power",
            "gpu_persistence": False,
            "description": "Lowest heat generation, reduced boost aggressiveness, rock-solid for continuous workloads."
        },
        "balanced": {
            "name": "Balanced (Gold-Standard Daily Driver)",
            "governor": "powersave",
            "epp": "balance_performance",
            "gpu_persistence": False,
            "description": "Official AMD Zen 3 Linux sweet spot: Full 4.65 GHz boost with minimal idle power draw."
        },
        "performance": {
            "name": "Performance / Ultra-Low-Latency",
            "governor": "performance",
            "epp": "performance",
            "gpu_persistence": True,
            "description": "Locks clocks at maximum, eliminates C-state wake latencies, GPU driver persistent in VRAM."
        }
    }

    @classmethod
    def get_status(cls):
        status = {
            "cpus": 0,
            "scaling_driver": "Unknown",
            "current_governor": "Unknown",
            "current_epp": "Unknown",
            "available_epp": [],
            "available_governors": [],
            "gpu_persistence": "Unknown",
            "cmdline_has_iommu_soft": False,
            "cmdline": ""
        }

        # CPU info
        cpu0_dir = Path("/sys/devices/system/cpu/cpu0/cpufreq")
        if cpu0_dir.exists():
            p_driver = cpu0_dir / "scaling_driver"
            if p_driver.exists():
                status["scaling_driver"] = p_driver.read_text().strip()

            p_gov = cpu0_dir / "scaling_governor"
            if p_gov.exists():
                status["current_governor"] = p_gov.read_text().strip()

            p_epp = cpu0_dir / "energy_performance_preference"
            if p_epp.exists():
                status["current_epp"] = p_epp.read_text().strip()

            p_avail_epp = cpu0_dir / "energy_performance_available_preferences"
            if p_avail_epp.exists():
                status["available_epp"] = p_avail_epp.read_text().split()

            p_avail_gov = cpu0_dir / "scaling_available_governors"
            if p_avail_gov.exists():
                status["available_governors"] = p_avail_gov.read_text().split()

        # Count online CPUs
        cpu_dirs = list(Path("/sys/devices/system/cpu").glob("cpu[0-9]*"))
        status["cpus"] = len(cpu_dirs)

        # GPU persistence mode
        try:
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=persistence_mode", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=2
            )
            if res.returncode == 0:
                status["gpu_persistence"] = res.stdout.strip()
        except Exception:
            pass

        # Kernel cmdline
        p_cmd = Path("/proc/cmdline")
        if p_cmd.exists():
            cmd = p_cmd.read_text().strip()
            status["cmdline"] = cmd
            status["cmdline_has_iommu_soft"] = "iommu=soft" in cmd

        return status

    @classmethod
    def apply_profile(cls, profile_name: str):
        p_name = profile_name.lower()
        if p_name not in cls.PROFILES:
            raise ValueError(f"Unknown profile '{profile_name}'. Available: {list(cls.PROFILES.keys())}")

        cfg = cls.PROFILES[p_name]
        is_root = (os.geteuid() == 0)
        actions = []
        commands_needed = []

        # 1. Apply EPP across all CPUs
        target_epp = cfg["epp"]
        epp_paths = list(Path("/sys/devices/system/cpu").glob("cpu[0-9]*/cpufreq/energy_performance_preference"))
        epp_success = 0
        for p in epp_paths:
            if is_root:
                try:
                    p.write_text(target_epp)
                    epp_success += 1
                except Exception:
                    pass
        if epp_paths:
            if is_root and epp_success == len(epp_paths):
                actions.append(f"CPU EPP set to '{target_epp}' across all {epp_success} cores.")
            else:
                commands_needed.append(f"echo {target_epp} | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference > /dev/null")

        # 2. Apply Governor
        target_gov = cfg["governor"]
        gov_paths = list(Path("/sys/devices/system/cpu").glob("cpu[0-9]*/cpufreq/scaling_governor"))
        gov_success = 0
        for p in gov_paths:
            if is_root:
                try:
                    p.write_text(target_gov)
                    gov_success += 1
                except Exception:
                    pass
        if gov_paths:
            if is_root and gov_success == len(gov_paths):
                actions.append(f"CPU Governor set to '{target_gov}' across all {gov_success} cores.")
            else:
                commands_needed.append(f"echo {target_gov} | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null")

        # 3. Apply GPU persistence mode
        if cfg["gpu_persistence"]:
            if is_root:
                try:
                    subprocess.run(["nvidia-smi", "-pm", "1"], capture_output=True, check=True)
                    actions.append("NVIDIA Persistence Mode activated (-pm 1).")
                except Exception:
                    commands_needed.append("sudo nvidia-smi -pm 1")
            else:
                commands_needed.append("sudo nvidia-smi -pm 1")
        else:
            if is_root:
                try:
                    subprocess.run(["nvidia-smi", "-pm", "0"], capture_output=True)
                    actions.append("NVIDIA Persistence Mode deactivated (default dynamic power saving).")
                except Exception:
                    pass

        return {
            "profile": p_name,
            "config": cfg,
            "applied_immediately": is_root and len(commands_needed) == 0,
            "actions": actions,
            "commands_needed": commands_needed
        }

    @classmethod
    def print_status_and_profiles(cls, target_apply=None):
        status = cls.get_status()
        print("=" * 100)
        print(" [LINUX OS RUNTIME ENGINE: CPU, DRIVER & POWER PROFILES]")
        print("=" * 100)
        print(f" CPU Cores / Threads: {status['cpus']}")
        print(f" CPU Scaling Driver : {status['scaling_driver']} (Optimal: amd-pstate-epp)")
        print(f" Active Governor    : {status['current_governor']}")
        print(f" Active EPP         : {status['current_epp']}")
        print(f" Available EPP      : {', '.join(status['available_epp'])}")
        print(f" GPU Persistence    : {status['gpu_persistence']}")
        if status["cmdline_has_iommu_soft"]:
            print(" [!] Kernel Cmdline  : 'iommu=soft' active (SWIOTLB bounce buffers degrade DMA performance)")
        print("-" * 100 + "\n")

        print("AVAILABLE LINUX RUNTIME PROFILES:")
        for key, p in cls.PROFILES.items():
            active_marker = " [ACTIVE]" if (p["epp"] == status["current_epp"] and p["governor"] == status["current_governor"]) else ""
            print(f"  * {key.upper():<12}: {p['name']}{active_marker}")
            print(f"      Governor: {p['governor']:<12} | EPP: {p['epp']:<20} | GPU-PM: {p['gpu_persistence']}")
            print(f"      Purpose : {p['description']}")
        print()

        if target_apply:
            res = cls.apply_profile(target_apply)
            print("-" * 100)
            if res["applied_immediately"]:
                print(f" [+] Profile '{target_apply.upper()}' successfully applied to the Linux system!")
                for a in res["actions"]:
                    print(f"     * {a}")
            else:
                print(f" [!] Applying profile '{target_apply.upper()}' requires root privileges.")
                print(f" [>] Execute the following commands:")
                for cmd in res["commands_needed"]:
                    print(f"       {cmd}")
                print(f"     Or run directly with sudo: sudo ./am4_advisor.py --linux-profile {target_apply}")
            print("-" * 100)
        print("=" * 100 + "\n")
