#!/usr/bin/env python3
"""Independent differential test of candidate and trusted HumanEval entry points."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import random
import sys


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


root = Path("/tmp/audit-work")
candidate_path = root / "solution.py"
canonical_path = root / "trusted-canonical.py"
candidate = load_function(candidate_path, "candidate_solution")
canonical = load_function(canonical_path, "trusted_canonical")

documented = [(2, 8), (8, 2), (10, 14)]
empty_and_boundary = [
    (1, 1),
    (1, 2),
    (2, 2),
    (2, 3),
    (3, 3),
    (3, 4),
    (4, 4),
    (4, 5),
    (5, 6),
    (6, 6),
    (6, 7),
    (7, 8),
    (8, 8),
    (8, 9),
    (9, 9),
    (9, 10),
    (14, 10),
]
branch_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14]
branch_pairs = [(a, b) for a in branch_values for b in branch_values]
exhaustive_small = [(a, b) for a in range(1, 65) for b in range(1, 65)]

rng = random.Random(163)
generated = [
    (rng.randint(1, 1_000_000), rng.randint(1, 1_000_000))
    for _ in range(1000)
]

categories = [
    ("documented", documented),
    ("empty_and_boundary", empty_and_boundary),
    ("all_branch_pairs", branch_pairs),
    ("exhaustive_positive_1_to_64", exhaustive_small),
    ("seeded_generated_positive", generated),
]

seen: set[tuple[int, int]] = set()
mismatches: list[tuple[int, int, object, object]] = []
category_counts: dict[str, int] = {}
for category, cases in categories:
    category_counts[category] = len(cases)
    for a, b in cases:
        seen.add((a, b))
        expected = canonical(a, b)
        actual = candidate(a, b)
        if actual != expected:
            mismatches.append((a, b, expected, actual))

print("candidate_sha256", sha256(candidate_path))
print("canonical_sha256", sha256(canonical_path))
print("intended_domain", "all pairs of positive Python integers")
print("category_counts", category_counts)
print("unique_pairs", len(seen))
print("mismatch_count", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)

for a, b in documented + empty_and_boundary:
    print("CASE", a, b, "canonical=", canonical(a, b), "candidate=", candidate(a, b))

sys.exit(1 if mismatches else 0)
