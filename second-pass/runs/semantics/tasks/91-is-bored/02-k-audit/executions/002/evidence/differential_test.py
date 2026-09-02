#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/91."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


canonical = load_entry(
    Path("/tmp/audit-work/fresh/canonical.py"), "trusted_canonical_91"
)
candidate = load_entry(
    Path("/tmp/audit-work/fresh/solution.py"), "candidate_solution_91"
)

# The explicit suite contains both documented examples, empty/minimal strings,
# all scanner branch boundaries, every delimiter, ASCII whitespace boundaries,
# Unicode whitespace recognized by Python's regex engine, multiple sentences,
# and punctuation-adjacent cases.
explicit_cases = [
    "",
    "Hello world",
    "The sky is blue. The sun is shining. I love this weather",
    "I ",
    "I am bored",
    "I",
    "I.",
    "I?",
    "I!",
    "Ix",
    "I\t",
    " I am bored",
    "\tI am bored",
    "\nI am bored",
    "\rI am bored",
    "\vI am bored",
    "\fI am bored",
    ".I am bored",
    ". I am bored",
    ".\tI am bored",
    ".\nI am bored",
    ".\rI am bored",
    ".\vI am bored",
    ".\fI am bored",
    "? I am bored",
    "! I am bored",
    "x.I am bored",
    "x. I am bored",
    "x?I am bored",
    "x!I am bored",
    "x.  I am bored",
    "I am.I am",
    "I am. I am",
    "x I am",
    "x. x I am",
    "..I am",
    "?.I am",
    ".\u00a0I am bored",  # NO-BREAK SPACE after delimiter
    ".\u0085I am bored",  # NEXT LINE after delimiter
    ".\u2003I am bored",  # EM SPACE after delimiter
    ".\u2028I am bored",  # LINE SEPARATOR after delimiter
    "\u00a0I am bored",   # leading Unicode whitespace
    "  I start here!\tI tab-leading.\n\nI newline-leading",
    "I am bored. I think. You are not!  I agree?Is this counted? Ironic.",
]

rng = random.Random(910026)
alphabet = [
    "I",
    "a",
    "x",
    " ",
    "\t",
    "\n",
    "\r",
    "\v",
    "\f",
    ".",
    "?",
    "!",
    "\u00a0",
    "\u0085",
    "\u2003",
    "\u2028",
]
generated_cases = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 31)))
    for _ in range(1000)
]
cases = explicit_cases + generated_cases

mismatches: list[tuple[int, str, int, int]] = []
for index, text in enumerate(cases):
    expected = canonical(text)
    actual = candidate(text)
    if expected != actual:
        mismatches.append((index, text, expected, actual))

print(f"explicit_cases={len(explicit_cases)}")
print(f"generated_cases={len(generated_cases)}")
print(f"random_seed={910026}")
print(f"alphabet={alphabet!r}")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for index, text, expected, actual in mismatches[:40]:
    print(
        f"MISMATCH index={index} input={text!r} "
        f"canonical={expected} candidate={actual}"
    )

if mismatches:
    raise SystemExit(1)
