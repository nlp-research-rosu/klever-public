#!/usr/bin/env python3
"""Independent canonical/candidate differential test for HumanEval 49."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/49-modp")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, n: int, p: int):
    try:
        return ("value", function(n, p))
    except Exception as error:  # diagnostic comparison includes exception types
        return ("exception", type(error).__name__)


def main() -> int:
    canonical = load_module("trusted_canonical_49", WORK / "canonical.py")
    candidate = load_module("generated_candidate_49", WORK / "solution.py")

    documented = [(3, 5), (1101, 101), (0, 101), (3, 11), (100, 101)]
    boundaries = [
        (0, 1), (0, 2), (0, 3),
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (63, 97), (64, 97), (65, 97),
        (4096, 65537),
    ]

    rng = random.Random(490049)
    generated = [(rng.randrange(0, 5001), rng.randrange(1, 10001))
                 for _ in range(500)]
    # Include a complete small grid so both sides of the canonical loop boundary
    # and the smallest positive modulus are necessarily exercised.
    generated += [(n, p) for n in range(0, 33) for p in range(1, 65)]

    intended_cases = list(dict.fromkeys(documented + boundaries + generated))
    mismatches = []
    prompt_mismatches = []
    for n, p in intended_cases:
        got_canonical = outcome(canonical.modp, n, p)
        got_candidate = outcome(candidate.modp, n, p)
        prompt_value = pow(2, n, p)
        if got_canonical != got_candidate:
            mismatches.append((n, p, got_canonical, got_candidate, prompt_value))
        if got_candidate != ("value", prompt_value):
            prompt_mismatches.append((n, p, got_candidate, prompt_value))

    print("INTENDED_DOMAIN n >= 0 and p > 0")
    print(f"DOCUMENTED_CASES {len(documented)}")
    print(f"BOUNDARY_CASES {len(boundaries)}")
    print(f"GENERATED_CASES {len(generated)} seed=490049")
    print(f"TOTAL_INTENDED_CASES {len(intended_cases)}")
    print(f"CANONICAL_CANDIDATE_MISMATCHES {len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    print(f"CANDIDATE_PROMPT_POW_MISMATCHES {len(prompt_mismatches)}")
    for mismatch in prompt_mismatches[:20]:
        print("PROMPT_MISMATCH", repr(mismatch))

    # Diagnostics outside the claimed/intended domain are recorded separately.
    outside = [
        (-3, 5), (-1, 1), (-1, 2), (-1, 3),
        (0, -5), (1, -5), (3, -5),
        (0, 0), (1, 0),
    ]
    print(f"OUTSIDE_DOMAIN_CASES {len(outside)}")
    for n, p in outside:
        print("OUTSIDE", n, p,
              "canonical=", repr(outcome(canonical.modp, n, p)),
              "candidate=", repr(outcome(candidate.modp, n, p)))

    # A mismatch against either trusted canonical behavior or prompt arithmetic
    # makes the differential command nonzero so the audit must judge it.
    return 1 if mismatches or prompt_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
