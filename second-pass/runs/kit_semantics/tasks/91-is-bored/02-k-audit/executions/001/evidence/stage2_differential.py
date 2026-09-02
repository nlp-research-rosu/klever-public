#!/usr/bin/env python3
"""Independent differential and docstring-resolution checks for HumanEval 91."""

from __future__ import annotations

import importlib.util
import itertools
import random
import re
from collections import Counter
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/case91")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


candidate = load_entry(SCRATCH / "solution.py", "audit_candidate")
canonical = load_entry(SCRATCH / "canonical.py", "audit_canonical")


def documented_resolution(text: str) -> int:
    """Independent split-based reading of the candidate's documented boundary.

    A sentence is each maximal segment between '.', '?', or '!'. Leading
    whitespace is formatting. Its first word is I when the first non-whitespace
    character is ASCII I and is followed by whitespace or the segment's end.
    """

    result = 0
    for sentence in re.split(r"[.?!]", text):
        remaining = sentence.lstrip()
        if remaining == "I" or (
            len(remaining) >= 2
            and remaining[0] == "I"
            and remaining[1].isspace()
        ):
            result += 1
    return result


documented_examples = [
    ("Hello world", 0),
    ("The sky is blue. The sun is shining. I love this weather", 1),
]

branch_and_boundary_cases = [
    "",
    "I",
    "I ",
    "I.",
    "I?",
    "I!",
    "Idea",
    "Ix",
    "I x",
    "I\tx",
    "I\nx",
    "I\vx",
    "I\fx",
    "I\u00a0x",
    "I\u2003x",
    " I work",
    "\tI work",
    ".I?",
    "!.I !",
    "x I work",
    "x.I work",
    "x? I work",
    "x!\tI work",
    "...",
    " . ? ! ",
    "I..I??I!!",
    "I,I",
    "I, too.",
    "İ work",
    "𝐈 work",
    "I😀",
    "😀. I smile",
]

alphabet = ("I", "x", " ", "\t", ".", "?", "!", ",")
exhaustive = (
    "".join(chars)
    for length in range(0, 6)
    for chars in itertools.product(alphabet, repeat=length)
)

rng = random.Random(9100730)
random_alphabet = (
    "I",
    "x",
    "a",
    " ",
    "\t",
    "\n",
    "\v",
    "\f",
    "\u00a0",
    "\u2003",
    ".",
    "?",
    "!",
    ",",
    "😀",
    "İ",
)
random_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 41)))
    for _ in range(10_000)
]

ordered_cases: list[str] = []
seen: set[str] = set()
for value in (
    [text for text, _ in documented_examples]
    + branch_and_boundary_cases
    + list(exhaustive)
    + random_cases
):
    if value not in seen:
        seen.add(value)
        ordered_cases.append(value)

for text, expected in documented_examples:
    actual = candidate(text)
    if actual != expected:
        raise AssertionError(
            f"documented example failed: {text!r}: expected={expected}, actual={actual}"
        )

doc_mismatches: list[tuple[str, int, int]] = []
canonical_mismatches: list[tuple[str, int, int, int]] = []
canonical_direction = Counter()
for text in ordered_cases:
    got = candidate(text)
    doc = documented_resolution(text)
    trusted_witness = canonical(text)
    if got != doc:
        doc_mismatches.append((text, got, doc))
    if got != trusted_witness:
        canonical_mismatches.append((text, got, trusted_witness, doc))
        canonical_direction[(got > trusted_witness, got < trusted_witness)] += 1

print("COMMAND: python3 /audit-output/evidence/stage2_differential.py")
print(f"documented_examples={len(documented_examples)} passed")
print(f"branch_boundary_cases={len(branch_and_boundary_cases)}")
print(
    "exhaustive_scope=all strings length 0..5 over "
    + repr("".join(alphabet))
)
print(
    "random_scope=10000 deterministic strings length 0..40 over "
    + repr("".join(random_alphabet))
    + " seed=9100730"
)
print(f"unique_cases={len(ordered_cases)}")
print(f"candidate_vs_documented_resolution_mismatches={len(doc_mismatches)}")
print(f"candidate_vs_canonical_mismatches={len(canonical_mismatches)}")
print(f"canonical_mismatch_directions={dict(canonical_direction)}")

print("branch_boundary_results:")
for text in branch_and_boundary_cases:
    print(
        f"  input={text!r} candidate={candidate(text)} "
        f"canonical={canonical(text)} documented_resolution={documented_resolution(text)}"
    )

print("first_80_candidate_vs_canonical_mismatches:")
for text, got, trusted_witness, doc in canonical_mismatches[:80]:
    print(
        f"  input={text!r} candidate={got} canonical={trusted_witness} "
        f"documented_resolution={doc}"
    )

if doc_mismatches:
    print("first_80_candidate_vs_documented_resolution_mismatches:")
    for text, got, doc in doc_mismatches[:80]:
        print(f"  input={text!r} candidate={got} documented_resolution={doc}")
    raise SystemExit(1)

print("RESULT=PASS")
