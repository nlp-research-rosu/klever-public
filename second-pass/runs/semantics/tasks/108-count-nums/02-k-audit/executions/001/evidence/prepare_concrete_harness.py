#!/usr/bin/env python3
"""Combine the byte-checked submission with reviewer-authored assertions."""

from pathlib import Path

solution = Path("/tmp/audit-work/audit-108/source/solution.py")
suffix = Path("/audit-output/evidence/concrete_harness_suffix.py")
output = Path("/tmp/audit-work/audit-108/source/concrete_reconstruction.py")

output.write_bytes(solution.read_bytes() + suffix.read_bytes())
print(f"solution={solution}")
print(f"suffix={suffix}")
print(f"output={output}")
