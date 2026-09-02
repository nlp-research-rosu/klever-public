#!/usr/bin/env python3
"""Wrap the freshly translated Module term in concrete Run/Call test programs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path("/tmp/audit-work/146-specialFilter")
MODULE = (ROOT / "candidate/regenerated-solution.mpy").read_text(encoding="utf-8").strip()
OUT = ROOT / "concrete-inputs"

CASES = {
    "prompt1": [15, -73, 14, -15],
    "prompt2": [33, -2, -3, 45, 21, 109],
    "empty": [],
    "threshold": [9, 10, 11, 12],
    "digit_widths": [99, 100, 101, 109, 111, 999, 1000, 1001, 90009],
    "negative": [-999999, -73, -11, -1],
    "wide": [10**20 + 1, 3 * 10**40 + 5, 8 * 10**50 + 7],
}


def load_candidate():
    path = ROOT / "candidate/solution.py"
    spec = importlib.util.spec_from_file_location("candidate_for_krun_oracle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.specialFilter


def list_expr(nums: list[int]) -> str:
    if not nums:
        return "ListExpr()"
    return "ListExpr(" + ", ".join(f"Int({number})" for number in nums) + ")"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    candidate = load_candidate()
    manifest = []
    for name, nums in CASES.items():
        expected = candidate(list(nums))
        program = f'Run({MODULE}, Call(Name("specialFilter"), {list_expr(nums)}))\n'
        path = OUT / f"{name}.mpy"
        path.write_text(program, encoding="utf-8")
        manifest.append({"name": name, "nums": nums, "expected": expected, "path": str(path)})
    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(manifest_path.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
