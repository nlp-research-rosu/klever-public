#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval 105."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.by_length


def encode_case(value):
    return {
        "container": type(value).__name__,
        "items": list(value),
    }


def outcome(function, value):
    try:
        return ("return", function(value))
    except Exception as error:  # Compare observable failure as well as success.
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    canonical = load_entry(
        "trusted_humaneval_105_canonical", SCRATCH / "trusted" / "canonical.py"
    )
    candidate = load_entry("candidate_humaneval_105", SCRATCH / "solution.py")

    cases: list[list[int] | tuple[int, ...]] = [
        [2, 1, 1, 4, 5, 8, 2, 3],
        [],
        [1, -1, 55],
        list(range(1, 10)),
        list(range(9, 0, -1)),
        [0, 1],
        [1, 2],
        [8, 9],
        [9, 10],
        [-10**100, 10**100, 1, 9],
        [True, False, 1, 0, 9],
        (2, 1, 9, 10),
    ]

    # All branch boundaries and duplicates for each output block.
    boundaries = [-2, -1, 0, *range(1, 10), 10, 55]
    cases.extend([[value] for value in boundaries])
    cases.extend([[value, value] for value in boundaries])

    # Exhaustive small lists cover every adjacency and multiplicity combination
    # through length four over all valid digits and representative strange values.
    for length in range(5):
        cases.extend([list(items) for items in itertools.product(boundaries, repeat=length)])

    # A deterministic broader sample includes large magnitudes and longer lists.
    rng = random.Random(105_20260726)
    random_alphabet = boundaries + [-10**100, 10**100]
    for _ in range(500):
        cases.append(
            [rng.choice(random_alphabet) for _ in range(rng.randrange(0, 61))]
        )

    manifest = json.dumps(
        [encode_case(value) for value in cases],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    manifest_sha256 = hashlib.sha256(manifest).hexdigest()

    mismatches = []
    for index, value in enumerate(cases):
        expected = outcome(canonical, value)
        actual = outcome(candidate, value)
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": encode_case(value),
                    "canonical": expected,
                    "candidate": actual,
                }
            )
            if len(mismatches) == 20:
                break

    print(f"case_count={len(cases)}")
    print(f"input_manifest_sha256={manifest_sha256}")
    print(
        "scope=documented examples; empty; every singleton/doubleton branch "
        "boundary; exhaustive lists of lengths 0..4 over "
        f"{boundaries!r}; 500 seeded lists of lengths 0..60; tuple and big-int probes"
    )
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, default=repr))
        return 1
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
