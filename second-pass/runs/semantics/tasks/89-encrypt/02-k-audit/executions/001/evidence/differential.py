#!/usr/bin/env python3
"""Independent differential audit for HumanEval problem 89."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


canonical = load_entry(Path("/reference/canonical.py"), "audit_canonical")
generated = load_entry(
    Path("/tmp/audit-work/candidate/solution.py"), "audit_generated"
)

documented = ["hi", "asdfghjkl", "gf", "et"]
boundaries = [
    "",
    "a",
    "v",
    "w",
    "x",
    "y",
    "z",
    "abcdefghijklmnopqrstuvwxyz",
    "`",
    "{",
    "A",
    "Z",
    "0",
    "9",
    " ",
    "\n",
    "!",
    "~",
    "é",
    "🙂",
    "aA",
    "z{",
]

# Exhaust all one- and two-character lowercase strings. This covers every
# lowercase branch/wrap boundary in every position.
lowercase_exhaustive = [""]
for audit_len in (1, 2):
    lowercase_exhaustive.extend(
        "".join(chars)
        for chars in itertools.product(string.ascii_lowercase, repeat=audit_len)
    )

# Deterministic representative longer strings from the intended general-string
# domain, including lowercase, other ASCII, whitespace, and Unicode.
audit_rng = random.Random(890089)
alphabet = string.ascii_letters + string.digits + string.punctuation + " \n\téΩ🙂"
generated_inputs = []
for _ in range(1000):
    audit_len = audit_rng.randrange(0, 25)
    generated_inputs.append(
        "".join(audit_rng.choice(string.ascii_lowercase) for _ in range(audit_len))
    )
for _ in range(1000):
    audit_len = audit_rng.randrange(0, 25)
    generated_inputs.append(
        "".join(audit_rng.choice(alphabet) for _ in range(audit_len))
    )

groups = [
    ("documented", documented),
    ("branch-boundaries", boundaries),
    ("lowercase-exhaustive-len<=2", lowercase_exhaustive),
    ("generated-seed-890089", generated_inputs),
]

all_mismatches = []
print("ORACLE=/reference/canonical.py::encrypt")
print("SUBJECT=/tmp/audit-work/candidate/solution.py::encrypt")
for group_name, cases in groups:
    mismatches = []
    exceptions = []
    for value in cases:
        try:
            expected = canonical(value)
        except Exception as err:  # pragma: no cover - audit logging path
            expected = ("EXCEPTION", type(err).__name__, str(err))
        try:
            actual = generated(value)
        except Exception as err:  # pragma: no cover - audit logging path
            actual = ("EXCEPTION", type(err).__name__, str(err))
            exceptions.append((value, actual))
        if actual != expected:
            mismatches.append((value, expected, actual))
    all_mismatches.extend((group_name, *entry) for entry in mismatches)
    print(
        f"GROUP={group_name} CASES={len(cases)} "
        f"MISMATCHES={len(mismatches)} SUBJECT_EXCEPTIONS={len(exceptions)}"
    )
    for value, expected, actual in mismatches[:12]:
        print(
            "MISMATCH "
            f"group={group_name} input={value!r} "
            f"canonical={expected!r} generated={actual!r}"
        )
    if len(mismatches) > 12:
        print(f"MISMATCH_OUTPUT_TRUNCATED remaining={len(mismatches) - 12}")

print(f"TOTAL_MISMATCHES={len(all_mismatches)}")
sys.exit(1 if all_mismatches else 0)
