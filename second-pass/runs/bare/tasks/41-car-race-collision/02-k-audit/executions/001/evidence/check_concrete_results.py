#!/usr/bin/env python3
"""Compare recorded K results with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


VALUES = [0, 1, 3, 10, 41]
EVIDENCE = Path("/audit-output/evidence")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.car_race_collision


def parse_result(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r"<result>\s*(-?[0-9]+)\s*</result>", text)
    if len(matches) != 1:
        raise RuntimeError(f"expected one result in {path}, found {matches}")
    if "EXIT_STATUS: 0" not in text:
        raise RuntimeError(f"krun did not exit successfully in {path}")
    return int(matches[0])


def main() -> int:
    canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_function(
        "submitted_generated", Path("/tmp/audit-work/race41/solution.py")
    )
    mismatches = []
    for value in VALUES:
        k_value = parse_result(EVIDENCE / f"krun_n_{value}.log")
        canonical_value = canonical(value)
        generated_value = generated(value)
        print(
            f"n={value} k={k_value} canonical={canonical_value} "
            f"generated={generated_value}"
        )
        if not (k_value == canonical_value == generated_value):
            mismatches.append(value)
    print(f"mismatch_count={len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
