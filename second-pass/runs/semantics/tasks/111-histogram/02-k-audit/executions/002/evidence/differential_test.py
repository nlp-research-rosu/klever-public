#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval 111."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/111-histogram/solution.py")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(CANONICAL_PATH, "trusted_histogram_canonical").histogram
candidate = load(CANDIDATE_PATH, "audited_histogram_candidate").histogram

documented = [
    ("a b c", {"a": 1, "b": 1, "c": 1}),
    ("a b b a", {"a": 2, "b": 2}),
    ("a b c a b", {"a": 2, "b": 2}),
    ("b b b b a", {"b": 4}),
    ("", {}),
]

intended_cases: list[str] = []
for size in range(0, 8):
    intended_cases.extend(
        " ".join(tokens)
        for tokens in itertools.product("abc", repeat=size)
    )

rng = random.Random(111)
for _ in range(500):
    size = rng.randrange(0, 65)
    intended_cases.append(" ".join(rng.choice("abcdef") for _ in range(size)))

branch_cases = [
    "",
    "a",
    "a a",
    "a b",
    "a a b",
    "a b b",
    "a b a",
    "a b c",
    "a a b b",
    "a b b c c",
    "a a b b c c",
    "a a a b b c",
    "a b b b c c c",
    "z y x z y",
]
intended_cases.extend(branch_cases)

mismatches: list[tuple[str, dict[str, int], dict[str, int]]] = []
for text in intended_cases:
    expected = canonical(text)
    actual = candidate(text)
    if expected != actual:
        mismatches.append((text, expected, actual))

print("DOCUMENTED_EXAMPLES")
for text, expected in documented:
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    print(
        repr(text),
        f"specified={expected!r}",
        f"canonical={canonical_result!r}",
        f"candidate={candidate_result!r}",
    )
    assert canonical_result == expected
    assert candidate_result == expected

print(
    "INTENDED_SCOPE "
    "all token sequences of lengths 0..7 over {a,b,c}; "
    "500 deterministic random sequences of lengths 0..64 over {a..f}; "
    "15 explicit branch-boundary cases"
)
print(f"INTENDED_CASE_COUNT={len(intended_cases)}")
print(f"INTENDED_MISMATCH_COUNT={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"INTENDED_MISMATCH={mismatch!r}")

# These are recorded separately because the prompt says space-separated lowercase
# letters and does not state that repeated/leading/trailing whitespace is accepted.
outside_strict_domain = [" a", "a ", "a  b", "a   a", "a\tb", "a\nb"]
print("EXPLORATORY_WHITESPACE_CASES")
for text in outside_strict_domain:
    print(
        repr(text),
        f"canonical={canonical(text)!r}",
        f"candidate={candidate(text)!r}",
        f"equal={canonical(text) == candidate(text)}",
    )

if mismatches:
    raise SystemExit(1)
