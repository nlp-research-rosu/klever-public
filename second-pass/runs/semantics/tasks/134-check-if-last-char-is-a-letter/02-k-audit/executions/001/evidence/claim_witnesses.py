#!/usr/bin/env python3
"""Ground witnesses for every entry precondition and one Unicode fidelity witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


canonical = load_function("witness_canonical", "/tmp/audit-work/canonical.py")
candidate = load_function(
    "witness_candidate", "/tmp/audit-work/candidate-src/solution.py"
)

witnesses = [
    ("audit-empty", "", False, "empty IntSeq"),
    ("audit-one-alpha", "a", True, "C=97; isAlphaC(97)=true"),
    ("audit-one-nonalpha", "7", False, "C=55; isAlphaC(55)=false"),
    (
        "audit-long-true",
        " a",
        True,
        "PREFIX=.IntSeq; PREV=32; LAST=97",
    ),
    (
        "audit-long-last-nonalpha",
        "a!",
        False,
        "PREFIX=.IntSeq; PREV=97; LAST=33; isAlphaC(33)=false",
    ),
    (
        "audit-long-prev-nonspace",
        "aa",
        False,
        "PREFIX=.IntSeq; PREV=97; LAST=97; PREV=/=32",
    ),
    (
        "audit-one-nonalpha-unicode-instance",
        "é",
        False,
        "C=233; supplied isAlphaC(233)=false",
    ),
    (
        "audit-long-last-nonalpha-unicode-instance",
        " é",
        False,
        "PREFIX=.IntSeq; PREV=32; LAST=233; supplied isAlphaC(233)=false",
    ),
]

mismatch_count = 0
for claim, value, formal_result, substitution in witnesses:
    canonical_result = canonical(value)
    candidate_result = candidate(value)
    agrees_both = formal_result == canonical_result == candidate_result
    mismatch_count += 0 if agrees_both else 1
    print(
        f"claim={claim} input={value!r} substitution={substitution}; "
        f"formal={formal_result!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r} agrees_both={agrees_both}"
    )

print(f"witness_count={len(witnesses)}")
print(f"formal_vs_both_mismatch_count={mismatch_count}")
raise SystemExit(1 if mismatch_count else 0)
