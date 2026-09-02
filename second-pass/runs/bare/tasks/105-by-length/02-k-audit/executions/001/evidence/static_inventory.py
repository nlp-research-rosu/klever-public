#!/usr/bin/env python3
"""Emit a bounded source inventory for the local K definition and proof files."""

from __future__ import annotations

import collections
import re
from pathlib import Path


root = Path("/tmp/audit-work/source")
k_paths = [root / "semantic.k", root / "verification.k", root / "spec.k"]

for path in k_paths:
    print(f"===== {path.name} =====")
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if (
            stripped.startswith(
                (
                    "requires ",
                    "module ",
                    "endmodule",
                    "imports ",
                    "configuration",
                    "syntax ",
                    "rule ",
                    "claim",
                    "<",
                )
            )
            or " [function" in line
            or " [total" in line
            or " [functional" in line
            or " [simplification" in line
            or " [priority" in line
            or " [owise" in line
            or "requires " in line
            or "ensures " in line
        ):
            print(f"{line_number:4}: {line}")

solution_source = (root / "solution.mpy").read_text(encoding="utf-8")
constructors = re.findall(r"\b([A-Za-z][A-Za-z0-9]*)\s*\(", solution_source)
print("===== solution.mpy constructor use counts =====")
for constructor, count in sorted(collections.Counter(constructors).items()):
    print(f"{constructor}={count}")

all_k_source = "\n".join(path.read_text(encoding="utf-8") for path in k_paths)
print("===== special declaration counts =====")
for label, pattern in (
    ("function_attributes", r"\[function(?:[,\]])"),
    ("total_attributes", r"\[[^\]]*\btotal\b[^\]]*\]"),
    ("functional_attributes", r"\[[^\]]*\bfunctional\b[^\]]*\]"),
    ("simplification_attributes", r"\[[^\]]*\bsimplification\b[^\]]*\]"),
    ("priority_attributes", r"\[[^\]]*\bpriority\b[^\]]*\]"),
    ("owise_attributes", r"\[[^\]]*\bowise\b[^\]]*\]"),
    ("opaque_attributes", r"\[[^\]]*\bopaque\b[^\]]*\]"),
    ("claims", r"(?m)^\s*claim(?:\s|$)"),
    ("rules", r"(?m)^\s*rule(?:\s|$)"),
):
    print(f"{label}={len(re.findall(pattern, all_k_source))}")
