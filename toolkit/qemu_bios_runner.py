#!/usr/bin/env python3
"""
Universal BIOS / Firmware Execution Runner for QEMU (qemu-mod).
Supports both Modern UEFI Firmware (B550 / AM4 / OVMF) and Legacy PC BIOS (Phoenix / Award / AMI).

Features:
- Automatic image format detection (UEFI Firmware Volume vs Legacy x86 Reset Vector)
- Tailored QEMU topologies (q35 + pflash + debugcon for UEFI; pc + bios + in_asm/trace for Legacy)
- Controlled execution with configurable timeout (no indefinite hangs)
- Execution metric extraction (instruction traces, basic blocks, POST milestones)
- Structured JSON and CLI output
"""

import os
import sys
import time
import json
import struct
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class BiosImageDetector:
    """Analyzes a ROM binary to classify firmware type and entry points."""

    @staticmethod
    def inspect(image_path: Path) -> Dict[str, Any]:
        size = image_path.stat().st_size
        with open(image_path, "rb") as f:
            head = f.read(4096)
            f.seek(max(0, size - 128))
            tail = f.read(128)

        # 1. Check for standalone PE32 PEIM binary
        is_peim = False
        if (image_path.name.endswith(".pe.bin") or image_path.name.endswith(".pe") or image_path.name.endswith(".efi")) and size < 2 * 1024 * 1024:
            if head[:2] == b"MZ" or b"PE\x00\x00" in head[:512]:
                is_peim = True

        # 2. Check for UEFI Firmware Volume (_FVH at offset 0x28 within FVs)
        is_uefi = False
        uefi_sig_offset = -1
        with open(image_path, "rb") as f:
            rom_data = f.read()
            idx = rom_data.find(b"_FVH")
            if idx != -1:
                is_uefi = True
                uefi_sig_offset = idx

        # 3. Check for Phoenix BCP structures
        is_phoenix = False
        if b"BCPSYS" in rom_data or b"BCPSEGMENT" in rom_data:
            is_phoenix = True

        # 4. Check for Legacy x86 Reset Vector at (size - 16)
        reset_vec_bytes = tail[-16:] if len(tail) >= 16 else b""
        reset_opcode = reset_vec_bytes[0] if reset_vec_bytes else 0
        has_reset_vector = reset_opcode in (0xE9, 0xEA)

        reset_target = "UNKNOWN"
        if has_reset_vector:
            if reset_opcode == 0xE9 and len(reset_vec_bytes) >= 3:
                rel = struct.unpack("<h", reset_vec_bytes[1:3])[0]
                target_ip = (0xFFF0 + 3 + rel) & 0xFFFF
                reset_target = f"F000:{target_ip:04X}"
            elif reset_opcode == 0xEA and len(reset_vec_bytes) >= 5:
                off, seg = struct.unpack("<HH", reset_vec_bytes[1:5])
                reset_target = f"{seg:04X}:{off:04X}"

        if is_peim:
            mode = "peim"
        elif is_uefi and size >= 2 * 1024 * 1024:
            mode = "uefi"
        else:
            mode = "legacy"

        return {
            "path": str(image_path.resolve()),
            "size": size,
            "mode": mode,
            "is_peim": is_peim,
            "is_uefi": is_uefi,
            "is_phoenix": is_phoenix,
            "uefi_sig_offset": uefi_sig_offset,
            "has_reset_vector": has_reset_vector,
            "reset_opcode": hex(reset_opcode),
            "reset_target": reset_target,
            "reset_bytes": reset_vec_bytes.hex(),
        }


