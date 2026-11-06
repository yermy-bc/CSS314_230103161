#!/usr/bin/env python3
"""Collect a basic hardware/software audit for Task 24."""
import os, platform, subprocess, sys
from pathlib import Path

def command_output(command):
    try:
        result=subprocess.run(command,capture_output=True,text=True,timeout=15,shell=isinstance(command,str))
        return result.stdout.strip() if result.returncode==0 else ""
    except Exception:
        return ""

def main():
    lines=["# Automatically Collected Hardware Audit","",
           f"- Operating system: {platform.platform()}",
           f"- Architecture: {platform.machine()}",
           f"- CPU model (Python): {platform.processor() or 'Not exposed by platform module'}",
           f"- Logical processors visible to Python: {os.cpu_count()}",
           f"- Python: {sys.version.split()[0]}",""]
    if sys.platform.startswith("linux"):
        lscpu=command_output(["lscpu"])
        if lscpu:
            lines += ["## lscpu output","```text",lscpu,"```",""]
        cache=command_output(["lscpu","-C"])
        if cache:
            lines += ["## Cache hierarchy","```text",cache,"```",""]
        lines += ["## Memory channel information",
                  "Linux does not consistently expose the populated memory-channel configuration. Verify it with BIOS/UEFI or a vendor utility.",""]
    elif sys.platform=="win32":
        ps='Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfCores,NumberOfLogicalProcessors | Format-List'
        cpu=command_output(["powershell","-NoProfile","-Command",ps])
        if cpu: lines += ["## Windows CPU information","```text",cpu,"```",""]
        lines += ["## Cache and memory channels",
                  "Check CPU-Z (CPU and Caches tabs; Memory tab for channel mode) or the laptop manufacturer's specifications.",""]
    elif sys.platform=="darwin":
        for key in ["machdep.cpu.brand_string","hw.physicalcpu","hw.logicalcpu"]:
            val=command_output(["sysctl","-n",key])
            if val: lines.append(f"- {key}: {val}")
        lines += ["","## Cache and memory channels","Verify with Apple system information or the manufacturer's technical documentation.",""]
    lines += ["## Manual verification required",
              "- Cache sizes/levels if not listed above.",
              "- RAM type, effective speed, capacity, and channel mode.",
              "- NUMA topology (Linux: `numactl --hardware`, if installed).",
              "- Power mode and whether the system was connected to AC power.",
              "",
              "This report is a basic software-collected inventory. Confirm all values before submission."]
    out=Path("analysis/task24_hardware_audit_auto.md")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\\n".join(lines)+"\\n",encoding="utf-8")
    print(f"Saved {out}")
if __name__=="__main__": main()
