#!/usr/bin/env python3
"""Independent deterministic differential check for HumanEval problem 89."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import string
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


def outcome(fn, value: str):
    try:
        return {"kind": "return", "value": fn(value)}
    except Exception as exc:  # Evidence includes abnormal termination.
        return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function("generated_solution", Path("/tmp/audit-work/source/solution.py"))

documented = ["hi", "asdfghjkl", "gf", "et"]
boundaries = [
    "",
    "a",
    "v",
    "w",
    "x",
    "y",
    "z",
    "az",
    "wxyz",
    "A",
    "Z",
    "0",
    "9",
    " ",
    "!",
    "{",
    "\n",
    "é",
    "🙂",
    "aA",
    "a-z",
    "hello world",
]

# Exhaust all lowercase strings through length two.
exhaustive_lower = [""]
for length in (1, 2):
    exhaustive_lower.extend(
        "".join(chars)
        for chars in itertools.product(string.ascii_lowercase, repeat=length)
    )

rng = random.Random(890089)
lower_random = [
    "".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randrange(0, 65)))
    for _ in range(200)
]
mixed_alphabet = string.ascii_letters + string.digits + string.punctuation + " \té🙂"
mixed_random = [
    "".join(rng.choice(mixed_alphabet) for _ in range(rng.randrange(0, 40)))
    for _ in range(200)
]

# These show the concrete Python recursion-limit boundary. Keep the two lengths
# distinct because the exact threshold depends on call overhead.
long_cases = ["a" * 900, "a" * 1100]

inputs = []
seen = set()
for group, values in [
    ("documented", documented),
    ("boundaries", boundaries),
    ("exhaustive_lower_len_le_2", exhaustive_lower),
    ("generated_lower", lower_random),
    ("generated_mixed", mixed_random),
    ("long", long_cases),
]:
    for value in values:
        if value not in seen:
            seen.add(value)
            inputs.append({"group": group, "input": value})

records = []
for case in inputs:
    expected = outcome(canonical, case["input"])
    actual = outcome(generated, case["input"])
    records.append(
        {
            **case,
            "canonical": expected,
            "generated": actual,
            "match": expected == actual,
        }
    )

evidence_dir = Path("/audit-output/evidence")
(evidence_dir / "differential-inputs.json").write_text(
    json.dumps(inputs, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
(evidence_dir / "differential-results.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

mismatches = [record for record in records if not record["match"]]
by_group = {}
for record in records:
    stats = by_group.setdefault(record["group"], {"cases": 0, "mismatches": 0})
    stats["cases"] += 1
    stats["mismatches"] += int(not record["match"])

print(f"python={sys.version.split()[0]}")
print(f"total_cases={len(records)}")
print(f"total_mismatches={len(mismatches)}")
print("group_summary=" + json.dumps(by_group, sort_keys=True))
print("first_20_mismatches:")
for record in mismatches[:20]:
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))

# A differential mismatch is an audit finding, not a harness failure.
raise SystemExit(0)
