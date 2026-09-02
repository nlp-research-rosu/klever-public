#!/usr/bin/env python3
"""Independent differential test for HumanEval 17 parse_music."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/reconstruction/solution.py")
TOKENS = ("o", "o|", ".|")


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


def outcome(function, value: str):
    try:
        return {"kind": "return", "value": function(value)}
    except Exception as error:  # The exception class is observable here.
        return {"kind": "raise", "type": type(error).__name__, "args": error.args}


canonical = load(CANONICAL_PATH, "trusted_canonical")
generated = load(GENERATED_PATH, "audited_generated")

documented = ["o o| .| o| o| .| .| .| .| o o"]
boundary = [
    "",
    "o",
    "o|",
    ".|",
    "o o|",
    "o| .|",
    ".| o",
    "o o| .|",
    " o ",
    "  o|  ",
    "   .|   o   ",
]

exhaustive = []
for length in range(0, 6):
    for notes in itertools.product(TOKENS, repeat=length):
        if not notes:
            exhaustive.append("")
        else:
            exhaustive.append(" ".join(notes))
            exhaustive.append("  ".join(notes))

rng = random.Random(170017)
randomized = []
for _ in range(500):
    length = rng.randrange(0, 51)
    notes = [rng.choice(TOKENS) for _ in range(length)]
    if notes:
        separators = [" " * rng.randrange(1, 5) for _ in range(length - 1)]
        value = "".join(
            part
            for pair in zip(notes, separators + [""])
            for part in pair
        )
        value = (" " * rng.randrange(0, 4)) + value + (" " * rng.randrange(0, 4))
    else:
        value = " " * rng.randrange(0, 7)
    randomized.append(value)

# These deliberately explore inputs not described as valid space-delimited note
# sequences. They do not determine the intended-domain test exit status.
exploratory_out_of_domain = [
    "\t",
    "\n",
    "o\to|",
    "o\n.|",
    "x",
    "o x",
    "|",
]

intended_cases = []
seen = set()
for source, values in (
    ("documented", documented),
    ("boundary", boundary),
    ("exhaustive-length-0-through-5", exhaustive),
    ("deterministic-random-length-0-through-50", randomized),
):
    for value in values:
        if value not in seen:
            intended_cases.append({"source": source, "input": value})
            seen.add(value)

intended_mismatches = []
for case in intended_cases:
    expected = outcome(canonical, case["input"])
    actual = outcome(generated, case["input"])
    if expected != actual:
        intended_mismatches.append({**case, "canonical": expected, "generated": actual})

exploratory_results = []
for value in exploratory_out_of_domain:
    expected = outcome(canonical, value)
    actual = outcome(generated, value)
    exploratory_results.append(
        {
            "input": value,
            "canonical": expected,
            "generated": actual,
            "match": expected == actual,
        }
    )

corpus = {
    "intended_domain": "finite sequences over {o, o|, .|}, delimited by one or more ASCII spaces, with optional leading/trailing ASCII spaces",
    "canonical": str(CANONICAL_PATH),
    "generated": str(GENERATED_PATH),
    "seed": 170017,
    "intended_cases": intended_cases,
    "exploratory_out_of_domain": exploratory_out_of_domain,
}
results = {
    "intended_case_count": len(intended_cases),
    "intended_mismatch_count": len(intended_mismatches),
    "intended_mismatches": intended_mismatches,
    "exploratory_results": exploratory_results,
}
(EVIDENCE / "stage2_inputs.json").write_text(
    json.dumps(corpus, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
(EVIDENCE / "stage2_results.json").write_text(
    json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

print(json.dumps(results, indent=2, sort_keys=True))
raise SystemExit(1 if intended_mismatches else 0)
