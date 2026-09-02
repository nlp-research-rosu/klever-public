#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval/49."""

from __future__ import annotations

import importlib.util
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/fresh")


def load_function(path: Path, module_name: str) -> Callable[[int, int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.modp


canonical = load_function(ROOT / "trusted" / "canonical.py", "trusted_canonical")
generated = load_function(ROOT / "solution.py", "generated_solution")


def outcome(function: Callable[[int, int], int], n: int, p: int) -> tuple[str, object]:
    try:
        return ("value", function(n, p))
    except Exception as error:  # Deliberately compare observable exception types.
        return ("exception", type(error).__name__)


documented = [(3, 5), (1101, 101), (0, 101), (3, 11), (100, 101)]
branch_boundaries = [
    (-2, 5),
    (-1, 5),
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 2),
    (2, 2),
    (1, 0),
    (0, 0),
    (1, -1),
    (0, -1),
    (2, -5),
]
formal_domain_grid = [(n, p) for n in range(0, 13) for p in range(1, 13)]
typed_domain_grid = [(n, p) for n in range(-5, 21) for p in range(-5, 13)]
rng = random.Random(49)
generated_cases = [(rng.randint(-20, 250), rng.randint(-20, 80)) for _ in range(400)]

categories = [
    ("documented_examples", documented),
    ("branch_and_empty_iteration_boundaries", branch_boundaries),
    ("formal_claim_domain_grid", formal_domain_grid),
    ("annotated_integer_domain_grid", typed_domain_grid),
    ("deterministic_generated_integer_inputs_seed_49", generated_cases),
]

all_mismatches: list[tuple[str, int, int, tuple[str, object], tuple[str, object]]] = []
print("oracle=/tmp/audit-work/fresh/trusted/canonical.py::modp")
print("candidate=/tmp/audit-work/fresh/solution.py::modp")
for category, cases in categories:
    mismatches = []
    kinds: Counter[str] = Counter()
    seen: set[tuple[int, int]] = set()
    for n, p in cases:
        if (n, p) in seen:
            continue
        seen.add((n, p))
        expected = outcome(canonical, n, p)
        actual = outcome(generated, n, p)
        kinds[f"canonical_{expected[0]}"] += 1
        kinds[f"generated_{actual[0]}"] += 1
        if expected != actual:
            mismatch = (category, n, p, expected, actual)
            mismatches.append(mismatch)
            all_mismatches.append(mismatch)
    print(
        f"category={category} cases={len(seen)} "
        f"mismatches={len(mismatches)} outcomes={dict(sorted(kinds.items()))}"
    )
    for _, n, p, expected, actual in mismatches[:20]:
        print(f"  mismatch n={n} p={p} canonical={expected} generated={actual}")
    if len(mismatches) > 20:
        print(f"  ... {len(mismatches) - 20} additional mismatches omitted")

print(f"total_category_mismatches_including_cross_category_duplicates={len(all_mismatches)}")
formal_mismatches = [
    mismatch
    for mismatch in all_mismatches
    if mismatch[0] == "formal_claim_domain_grid"
]
print(f"formal_claim_domain_mismatches={len(formal_mismatches)}")
print("DIFFERENTIAL_MATCH" if not all_mismatches else "DIFFERENTIAL_MISMATCH")
sys.exit(0 if not all_mismatches else 1)
