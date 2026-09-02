#!/usr/bin/env python3
"""Independent canonical-versus-generated differential for HumanEval/162."""

import importlib.util
import random
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/proof-162")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", SCRATCH / "canonical.py").string_to_md5
generated = load("generated_solution", SCRATCH / "solution.py").string_to_md5


def outcome(function, text):
    try:
        return ("return", function(text))
    except Exception as error:
        return ("raise", type(error).__name__)


documented = ["Hello world"]
boundaries = [
    "",
    "a",
    "\x00",
    "\x7f",
    "a\x00b",
    "\n",
    " " * 64,
    "a" * 65,
    "\x80",
    "é",
    "Ā",
    "中",
    "🙂",
    "ascii then é",
]

rng = random.Random(162)
ascii_alphabet = "".join(chr(code) for code in range(128))
unicode_alphabet = ascii_alphabet + "éĀ中🙂"
generated_inputs = []
for length in (2, 3, 7, 16, 31, 128):
    generated_inputs.append(
        "".join(rng.choice(ascii_alphabet) for _ in range(length))
    )
    generated_inputs.append(
        "".join(rng.choice(unicode_alphabet) for _ in range(length))
    )

cases = documented + boundaries + generated_inputs
mismatches = []
for index, text in enumerate(cases):
    left = outcome(canonical, text)
    right = outcome(generated, text)
    equal = left == right
    if not equal:
        mismatches.append((index, text, left, right))
    print(
        f"case={index:02d} input={text!r} "
        f"canonical={left!r} generated={right!r} equal={equal}"
    )

print(
    f"SUMMARY total={len(cases)} matches={len(cases)-len(mismatches)} "
    f"mismatches={len(mismatches)}"
)
for index, text, left, right in mismatches:
    print(
        f"MISMATCH case={index:02d} input={text!r} "
        f"canonical={left!r} generated={right!r}"
    )

# The documented example must agree; the complete differential deliberately
# exits nonzero if any intended string behavior differs.
assert outcome(canonical, "Hello world") == (
    "return",
    "3e25960a79dbc69b674cd4ec67a72c62",
)
raise SystemExit(1 if mismatches else 0)
