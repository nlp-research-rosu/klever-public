#!/usr/bin/env python3
"""Independent docstring/canonical/candidate differential for HumanEval 99."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.closest_integer


canonical = load_function("trusted_canonical", "/reference/canonical.py")
candidate = load_function("submitted_solution", "/candidate/solution.py")


def invoke(function, text):
    try:
        value = function(text)
        return {"kind": "return", "type": type(value).__name__, "value": value}
    except Exception as err:
        return {
            "kind": "raise",
            "type": type(err).__name__,
            "value": str(err),
        }


def decimal_oracle(text):
    """Nearest integer of the exact finite Decimal denoted by text."""
    try:
        number = Decimal(text)
    except (InvalidOperation, ValueError):
        return None
    if not number.is_finite():
        return None
    return int(number.to_integral_value(rounding=ROUND_HALF_UP))


named_cases = [
    # Docstring examples.
    ("example", "10"),
    ("example", "15.3"),
    ("example", "14.5"),
    ("example", "-14.5"),
    # Zero, integer spellings, and both sign branches.
    ("boundary", "0"),
    ("boundary", "-0"),
    ("boundary", "0.0"),
    ("boundary", "-0.0"),
    ("boundary", "12."),
    ("boundary", "-12."),
    ("boundary", ".25"),
    ("boundary", "-.25"),
    # Every half boundary and immediate decimal neighbors.
    ("boundary", "0.49"),
    ("boundary", "0.5"),
    ("boundary", "0.51"),
    ("boundary", "-0.49"),
    ("boundary", "-0.5"),
    ("boundary", "-0.51"),
    ("boundary", "2.499999"),
    ("boundary", "2.500000"),
    ("boundary", "2.500001"),
    ("boundary", "-2.499999"),
    ("boundary", "-2.500000"),
    ("boundary", "-2.500001"),
    # Alternate numeric-string spellings, including ties not ending in ".5".
    ("spelling", "+14.5"),
    ("spelling", "014.500"),
    ("spelling", "145e-1"),
    ("spelling", "-145e-1"),
    ("spelling", "1.45e1"),
    ("spelling", "-1.45e1"),
    ("spelling", " 14.5 "),
    # Numeric-representation boundary probes.
    ("representation", "0.49999999999999994"),
    ("representation", "0.49999999999999999"),
    ("representation", "-0.49999999999999994"),
    ("representation", "-0.49999999999999999"),
    ("representation", "2.49999999999999999"),
    ("representation", "-2.49999999999999999"),
    ("representation", "9007199254740992.5"),
    ("representation", "-9007199254740992.5"),
    ("representation", "1e308"),
    ("representation", "-1e308"),
    ("representation", "5e-324"),
    ("representation", "-5e-324"),
    # Underspecified invalid/non-finite inputs; recorded but not scored.
    ("unspecified", ""),
    ("unspecified", "not-a-number"),
    ("unspecified", "nan"),
    ("unspecified", "inf"),
    ("unspecified", "-inf"),
]

generated = []
for n in range(-40, 41):
    generated.extend(
        [
            ("generated-grid", str(n)),
            ("generated-grid", f"{n}.25"),
            ("generated-grid", f"{n}.49"),
            ("generated-grid", f"{n}.50"),
            ("generated-grid", f"{n}.51"),
            ("generated-grid", f"{n}.75"),
        ]
    )

rng = random.Random(990073)
for _ in range(750):
    sign = "-" if rng.randrange(2) else ""
    integer = rng.randrange(0, 100_000)
    fraction = rng.randrange(0, 1_000_000)
    generated.append(("generated-random-6dp", f"{sign}{integer}.{fraction:06d}"))

cases = named_cases + generated
records = []
candidate_exact_mismatches = []
candidate_canonical_mismatches = []
candidate_doc_examples_bad = []

for category, text in cases:
    expected = decimal_oracle(text)
    cand = invoke(candidate, text)
    canon = invoke(canonical, text)
    record = {
        "category": category,
        "input": text,
        "exact_decimal_oracle": expected,
        "candidate": cand,
        "canonical": canon,
    }
    records.append(record)
    if cand != canon:
        candidate_canonical_mismatches.append(record)
    if expected is not None and cand != {
        "kind": "return",
        "type": "int",
        "value": expected,
    }:
        candidate_exact_mismatches.append(record)
    if category == "example" and cand != {
        "kind": "return",
        "type": "int",
        "value": expected,
    }:
        candidate_doc_examples_bad.append(record)

inputs_path = Path("/audit-output/evidence/stage2/differential-inputs.json")
results_path = Path("/audit-output/evidence/stage2/differential-results.json")
inputs_path.write_text(
    json.dumps(
        {
            "seed": 990073,
            "generated_random_count": 750,
            "cases": [{"category": c, "input": t} for c, t in cases],
        },
        indent=2,
        ensure_ascii=False,
    )
    + "\n"
)
results_path.write_text(
    json.dumps(
        {
            "records": records,
            "candidate_exact_mismatches": candidate_exact_mismatches,
            "candidate_canonical_mismatches": candidate_canonical_mismatches,
            "candidate_doc_examples_bad": candidate_doc_examples_bad,
        },
        indent=2,
        ensure_ascii=False,
    )
    + "\n"
)

input_hash = hashlib.sha256(inputs_path.read_bytes()).hexdigest()
print(f"case_count={len(cases)}")
print(f"input_manifest_sha256={input_hash}")
print(f"candidate_doc_examples_bad={len(candidate_doc_examples_bad)}")
print(f"candidate_exact_decimal_mismatches={len(candidate_exact_mismatches)}")
print(f"candidate_canonical_mismatches={len(candidate_canonical_mismatches)}")

print("candidate_exact_decimal_mismatch_records")
for record in candidate_exact_mismatches:
    print(json.dumps(record, sort_keys=True))

print("candidate_canonical_mismatch_records")
for record in candidate_canonical_mismatches:
    print(json.dumps(record, sort_keys=True))

assert not candidate_doc_examples_bad

# On the ordinary six-decimal generated domain, exact decimal behavior is
# docstring-determined and should not depend on exotic float representation.
ordinary_bad = [
    r
    for r in candidate_exact_mismatches
    if r["category"] in {"generated-grid", "generated-random-6dp"}
]
print(f"ordinary_generated_exact_mismatches={len(ordinary_bad)}")
assert not ordinary_bad
