#!/usr/bin/env python3
"""Independent candidate/canonical/contract differential for HumanEval 95."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/tmp/audit-work/95-check-dict-case/solution.py"), "generated_candidate")


def contract_oracle(value: dict) -> bool:
    """Direct formalization of prompt.py's all-keys/nonempty contract."""
    keys = tuple(value.keys())
    return bool(keys) and (
        all(isinstance(key, str) and key.islower() for key in keys)
        or all(isinstance(key, str) and key.isupper() for key in keys)
    )


documented = [
    ({"a": "apple", "b": "banana"}, True),
    ({"a": "apple", "A": "banana", "B": "banana"}, False),
    ({"a": "apple", 8: "banana"}, False),
    ({"Name": "John", "Age": "36", "City": "Houston"}, False),
    ({"STATE": "NC", "ZIP": "12345"}, True),
]

branch_boundaries = [
    {},
    {"a": 0},
    {"A": 0},
    {"": 0},
    {"123": 0},
    {"a1": 0},
    {"A1": 0},
    {"a": 0, "b": 1},
    {"A": 0, "B": 1},
    {"a": 0, "B": 1},
    {"A": 0, "b": 1},
    {"a": 0, 8: 1},
    {8: 0, "a": 1},
    {"A": 0, "B": 1, "c": 2},
    {"a": 0, "b": 1, "C": 2},
    {"A": 0, "B": 1, 8: 2},
    {"a": 0, "b": 1, "123": 2},
    {("A",): 0},
    {"é": 0},
    {"É": 0},
    {"ǅ": 0},
]

key_pool = (
    "",
    "a",
    "b2",
    "A",
    "B2",
    "123",
    "a-B",
    "Aa",
    "é",
    "É",
    0,
    8,
    None,
    ("tuple",),
)

cases: list[tuple[str, dict, bool | None]] = []
for value, expected in documented:
    cases.append(("documented", value, expected))
for value in branch_boundaries:
    cases.append(("boundary", value, None))
for size in range(5):
    for keys in product(key_pool, repeat=size):
        value = {key: index for index, key in enumerate(keys)}
        cases.append((f"product-size-{size}", value, None))

rng = random.Random(950730)
for index in range(500):
    size = rng.randrange(0, 9)
    keys = [rng.choice(key_pool) for _ in range(size)]
    value = {key: (index, position) for position, key in enumerate(keys)}
    cases.append(("seeded-random", value, None))

counts = {
    "cases": 0,
    "documented_expected_mismatch_candidate": 0,
    "documented_expected_mismatch_canonical": 0,
    "candidate_vs_canonical": 0,
    "candidate_vs_contract": 0,
    "canonical_vs_contract": 0,
}
first_mismatches: list[str] = []

for source, value, expected in cases:
    got_candidate = candidate(value)
    got_canonical = canonical(value)
    got_contract = contract_oracle(value)
    counts["cases"] += 1
    mismatch_labels: list[str] = []
    if expected is not None and got_candidate != expected:
        counts["documented_expected_mismatch_candidate"] += 1
        mismatch_labels.append("candidate!=documented")
    if expected is not None and got_canonical != expected:
        counts["documented_expected_mismatch_canonical"] += 1
        mismatch_labels.append("canonical!=documented")
    if got_candidate != got_canonical:
        counts["candidate_vs_canonical"] += 1
        mismatch_labels.append("candidate!=canonical")
    if got_candidate != got_contract:
        counts["candidate_vs_contract"] += 1
        mismatch_labels.append("candidate!=contract")
    if got_canonical != got_contract:
        counts["canonical_vs_contract"] += 1
        mismatch_labels.append("canonical!=contract")
    if mismatch_labels and len(first_mismatches) < 30:
        first_mismatches.append(
            f"{source} {value!r}: candidate={got_candidate!r} "
            f"canonical={got_canonical!r} contract={got_contract!r} "
            f"expected={expected!r} [{', '.join(mismatch_labels)}]"
        )

print("INDEPENDENT DIFFERENTIAL TEST")
print("oracle: direct prompt contract; implementation does not import candidate helpers")
print("generated corpus: all key sequences of lengths 0..4 over a 14-key pool,")
print("plus documented, explicit branch-boundary, and 500 seeded-random cases")
for key, value in counts.items():
    print(f"{key} = {value}")
print("FIRST_MISMATCHES")
for mismatch in first_mismatches:
    print(mismatch)

assert counts["documented_expected_mismatch_candidate"] == 0
assert counts["candidate_vs_contract"] == 0

# A candidate/canonical divergence is deliberately reported, not hidden.
raise SystemExit(1 if counts["candidate_vs_canonical"] else 0)
