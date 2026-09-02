#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("candidate_solution", Path("/candidate/solution.py"))


def independent_rotation_oracle(values: list[int]) -> bool:
    if not values:
        return True
    target = sorted(values)
    return any(
        values[-shift:] + values[:-shift] == target
        for shift in range(len(values))
    )


documented_and_boundaries = [
    [],
    [1],
    [0],
    [-1],
    [1, 2],
    [2, 1],
    [-2, -1, 0],
    [0, -2, -1],
    [-1, 0, -2],
    [1, 2, 3],
    [3, 4, 5, 1, 2],
    [3, 5, 4, 1, 2],
    [1, 3, 2],
    [2, 3, 1],
    [4, 1, 3, 2],
    [-(10**40), 0, 10**40],
    [10**40, -(10**40), 0],
    [0, 10**40, -(10**40)],
]

unique_permutations = [
    list(values)
    for length in range(0, 9)
    for values in itertools.permutations(range(length))
]

rng = random.Random(109)
random_unique = []
for _ in range(2000):
    length = rng.randrange(0, 65)
    values = rng.sample(range(-10_000, 10_001), length)
    random_unique.append(values)

# These are outside the documented unique-element contract.  They check that
# duplicate handling does not conceal a boundary mismatch in the rewrite.
duplicate_robustness = [
    list(values)
    for length in range(0, 8)
    for values in itertools.product((-1, 0, 1), repeat=length)
]

scopes = [
    ("documented_and_boundaries", documented_and_boundaries, True),
    ("all_unique_permutations_lengths_0_through_8", unique_permutations, True),
    ("seed_109_random_unique_lengths_0_through_64", random_unique, True),
    ("out_of_contract_duplicate_robustness", duplicate_robustness, False),
]

corpus = []
mismatches = []
intended_mismatches = []
for scope_name, cases, intended_domain in scopes:
    scope_mismatches = 0
    for values in cases:
        expected = independent_rotation_oracle(values)
        canonical_result = canonical(list(values))
        generated_result = generated(list(values))
        corpus.append([scope_name, values])
        if not (
            type(canonical_result) is bool
            and type(generated_result) is bool
            and canonical_result == expected
            and generated_result == expected
        ):
            scope_mismatches += 1
            mismatches.append(
                {
                    "scope": scope_name,
                    "input": values,
                    "oracle": expected,
                    "canonical": canonical_result,
                    "generated": generated_result,
                }
            )
            if intended_domain:
                intended_mismatches.append(mismatches[-1])
    print(
        f"scope={scope_name} intended_domain={intended_domain} "
        f"cases={len(cases)} mismatches={scope_mismatches}"
    )

encoded = json.dumps(corpus, separators=(",", ":"), ensure_ascii=True).encode()
print(f"complete_corpus_cases={len(corpus)}")
print(f"complete_corpus_json_sha256={hashlib.sha256(encoded).hexdigest()}")
print(f"total_mismatches={len(mismatches)}")
print(f"intended_domain_mismatches={len(intended_mismatches)}")
print(f"out_of_contract_observations={len(mismatches) - len(intended_mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], indent=2))
if intended_mismatches:
    raise SystemExit(1)
