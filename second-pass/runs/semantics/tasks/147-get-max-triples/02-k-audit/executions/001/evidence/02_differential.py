#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


def main() -> int:
    canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_entry(
        "submitted_generated", Path("/tmp/audit-work/reconstruction/solution.py")
    )

    rng = random.Random(147)
    documented = [5]
    empty_extension = [0]  # Outside the positive-input contract, recorded separately.
    branch_boundaries = list(range(1, 13))
    representative_generated = sorted(rng.sample(range(13, 221), 36))
    inputs = sorted(
        set(documented + empty_extension + branch_boundaries + representative_generated)
    )

    print("ORACLE /reference/canonical.py:get_max_triples")
    print("GENERATED /tmp/audit-work/reconstruction/solution.py:get_max_triples")
    print("INTENDED_DOMAIN positive integers")
    print("EMPTY_EXTENSION_CASE 0")
    print("DOCUMENTED_EXAMPLES " + json.dumps(documented))
    print("BRANCH_BOUNDARIES " + json.dumps(branch_boundaries))
    print(
        "REPRESENTATIVE_GENERATED seed=147 population=[13,220] sample_size=36 values="
        + json.dumps(representative_generated)
    )
    print("ALL_INPUTS " + json.dumps(inputs))

    mismatches: list[dict[str, int]] = []
    results: list[dict[str, int]] = []
    for n in inputs:
        expected = canonical(n)
        actual = generated(n)
        row = {"n": n, "canonical": expected, "generated": actual}
        results.append(row)
        if expected != actual:
            mismatches.append(row)

    print("RESULTS " + json.dumps(results, separators=(",", ":")))
    print(f"CASE_COUNT {len(inputs)}")
    print(f"MISMATCH_COUNT {len(mismatches)}")
    if mismatches:
        print("MISMATCHES " + json.dumps(mismatches, separators=(",", ":")))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
