#!/usr/bin/env python3
"""Independent return-value differential for HumanEval 149.

The test imports the trusted canonical implementation and the submitted Python
implementation from their audit-scratch copies.  It also checks both against a
separate direct rendering of the natural-language return contract.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
INPUT_LOG = Path("/audit-output/evidence/differential_inputs.jsonl")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


canonical = load_function(SCRATCH / "trusted" / "canonical.py", "trusted_canonical")
submitted = load_function(SCRATCH / "solution.py", "submitted_solution")


def contract_oracle(words: list[str]) -> list[str]:
    return sorted((word for word in words if len(word) % 2 == 0),
                  key=lambda word: (len(word), word))


documented = [
    (["aa", "a", "aaa"], ["aa"]),
    (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
]

boundaries = [
    [],
    [""],
    ["a"],
    ["aa"],
    ["aaa"],
    ["aaaa"],
    ["", "a", "aa", "aaa", "aaaa"],
    ["ba", "ab", "aa", "ab"],
    ["dddd", "bb", "cccc", "aa", "x"],
    ["zz", "", "a", "zz", "aa", ""],
    ["é", "éé", "😀", "😀😀", ""],
]

# Exhaust all lists through length four over a pool that crosses even/odd
# length branches, lexical ties, duplicates, and the zero-length boundary.
pool = ["", "a", "b", "aa", "ab", "ba", "aaa", "aaaa"]
exhaustive = [
    list(items)
    for width in range(5)
    for items in itertools.product(pool, repeat=width)
]

# Deterministic broader sample over varied list and word lengths.
rng = random.Random(149)
alphabet = "abcxyz"
generated = [
    [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
        for _ in range(rng.randrange(0, 13))
    ]
    for _ in range(500)
]

all_cases = [case for case, _ in documented] + boundaries + exhaustive + generated
mismatches = []
canonical_mutations = 0
submitted_mutations = 0

with INPUT_LOG.open("w", encoding="utf-8") as stream:
    for index, words in enumerate(all_cases):
        stream.write(json.dumps({"index": index, "input": words},
                                ensure_ascii=False) + "\n")
        expected = contract_oracle(words)
        canonical_arg = list(words)
        submitted_arg = list(words)
        canonical_result = canonical(canonical_arg)
        submitted_result = submitted(submitted_arg)
        canonical_mutations += canonical_arg != words
        submitted_mutations += submitted_arg != words
        if canonical_result != expected or submitted_result != expected:
            mismatches.append({
                "index": index,
                "input": words,
                "expected": expected,
                "canonical": canonical_result,
                "submitted": submitted_result,
            })

for words, expected in documented:
    assert contract_oracle(words) == expected

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_cases={len(exhaustive)}")
print(f"generated_cases={len(generated)}")
print(f"total_cases={len(all_cases)}")
print(f"return_value_mismatches={len(mismatches)}")
print(f"canonical_input_mutations={canonical_mutations}")
print(f"submitted_input_mutations={submitted_mutations}")
if mismatches:
    print(json.dumps(mismatches[:10], ensure_ascii=False, indent=2))
    raise SystemExit(1)
