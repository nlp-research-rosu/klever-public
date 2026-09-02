#!/usr/bin/env python3
"""Independent canonical/candidate/property differential for HumanEval 106."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def property_oracle(n: int) -> list[int]:
    return [
        math.factorial(i) if i % 2 == 0 else i * (i + 1) // 2
        for i in range(1, n + 1)
    ]


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_106")
    generated = load_entry(
        Path("/tmp/audit-work/reconstruction/solution.py"),
        "candidate_solution_106",
    )

    seed = 106
    generator = random.Random(seed)
    documented_and_boundaries = [-3, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    exhaustive_small = list(range(0, 65))
    generated_inputs = [generator.randint(0, 120) for _ in range(64)]
    scale_inputs = [100, 120, 200]
    inputs = sorted(
        set(
            documented_and_boundaries
            + exhaustive_small
            + generated_inputs
            + scale_inputs
        )
    )

    print(f"seed={seed}")
    print(f"inputs={inputs}")
    mismatches: list[dict[str, object]] = []
    records: list[dict[str, object]] = []
    for n in inputs:
        trusted = canonical(n)
        candidate = generated(n)
        expected = property_oracle(n)
        record = {
            "n": n,
            "canonical": trusted,
            "candidate": candidate,
            "property": expected,
        }
        records.append(record)
        if trusted != candidate or candidate != expected:
            mismatches.append(record)
            print(f"MISMATCH n={n} record={record!r}")

    for n in documented_and_boundaries:
        record = next(item for item in records if item["n"] == n)
        print(
            f"boundary n={n} canonical={record['canonical']} "
            f"candidate={record['candidate']} property={record['property']}"
        )

    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    print(f"records_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"case_count={len(records)}")
    print(f"mismatch_count={len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
