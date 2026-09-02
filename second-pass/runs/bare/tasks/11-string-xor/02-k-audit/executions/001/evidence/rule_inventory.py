#!/usr/bin/env python3
"""Emit exhaustive numbered K sources plus mechanically detected item counts."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("/tmp/audit-work/11-string-xor-audit/source")
for filename in ("semantic.k", "verification.k", "spec.k"):
    path = SOURCE / filename
    lines = path.read_text(encoding="utf-8").splitlines()
    print(f"FILE {filename}")
    print(
        "COUNTS "
        f"syntax={sum(line.strip().startswith('syntax ') for line in lines)} "
        f"rules={sum(line.strip().startswith('rule ') for line in lines)} "
        f"claims={sum(line.strip().startswith('claim') for line in lines)} "
        f"priority40={sum('[priority(40)]' in line for line in lines)} "
        f"function={sum('[function' in line for line in lines)} "
        f"total={sum('total' in line for line in lines)} "
        f"functional={sum('functional' in line for line in lines)} "
        f"opaque={sum('opaque' in line for line in lines)} "
        f"simplification={sum('simplification' in line for line in lines)} "
        f"macro={sum('[macro]' in line for line in lines)}"
    )
    for line_number, line in enumerate(lines, 1):
        print(f"{line_number:4d}: {line}")
    print()
