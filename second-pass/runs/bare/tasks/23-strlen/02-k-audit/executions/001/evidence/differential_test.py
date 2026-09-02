#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scratch = Path("/tmp/audit-work/reconstruction")
canonical = load_module("trusted_canonical", scratch / "canonical.py")
generated = load_module("candidate_solution", scratch / "solution.py")

# Documented examples, the empty/nonempty boundary, representation boundaries,
# and deterministic representative generated strings. There are no branches in
# the submitted one-expression implementation, so there are no algorithmic
# branch thresholds beyond empty versus nonempty input.
cases = [
    "",
    "a",
    "abc",
    " ",
    "\x00",
    "\n",
    "\"",
    "\\",
    "é",
    "e\u0301",
    "😀",
    "a😀é",
    "\U0010ffff",
    "a" * 255,
    "😀" * 256,
]

rng = random.Random(230023)
alphabet = ["a", "Z", "0", " ", "\x00", "\n", "é", "\u0301", "😀", "\U0010ffff"]
for length in list(range(0, 17)) + [31, 32, 33, 63, 64, 65, 127]:
    for _ in range(3):
        cases.append("".join(rng.choice(alphabet) for _ in range(length)))

mismatches = 0
for index, value in enumerate(cases):
    expected = canonical.strlen(value)
    actual = generated.strlen(value)
    if expected != actual:
        mismatches += 1
    print(
        f"case={index:03d} input={value!r} "
        f"python_len={len(value)} canonical={expected} candidate={actual}"
    )

print(f"TOTAL_CASES={len(cases)}")
print(f"MISMATCHES={mismatches}")
raise SystemExit(1 if mismatches else 0)
