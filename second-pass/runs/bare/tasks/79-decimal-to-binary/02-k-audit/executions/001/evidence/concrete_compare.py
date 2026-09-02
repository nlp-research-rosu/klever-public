#!/usr/bin/env python3
"""Compare freshly kompiled generated K semantics with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path
from types import ModuleType


WORK = Path("/tmp/audit-work")
DEFINITION = WORK / "build-concrete" / "concrete-kompiled"
PROGRAM = WORK / "submitted-solution.mpy"
CASES = [
    -33,
    -32,
    -31,
    -5,
    -3,
    -2,
    -1,
    0,
    1,
    2,
    3,
    15,
    32,
    33,
    255,
    256,
    257,
    -(2**63),
    2**63,
]


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_result(output: str) -> str:
    match = re.search(
        r"<result>\s*strVal\s*\(\s*\"([01bd]+)\"\s*\)\s*~>\s*\.K\s*</result>",
        output,
        re.DOTALL,
    )
    if match is None:
        raise ValueError(f"could not find terminal strVal in:\n{output}")
    return match.group(1)


def main() -> int:
    canonical = load_module("trusted_canonical", WORK / "canonical.py")
    candidate = load_module("candidate_solution", WORK / "solution.py")
    failures = 0
    for value in CASES:
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cARG={value}",
        ]
        print("$ " + " ".join(command))
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        print(result.stdout.rstrip())
        if result.stderr:
            print("[stderr]")
            print(result.stderr.rstrip())
        print(f"[exit {result.returncode}]")
        k_value = parse_result(result.stdout) if result.returncode == 0 else None
        canonical_value = canonical.decimal_to_binary(value)
        candidate_value = candidate.decimal_to_binary(value)
        same = (
            result.returncode == 0
            and k_value == canonical_value
            and k_value == candidate_value
        )
        print(
            f"comparison input={value} K={k_value!r} "
            f"canonical={canonical_value!r} candidate={candidate_value!r} "
            f"match={same}"
        )
        if not same:
            failures += 1
    print(f"cases={len(CASES)} mismatches={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
