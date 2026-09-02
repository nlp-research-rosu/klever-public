#!/usr/bin/env python3
"""Independent differential check for trusted and submitted strlen functions."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path


sys.dont_write_bytecode = True
TRUSTED_PATH = Path("/tmp/audit-work/23-strlen/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/23-strlen/candidate/solution.py")
RESULTS_PATH = Path("/audit-output/evidence/03-differential-cases.json")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strlen


trusted_strlen = load_function(TRUSTED_PATH, "trusted_canonical")
generated_strlen = load_function(GENERATED_PATH, "submitted_solution")

cases: list[tuple[str, str]] = [
    ("documented-empty", ""),
    ("documented-abc", "abc"),
    ("boundary-one-ascii", "x"),
    ("boundary-two-ascii", "xy"),
    ("whitespace", " \t\n\r"),
    ("embedded-nul", "a\x00b"),
    ("bmp-unicode", "λ漢字"),
    ("astral-unicode", "🙂🧪"),
    ("combining-sequence", "e\u0301"),
    ("repeated-4096", "z" * 4096),
]

rng = random.Random(230023)
alphabet = ["a", "Z", "0", " ", "\n", "\x00", "λ", "漢", "🙂", "\u0301"]
for index in range(500):
    length = rng.randrange(0, 257)
    value = "".join(rng.choice(alphabet) for _ in range(length))
    cases.append((f"generated-{index:03d}", value))

results: list[dict[str, object]] = []
mismatches = 0
for label, value in cases:
    trusted = trusted_strlen(value)
    generated = generated_strlen(value)
    expected_structural_length = len(value)
    match = trusted == generated == expected_structural_length
    mismatches += not match
    results.append(
        {
            "label": label,
            "input": value,
            "python_codepoint_length": expected_structural_length,
            "trusted_result": trusted,
            "generated_result": generated,
            "match": match,
        }
    )

RESULTS_PATH.write_text(
    json.dumps(
        {
            "seed": 230023,
            "alphabet": alphabet,
            "case_count": len(cases),
            "mismatch_count": mismatches,
            "cases": results,
        },
        ensure_ascii=True,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

print(f"trusted={TRUSTED_PATH}")
print(f"generated={GENERATED_PATH}")
print("formal_domain=str (Python Unicode strings)")
print("control_flow_branches=0")
print(f"case_count={len(cases)}")
print(f"mismatch_count={mismatches}")
print(f"results={RESULTS_PATH}")
raise SystemExit(1 if mismatches else 0)
