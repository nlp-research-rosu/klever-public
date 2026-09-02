#!/usr/bin/env python3
"""Independent differential test of candidate solution.py against canonical.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    canonical = load("/reference/canonical.py", "trusted_canonical")
    candidate = load("/tmp/audit-work/task/solution.py", "generated_solution")

    documented = [15, 32]
    branch_boundaries = [
        0, 1, 2, 3, 7, 8, 15, 16, 31, 32, 33, 63, 64, 65,
        102, 103, 127, 128, 129, 255, 256, 257, 1023, 1024, 1025,
    ]
    exhaustive_small = list(range(0, 513))
    rng = random.Random(790079)
    representative = [rng.randrange(0, 10**18) for _ in range(200)]
    large = [2**256 - 1, 2**256, 2**256 + 1, 2**1024 - 1, 2**1024, 2**1024 + 1]
    outside_formal_probe = [-1, -2, -15, -32, -103, -(2**256)]
    cases = documented + branch_boundaries + exhaustive_small + representative + large + outside_formal_probe

    inputs_record = {
        "documented": documented,
        "branch_boundaries": branch_boundaries,
        "exhaustive_small": {"start": 0, "stop_inclusive": 512},
        "representative_seed": 790079,
        "representative_values": representative,
        "large": large,
        "outside_formal_probe": outside_formal_probe,
    }
    record_path = Path("/audit-output/evidence/differential-inputs.json")
    record_path.write_text(json.dumps(inputs_record, indent=2, sort_keys=True) + "\n")

    mismatches = []
    format_failures = []
    for value in cases:
        expected = canonical.decimal_to_binary(value)
        actual = candidate.decimal_to_binary(value)
        if actual != expected:
            mismatches.append({"input": value, "canonical": expected, "candidate": actual})
        if value >= 0:
            payload = actual[2:-2] if actual.startswith("db") and actual.endswith("db") else ""
            if not payload or any(ch not in "01" for ch in payload):
                format_failures.append({"input": value, "result": actual})

    print("oracle=/reference/canonical.py:decimal_to_binary")
    print("candidate=/tmp/audit-work/task/solution.py:decimal_to_binary")
    print(f"documented_count={len(documented)}")
    print(f"branch_boundary_count={len(branch_boundaries)}")
    print("exhaustive_small=0..512")
    print(f"representative_seed=790079 representative_count={len(representative)}")
    print(f"large_count={len(large)} outside_formal_probe_count={len(outside_formal_probe)}")
    print(f"total_cases={len(cases)}")
    print(f"input_record_sha256={hashlib.sha256(record_path.read_bytes()).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"nonnegative_format_failure_count={len(format_failures)}")
    print("sample_results:")
    for value in [0, 1, 15, 32, 103, -1]:
        print(f"  {value}: {candidate.decimal_to_binary(value)!r}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2))
    if format_failures:
        print(json.dumps(format_failures[:20], indent=2))
    assert not mismatches
    assert not format_failures
    print("DIFFERENTIAL_OK")


if __name__ == "__main__":
    main()
