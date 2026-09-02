#!/usr/bin/env python3
"""Ground satisfying witnesses for every candidate claim precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


def bored_summary(codes: tuple[int, ...], count: int, state: int) -> int:
    for code in codes:
        if code in (46, 63, 33):
            state = 0
        elif state == 0:
            if code == 32 or 9 <= code <= 13:
                state = 0
            elif code == 73:
                state = 1
            else:
                state = 2
        elif state == 1:
            if code == 32:
                count += 1
            state = 2
    return count


root = Path("/tmp/audit-work/fresh")
canonical = load(root / "canonical.py", "canonical_for_claim_witnesses")
candidate = load(root / "solution.py", "candidate_for_claim_witnesses")

witnesses = [
    # helper-claim label, internal initial state, remaining sequence, a whole
    # Python string that realizes the same scanner situation, expected result
    ("loop-state-0", 0, "I am", "I am", 1),
    ("loop-state-1", 1, " ", "I ", 1),
    ("loop-state-2", 2, ".I ", "x.I ", 1),
]

for label, state, remaining, whole, expected in witnesses:
    codes = tuple(ord(character) for character in remaining)
    summary = bored_summary(codes, 0, state)
    canonical_result = canonical(whole)
    candidate_result = candidate(whole)
    print(
        f"{label}: GLOBAL=.Map INPUT=.IntSeq N=0 "
        f"CH=str(.IntSeq) CODE=0 state={state} CS={codes!r}"
    )
    print('  requires notBool("ord" in_keys(.Map)) = true')
    print(
        f"  summary={summary} canonical({whole!r})={canonical_result} "
        f"candidate({whole!r})={candidate_result}"
    )
    assert summary == canonical_result == candidate_result == expected

examples = [
    ("prompt-example-0", "Hello world", 0),
    (
        "prompt-example-1",
        "The sky is blue. The sun is shining. I love this weather",
        1,
    ),
]
for label, text, expected in examples:
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    print(
        f"{label}: ground entry configuration input={text!r} "
        f"postcondition={expected} canonical={canonical_result} "
        f"candidate={candidate_result}"
    )
    assert canonical_result == candidate_result == expected

print("all_five_claim_preconditions_have_satisfying_ground_witnesses=True")
