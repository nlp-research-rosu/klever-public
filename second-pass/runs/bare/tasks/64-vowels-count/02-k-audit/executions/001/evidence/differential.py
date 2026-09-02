#!/usr/bin/env python3
"""Independent differential test for HumanEval 64.

The trusted canonical and candidate implementation are imported from distinct,
explicit paths.  A third, direct contract oracle is used so agreement between
the two implementations is not the sole check.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


def contract_oracle(s: str) -> int:
    return sum(ch in "aeiouAEIOU" for ch in s) + int(
        bool(s) and s[-1] in "yY"
    )


def outcome(fn, s: str):
    try:
        return {"kind": "value", "value": fn(s)}
    except Exception as exc:  # record, rather than hide, boundary behavior
        return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}


canonical = load_function(
    "trusted_canonical", Path("/reference/canonical.py")
)
generated = load_function(
    "scratch_generated", Path("/tmp/audit-work/candidate-src/solution.py")
)

named_cases = [
    "abcde",  # documented example
    "ACEDY",  # documented example and final uppercase Y
    "",       # empty boundary
    "a", "A", "u", "U",  # vowel branch and length-one boundary
    "y", "Y",              # final-y branch
    "b", "é", "😀",        # default branch, including Unicode
    "ay", "aY", "ya", "Ya", "yy", "YYY", "rhythm", "rhythmy",
    "aeiouAEIOU", "bcdfg", "Yodel", "toy", "toys",
]

# Exhaustive short inputs span every semantic character class and all branch
# transitions. Random cases add broader lengths and Unicode representatives.
alphabet = ["a", "A", "y", "Y", "b", "é", "😀"]
generated_cases = [
    "".join(chars)
    for length in range(0, 5)
    for chars in itertools.product(alphabet, repeat=length)
]
rng = random.Random(640064)
random_alphabet = "aeiouAEIOUyYbcdfgXYZéΩ😀"
random_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 81)))
    for _ in range(500)
]

cases = list(dict.fromkeys(named_cases + generated_cases + random_cases))
mismatches = []
candidate_contract_mismatches = []
canonical_contract_mismatches = []
for s in cases:
    can = outcome(canonical, s)
    gen = outcome(generated, s)
    expected = contract_oracle(s)
    if can != gen:
        mismatches.append({"input": s, "canonical": can, "generated": gen})
    if gen != {"kind": "value", "value": expected}:
        candidate_contract_mismatches.append(
            {"input": s, "expected": expected, "generated": gen}
        )
    # The trusted canonical intentionally indexes s[-1], so its empty-string
    # exception is reported separately from its nonempty contract behavior.
    if s and can != {"kind": "value", "value": expected}:
        canonical_contract_mismatches.append(
            {"input": s, "expected": expected, "canonical": can}
        )

print(f"case_count={len(cases)}")
print(f"candidate_contract_mismatch_count={len(candidate_contract_mismatches)}")
print(f"canonical_nonempty_contract_mismatch_count={len(canonical_contract_mismatches)}")
print(f"canonical_vs_generated_mismatch_count={len(mismatches)}")
print("canonical_vs_generated_mismatches=")
print(json.dumps(mismatches, ensure_ascii=False, indent=2))
print("named_case_results=")
for s in named_cases:
    print(
        json.dumps(
            {
                "input": s,
                "oracle": contract_oracle(s),
                "canonical": outcome(canonical, s),
                "generated": outcome(generated, s),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )

if candidate_contract_mismatches or canonical_contract_mismatches:
    raise SystemExit(1)
