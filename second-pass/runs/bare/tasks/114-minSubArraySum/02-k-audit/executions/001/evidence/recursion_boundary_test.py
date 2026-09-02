#!/usr/bin/env python3
"""Expose the candidate/canonical divergence at CPython's recursion boundary."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


def outcome(function, nums: list[int]):
    try:
        return ("return", function(nums.copy()))
    except Exception as exc:
        return ("exception", type(exc).__name__)


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "boundary_canonical")
    candidate = load(
        Path("/tmp/audit-work/114-minSubArraySum-audit/solution.py"),
        "boundary_candidate",
    )
    nums = [1] * 1100
    trusted = outcome(canonical, nums)
    generated = outcome(candidate, nums)
    print(f"python={sys.version.split()[0]} recursion_limit={sys.getrecursionlimit()}")
    print(f"input=([1] * {len(nums)}) canonical={trusted} candidate={generated}")
    if trusted != ("return", 1):
        raise AssertionError(f"unexpected canonical boundary outcome: {trusted}")
    if generated != ("exception", "RecursionError"):
        raise AssertionError(f"expected candidate RecursionError, got: {generated}")
    print("INTENDED-DOMAIN DIVERGENCE CONFIRMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
