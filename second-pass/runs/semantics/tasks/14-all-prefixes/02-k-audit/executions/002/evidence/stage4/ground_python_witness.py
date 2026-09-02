#!/usr/bin/env python3
"""Print concrete claim substitutions against both Python implementations."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/run-002")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load("canonical_ground", WORK / "canonical.py").all_prefixes
    candidate = load("candidate_ground", WORK / "solution.py").all_prefixes
    cases = ["", "abc"]
    expected = {"": [], "abc": ["a", "ab", "abc"]}
    for value in cases:
        canonical_result = canonical(value)
        candidate_result = candidate(value)
        print(f"input={value!r}")
        print(f"  canonical={canonical_result!r}")
        print(f"  candidate={candidate_result!r}")
        print(f"  explicit_K_postcondition={expected[value]!r}")
        if canonical_result != expected[value] or candidate_result != expected[value]:
            return 1
    print("GROUND_PYTHON_WITNESSES=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
