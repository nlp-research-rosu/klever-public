#!/usr/bin/env python3
"""Independent candidate/canonical differential audit for HumanEval 49-modp."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/fresh/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/02_inputs.json")


def load_entry(path: Path, module_name: str) -> Callable[[int, int], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.modp


def observe(fn: Callable[[int, int], Any], n: int, p: int) -> dict[str, Any]:
    try:
        value = fn(n, p)
        return {"kind": "return", "type": type(value).__name__, "value": value}
    except Exception as err:  # Evidence records exception behavior too.
        return {
            "kind": "exception",
            "type": type(err).__name__,
            "message": str(err),
        }


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_modp")
generated = load_entry(GENERATED_PATH, "candidate_generated_modp")

examples = [(3, 5), (1101, 101), (0, 101), (3, 11), (100, 101)]
boundaries = [
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 2),
    (2, 3),
    (3, 2),
    (4, 3),
    (63, 97),
    (64, 97),
    (65, 97),
    (10_000, 1),
    (10_000, 65_537),
]
exhaustive_small = [(n, p) for n in range(0, 33) for p in range(1, 34)]

rng = random.Random(49_2026_07_23)
seeded_generated = [
    (rng.randrange(0, 20_001), rng.randrange(1, 20_002)) for _ in range(750)
]

intended_inputs = sorted(
    set(examples + boundaries + exhaustive_small + seeded_generated)
)
outside_formal_domain = [
    (-5, 1),
    (-2, 5),
    (-1, 2),
    (-1, 5),
    (0, 0),
    (1, 0),
    (2, 0),
    (0, -1),
    (1, -1),
    (2, -5),
]

INPUTS_PATH.write_text(
    json.dumps(
        {
            "examples": examples,
            "boundaries": boundaries,
            "exhaustive_small": exhaustive_small,
            "seed": 49_2026_07_23,
            "seeded_generated": seeded_generated,
            "intended_unique": intended_inputs,
            "outside_formal_domain": outside_formal_domain,
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

intended_mismatches = []
for n, p in intended_inputs:
    left = observe(canonical, n, p)
    right = observe(generated, n, p)
    if left != right:
        intended_mismatches.append(
            {"input": [n, p], "canonical": left, "generated": right}
        )

outside_results = []
for n, p in outside_formal_domain:
    left = observe(canonical, n, p)
    right = observe(generated, n, p)
    outside_results.append(
        {
            "input": [n, p],
            "canonical": left,
            "generated": right,
            "same": left == right,
        }
    )

input_digest = hashlib.sha256(
    json.dumps(intended_inputs, separators=(",", ":")).encode()
).hexdigest()

print(f"canonical={CANONICAL_PATH}")
print(f"generated={GENERATED_PATH}")
print("formal_domain=n >= 0 and p > 0")
print(f"documented_examples={len(examples)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_small_cases={len(exhaustive_small)}")
print(f"seeded_generated_cases={len(seeded_generated)}")
print(f"intended_unique_cases={len(intended_inputs)}")
print(f"intended_input_sha256={input_digest}")
print(f"intended_mismatch_count={len(intended_mismatches)}")
if intended_mismatches:
    print("INTENDED_MISMATCHES")
    print(json.dumps(intended_mismatches, indent=2, sort_keys=True))
print("OUTSIDE_FORMAL_DOMAIN")
print(json.dumps(outside_results, indent=2, sort_keys=True))

raise SystemExit(1 if intended_mismatches else 0)
