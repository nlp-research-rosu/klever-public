#!/usr/bin/env python3
"""Independent differential test for HumanEval 134.

Oracle: /reference/canonical.py.
Candidate implementation: the scratch copy of /candidate/solution.py.

The fixed cases cover all examples and every branch boundary in the candidate.
The generated corpus exhausts lengths 0..4 over a representative alphabet and
adds deterministic random strings of lengths 0..12. Results include exceptions.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


def outcome(function, argument: str):
    try:
        return ("return", function(argument))
    except Exception as error:  # The reference itself is part of the oracle.
        return ("raise", type(error).__name__, str(error))


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_134")
candidate = load_entry(
    Path("/tmp/audit-work/source/solution.py"), "scratch_candidate_134"
)

fixed_cases = [
    # Documented examples.
    "apple pie",
    "apple pi e",
    "apple pi e ",
    "",
    # len == 1 boundary; alphabetic true/false.
    "A",
    "z",
    "7",
    " ",
    "é",
    "α",
    "İ",
    # len > 1 boundary, final-alphabetic and penultimate-space boundaries.
    " a",
    " 1",
    "aa",
    "aA",
    "a ",
    "  ",
    "x a",
    "x  a",
    "x\tA",
    "\t A",
    # Representative non-ASCII final letters.
    "x é",
    "x α",
    "x K",
    "x ſ",
]

exhaustive_alphabet = ["a", "Z", "0", " ", "\t", "é", "α"]
exhaustive_cases = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(exhaustive_alphabet, repeat=length)
]

random_source = random.Random(134)
random_alphabet = exhaustive_alphabet + ["_", "-", "K", "İ", "\n"]
random_cases = [
    "".join(random_source.choice(random_alphabet) for _ in range(length))
    for length in range(13)
    for _ in range(40)
]

# Preserve order while eliminating duplicate test inputs.
cases = list(dict.fromkeys(fixed_cases + exhaustive_cases + random_cases))
mismatches = []
for text in cases:
    expected = outcome(canonical, text)
    actual = outcome(candidate, text)
    if expected != actual:
        mismatches.append((text, expected, actual))

print("oracle=/reference/canonical.py:check_if_last_char_is_a_letter")
print("candidate=/tmp/audit-work/source/solution.py:check_if_last_char_is_a_letter")
print(f"fixed_cases={len(fixed_cases)}")
print(
    "exhaustive_scope=all strings of lengths 0..4 over "
    + repr(exhaustive_alphabet)
)
print(
    "random_scope=40 strings per length 0..12, seed=134, alphabet="
    + repr(random_alphabet)
)
print(f"unique_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for text, expected, actual in mismatches[:100]:
    print(f"MISMATCH input={text!r} canonical={expected!r} candidate={actual!r}")
if len(mismatches) > 100:
    print(f"MISMATCH_OUTPUT_TRUNCATED remaining={len(mismatches) - 100}")

# A differential mismatch is evidence, not a harness failure; keep exit zero so
# the full audit can proceed and judge it.
