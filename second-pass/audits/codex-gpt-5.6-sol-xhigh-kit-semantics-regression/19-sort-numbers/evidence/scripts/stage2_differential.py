#!/usr/bin/env python3
"""Independent differential tests for HumanEval 19 over its intended domain."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
import random
from typing import Any, Callable


EVIDENCE = Path("/audit-output/evidence")
REFERENCE = Path("/reference/canonical.py")
CANDIDATE = Path("/candidate/solution.py")
WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def load_entry(module_name: str, path: Path) -> Callable[[str], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


canonical = load_entry("trusted_humaneval19_canonical", REFERENCE)
generated = load_entry("submitted_humaneval19_solution", CANDIDATE)

cases: list[dict[str, Any]] = []


def add(category: str, value: str) -> None:
    cases.append({"id": len(cases), "category": category, "input": value})


# Stated example, empty boundary, all rank branches, and all comparison/equality
# boundaries represented by every ordered pair of valid words.
add("documented-example", "three one five")
add("empty", "")
for word in WORDS:
    add("singleton", word)
for left, right in itertools.product(WORDS, repeat=2):
    add("all-ordered-pairs", f"{left} {right}")

# Sequence and ASCII-space boundaries accepted by the reference implementation.
add("ascending", " ".join(WORDS))
add("descending", " ".join(reversed(WORDS)))
add("duplicate-heavy", "nine zero nine zero five five one one")
add("leading-space", "  three one")
add("trailing-space", "three one  ")
add("repeated-space", "three   one five")
add("only-spaces", "     ")

rng = random.Random(190019)
for _ in range(256):
    length = rng.randrange(0, 31)
    tokens = [rng.choice(WORDS) for _ in range(length)]
    add("seeded-generated", " ".join(tokens))


def call(fn: Callable[[str], str], value: str) -> dict[str, str]:
    try:
        return {"kind": "return", "value": fn(value)}
    except Exception as err:  # evidence records discrepancies, including exceptions
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


results = []
mismatches = []
for case in cases:
    reference_result = call(canonical, case["input"])
    candidate_result = call(generated, case["input"])
    row = {
        **case,
        "canonical": reference_result,
        "candidate": candidate_result,
        "match": reference_result == candidate_result,
    }
    results.append(row)
    if not row["match"]:
        mismatches.append(row)

# Characterize, but do not count as intended-domain failures, Python whitespace
# behavior that the prompt's space-delimited domain excludes.
outside_domain = []
for value in ("one\ttwo", "one\ntwo", "one\u00a0two"):
    outside_domain.append({
        "input": value,
        "canonical": call(canonical, value),
        "candidate": call(generated, value),
    })

(EVIDENCE / "stage2-inputs.json").write_text(
    json.dumps({"intended_domain": cases, "outside_domain_probes": [row["input"] for row in outside_domain]},
               indent=2, sort_keys=True)
    + "\n"
)
(EVIDENCE / "stage2-results.json").write_text(
    json.dumps({"results": results, "outside_domain": outside_domain}, indent=2, sort_keys=True) + "\n"
)

category_counts: dict[str, int] = {}
for case in cases:
    category_counts[case["category"]] = category_counts.get(case["category"], 0) + 1

print(json.dumps({
    "canonical": str(REFERENCE),
    "candidate": str(CANDIDATE),
    "case_count": len(cases),
    "category_counts": category_counts,
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
    "outside_domain": outside_domain,
}, indent=2, sort_keys=True))

raise SystemExit(0 if not mismatches else 1)