class QemuBiosRunner:
    """Orchestrates QEMU and Unicorn invocation, timeout monitoring, and log extraction."""

    def __init__(
        self,
        image_path: Path,
        mode: str = "auto",
        timeout: float = 3.0,
        work_dir: Optional[Path] = None,
        enable_gdb: bool = False,
        gdb_port: int = 1234,
    ):
        self.image_path = image_path.resolve()
        self.timeout = timeout
        self.work_dir = work_dir or Path("/tmp/qemu_bios_runner")
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.enable_gdb = enable_gdb
        self.gdb_port = gdb_port
        self.info = BiosImageDetector.inspect(self.image_path)
        self.mode = self.info["mode"] if mode == "auto" else mode

    def build_qemu_cmd(self, log_path: Path) -> List[str]:
        if self.mode == "peim":
            # Direct 32-bit PEIM execution via Unicorn harness
            harness_py = Path("/run/media/julian/ML6/uefi-peim-harness/unicorn_peim.py")
            if not harness_py.exists():
                harness_py = Path(__file__).resolve().parent.parent / "scratches" / "unicorn_peim.py"
            return ["python3", str(harness_py), str(self.image_path), "200000"]

        if self.mode == "uefi":
            # UEFI mode from ML6/bios-re: q35, split pflash (CODE + VARS), optional FAT ESP, debugcon
            vars_template = Path("/run/media/julian/ML6/edk2/Build/Ovmf3264/DEBUG_GCC/FV/OVMF_VARS.fd")
            if not vars_template.exists():
                vars_template = Path("/usr/share/edk2/x64/OVMF_VARS.4m.fd")

            # Dedicated VARS copy in work_dir so flash state is writable
            local_vars = self.work_dir / "OVMF_VARS.fd"
            if vars_template.exists() and not local_vars.exists():
                import shutil
                shutil.copyfile(vars_template, local_vars)

            # Optional FAT ESP drive with systemd-bootx64.efi
            esp_dir = self.work_dir / "esp" / "EFI" / "BOOT"
            esp_dir.mkdir(parents=True, exist_ok=True)
            bootx64 = esp_dir / "BOOTX64.EFI"
            systemd_boot = Path("/usr/lib/systemd/boot/efi/systemd-bootx64.efi")
            if systemd_boot.exists() and not bootx64.exists():
                import shutil
                shutil.copyfile(systemd_boot, bootx64)

            cmd = [
                "qemu-system-x86_64",
                "-accel", "tcg",
                "-M", "q35",
                "-m", "512M",
                "-nographic",
                "-net", "none",
                "-no-reboot",
                "-drive", f"if=pflash,format=raw,readonly=on,file={self.image_path}",
            ]
            if local_vars.exists():
                cmd.extend(["-drive", f"if=pflash,format=raw,file={local_vars}"])
            if (self.work_dir / "esp").exists():
                cmd.extend(["-drive", f"file=fat:rw:{self.work_dir / 'esp'},format=raw"])

            cmd.extend([
                "-debugcon", f"file:{log_path}",
                "-global", "isa-debugcon.iobase=0x402",
            ])
        else:
            # Legacy mode: qemu-system-i386, PC machine, -bios, in_asm trace
            cmd = [
                "qemu-system-i386",
                "-accel", "tcg",
                "-M", "pc",
                "-m", "128M",
                "-bios", str(self.image_path),
                "-nographic",
                "-no-reboot",
                "-d", "in_asm,int,unimp",
                "-D", str(log_path),
            ]

        if self.enable_gdb:
            cmd.extend(["-gdb", f"tcp::{self.gdb_port}", "-S"])

        return cmd

    def run(self) -> Dict[str, Any]:
        log_path = self.work_dir / f"run_{self.mode}_{int(time.time())}.log"
        cmd = self.build_qemu_cmd(log_path)

        start_time = time.time()
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
        )

        try:
            stdout_data, stderr_data = proc.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            # Terminate gracefully with SIGINT/SIGTERM so log buffers flush
            proc.terminate()
            try:
                stdout_data, stderr_data = proc.communicate(timeout=1.0)
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout_data, stderr_data = proc.communicate()

        elapsed = time.time() - start_time
        exit_code = proc.returncode

        # Analyze log output
        analysis = self._analyze_log(log_path, stdout_data.decode("latin1", errors="replace"))

        return {
            "image": str(self.image_path),
            "size": self.info["size"],
            "mode": self.mode,
            "architecture_info": self.info,
            "qemu_cmd": " ".join(cmd),
            "duration_sec": round(elapsed, 3),
            "exit_code": exit_code,
            "log_path": str(log_path),
            "log_size": os.path.getsize(log_path) if log_path.exists() else 0,
            "stdout": stdout_data.decode("latin1", errors="replace").strip(),
            "stderr": stderr_data.decode("latin1", errors="replace").strip(),
            "analysis": analysis,
        }

    def _analyze_log(self, log_path: Path, stdout_str: str = "") -> Dict[str, Any]:
        if self.mode == "peim":
            # Parse Unicorn PEIM harness output
            lines = [l.strip() for l in stdout_str.splitlines() if l.strip()]
            pei_services = [l for l in lines if "[PEI]" in l or "slot " in l]
            ppi_installed = [l for l in lines if "InstallPpi" in l or "NotifyPpi" in l or "slot 8" in l or "slot 9" in l or "slot 6" in l]
            success = any("returned: 0x0" in l or "EFI_SUCCESS" in l or "ENTRY RETURNED" in l for l in lines)
            entry_info = next((l for l in lines if "Loaded PE32" in l or "ImageBase=" in l), "UNKNOWN")
            insns_line = next((l for l in lines if "instructions executed:" in l), "instructions executed: 0")
            insns = int(insns_line.split(":")[-1].strip()) if ":" in insns_line else 0
            calls_line = next((l for l in lines if "PEI service calls:" in l), "PEI service calls: 0")
            calls = int(calls_line.split(":")[-1].strip()) if ":" in calls_line else len(pei_services)

            return {
                "status": "PEIM_SUCCESS" if success else "PEIM_EXECUTED",
                "entry_info": entry_info,
                "instructions_executed": insns,
                "pei_services_invoked": calls,
                "ppis_installed": len(ppi_installed),
                "summary_lines": [l for l in lines if "slot" in l or "SMBUS" in l or "ENTRY" in l][:8],
            }

        if not log_path.exists():
            return {"status": "NO_LOG"}

        size = os.path.getsize(log_path)
        blocks_captured = []
        instructions_executed = 0
        milestones = []

        if self.mode == "legacy":
            # Parse in_asm trace
            with open(log_path, "r", encoding="latin1", errors="replace") as f:
                current_block = []
                for line in f:
                    line_s = line.strip()
                    if line_s == "IN:":
                        if current_block and len(blocks_captured) < 15:
                            blocks_captured.append("\n".join(current_block))
                        current_block = []
                    elif line_s.startswith("0x"):
                        current_block.append(line_s)
                        instructions_executed += 1
                        if "ljmpw" in line_s or "ljmpl" in line_s:
                            if "Far Jump" not in milestones:
                                milestones.append(f"Far Jump: {line_s}")
                        if "cli" in line_s and "CLI" not in milestones:
                            milestones.append("CLI Executed")

                if current_block and len(blocks_captured) < 15:
                    blocks_captured.append("\n".join(current_block))

            status = "EXECUTION_ACTIVE" if instructions_executed > 10 else "STALLED"

            return {
                "status": status,
                "instructions_executed": instructions_executed,
                "first_blocks": blocks_captured[:5],
                "milestones": milestones,
            }
        else:
            # Parse UEFI debugcon log
            with open(log_path, "r", encoding="latin1", errors="replace") as f:
                lines = [line.strip() for line in f if line.strip()]

            status = "UEFI_BOOT_ACTIVE" if len(lines) > 0 else "NO_DEBUGCON_OUTPUT"
            return {
                "status": status,
                "total_lines": len(lines),
                "head": lines[:10],
                "tail": lines[-10:] if len(lines) > 10 else lines,
            }


