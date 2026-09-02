#!/usr/bin/env python3
"""Ground witnesses for the entry and loop claim preconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_reverse_delete(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def kept_acc(s: str, c: str, accumulator: str) -> str:
    for character in s:
        if character not in c:
            accumulator += character
    return accumulator


def reversed_kept_acc(s: str, c: str, accumulator: str) -> str:
    for character in s:
        if character not in c:
            accumulator = character + accumulator
    return accumulator


def last_character(s: str, prior_value: str) -> str:
    return prior_value if not s else s[-1]


canonical = load_reverse_delete(Path("/reference/canonical.py"), "canonical_witness")
generated = load_reverse_delete(
    Path("/tmp/audit-work/review-112/reconstruction/solution.py"),
    "generated_witness",
)

entry_witnesses = []
for s, c in [("abcde", "ae"), ("", ""), ("abcdedcba", "ab")]:
    kept = kept_acc(s, c, "")
    reversed_kept = reversed_kept_acc(s, c, "")
    claimed = (kept, kept == reversed_kept)
    entry_witnesses.append(
        {
            "S_codepoints": [ord(ch) for ch in s],
            "C_codepoints": [ord(ch) for ch in c],
            "formal_claim_result": claimed,
            "canonical_result": canonical(s, c),
            "generated_result": generated(s, c),
        }
    )
    assert claimed == canonical(s, c) == generated(s, c)

# A fully ground LOOP-SPEC precondition witness:
# L=1, ORIG="a", C="", S="a", A="", RA="", V=str(""), P=parent(0).
# Only the listed local bindings are constrained by the claim; the framed cells
# can be any well-formed MPY state. Its claimed post-state is computed below.
loop_witness = {
    "pre": {
        "L": 1,
        "ORIG_codepoints": [97],
        "C_codepoints": [],
        "S_codepoints": [97],
        "A_codepoints": [],
        "RA_codepoints": [],
        "V": {"str_codepoints": []},
        "P": {"parent": 0},
    },
    "post": {
        "result_codepoints": [ord(ch) for ch in kept_acc("a", "", "")],
        "reversed_result_codepoints": [
            ord(ch) for ch in reversed_kept_acc("a", "", "")
        ],
        "character_codepoints": [
            ord(ch) for ch in last_character("a", "")
        ],
    },
}

print(
    json.dumps(
        {
            "entry_witnesses": entry_witnesses,
            "loop_witness": loop_witness,
            "all_entry_comparisons_equal": True,
        },
        ensure_ascii=False,
        indent=2,
    )
)