def main():
    parser = argparse.ArgumentParser(description="Universal QEMU BIOS Runner (qemu-mod)")
    parser.add_argument("image", help="Path to BIOS/Firmware ROM or PEIM image")
    parser.add_argument("--mode", choices=["auto", "uefi", "legacy", "peim"], default="auto", help="Execution mode (default: auto)")
    parser.add_argument("--timeout", type=float, default=2.0, help="Execution timeout in seconds (default: 2.0)")
    parser.add_argument("--gdb", action="store_true", help="Start GDB stub server (QEMU pauses on start for GDB attach)")
    parser.add_argument("--gdb-port", type=int, default=1234, help="GDB server port (default: 1234)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Error: Image '{args.image}' does not exist.", file=sys.stderr)
        sys.exit(1)

    runner = QemuBiosRunner(
        image_path=image_path,
        mode=args.mode,
        timeout=args.timeout,
        enable_gdb=args.gdb,
        gdb_port=args.gdb_port,
    )
    result = runner.run()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 60)
        print(" QEMU BIOS Execution Report (qemu-mod)")
        print("=" * 60)
        print(f" Image:        {result['image']}")
        print(f" Size:         {result['size']} bytes ({result['size'] // 1024} KB)")
        print(f" Detected:     {result['mode'].upper()} (Reset: {result['architecture_info']['reset_target']})")
        print(f" Execution:    {result['duration_sec']}s (Exit code: {result['exit_code']})")
        print(f" Log Size:     {result['log_size']} bytes")
        print(f" Status:       {result['analysis']['status']}")

        if result['mode'] == 'legacy':
            print(f" Instructions: {result['analysis'].get('instructions_executed', 0)}")
            print(f" Milestones:   {', '.join(result['analysis'].get('milestones', []))}")
            if result['analysis'].get('first_blocks'):
                print("\n Initial Execution Trace:")
                for i, blk in enumerate(result['analysis']['first_blocks'][:2]):
                    print(f"--- Block {i + 1} ---")
                    print(blk)
        elif result['mode'] == 'peim':
            print(f" Entry Info:   {result['analysis'].get('entry_info')}")
            print(f" PEI Services: {result['analysis'].get('pei_services_invoked', 0)}")
            print(f" PPIs:         {result['analysis'].get('ppis_installed', 0)}")
            print("\n Execution Summary:")
            for l in result['analysis'].get('summary_lines', [])[:6]:
                print(f"   {l}")
        else:
            print(f" Debugcon Lines: {result['analysis'].get('total_lines', 0)}")
            for l in result['analysis'].get('head', [])[:5]:
                print(f"   {l}")
        print("=" * 60)


if __name__ == "__main__":
    main()
