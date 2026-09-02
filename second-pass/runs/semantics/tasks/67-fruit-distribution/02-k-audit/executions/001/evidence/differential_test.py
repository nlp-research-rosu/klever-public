#!/usr/bin/env python3
"""Independent differential tests for the trusted canonical and submitted source."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
SUBMITTED_PATH = Path("/tmp/audit-work/reconstruction/solution.py")


def load_function(path: Path, module_name: str) -> Callable[[str, int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fruit_distribution


@dataclass(frozen=True)
class Case:
    category: str
    sentence: str
    total: int
    intended_domain: bool


def outcome(function: Callable[[str, int], int], case: Case) -> dict[str, object]:
    try:
        return {"kind": "return", "value": function(case.sentence, case.total)}
    except Exception as error:  # The exception type is the observable under comparison.
        return {"kind": "exception", "type": type(error).__name__, "text": str(error)}


canonical = load_function(CANONICAL_PATH, "trusted_canonical")
submitted = load_function(SUBMITTED_PATH, "submitted_solution")

cases: list[Case] = [
    Case("documented-example", "5 apples and 6 oranges", 19, True),
    Case("documented-example", "0 apples and 1 oranges", 3, True),
    Case("documented-example", "2 apples and 3 oranges", 100, True),
    Case("documented-example", "100 apples and 1 oranges", 120, True),
    Case("zero-boundary", "0 apples and 0 oranges", 0, True),
    Case("left-zero-boundary", "0 apples and 7 oranges", 7, True),
    Case("right-zero-boundary", "9 apples and 0 oranges", 9, True),
    Case("all-fruit-consumed-boundary", "9 apples and 7 oranges", 16, True),
    Case("large-decimal-boundary", "999999 apples and 1000001 oranges", 3000000, True),
    # Required empty and robustness probes. These do not satisfy the exact sentence
    # grammar and therefore are explicitly outside the intended/formal domain.
    Case("empty-string-probe", "", 0, False),
    Case("whitespace-only-probe", "   ", 0, False),
    Case("missing-number-probe", "5 apples and oranges", 10, False),
    Case("extra-number-probe", "5 apples and 6 oranges and 1 pear", 20, False),
    Case("negative-count-probe", "-1 apples and 2 oranges", 10, False),
    Case("tab-delimiter-probe", "5\tapples\tand\t6\toranges", 19, False),
    Case("repeated-space-probe", "5  apples and  6 oranges", 19, False),
]

# Exhaustive small exact-grammar boundary grid. The total ranges from the
# minimum valid total A+B through A+B+3.
for apples in range(0, 9):
    for oranges in range(0, 9):
        for mangoes in range(0, 4):
            cases.append(
                Case(
                    "small-exhaustive-grid",
                    f"{apples} apples and {oranges} oranges",
                    apples + oranges + mangoes,
                    True,
                )
            )

# Deterministic representative generated inputs across a wider numeric range.
generator = random.Random(670067)
for _ in range(2000):
    apples = generator.randint(0, 10**9)
    oranges = generator.randint(0, 10**9)
    mangoes = generator.randint(0, 10**9)
    cases.append(
        Case(
            "seeded-wide-sample",
            f"{apples} apples and {oranges} oranges",
            apples + oranges + mangoes,
            True,
        )
    )

records: list[dict[str, object]] = []
for case in cases:
    expected = outcome(canonical, case)
    actual = outcome(submitted, case)
    records.append(
        {
            "category": case.category,
            "sentence": case.sentence,
            "total": case.total,
            "intended_domain": case.intended_domain,
            "canonical": expected,
            "submitted": actual,
            "equal": expected == actual,
        }
    )

intended = [record for record in records if record["intended_domain"]]
outside = [record for record in records if not record["intended_domain"]]
intended_mismatches = [record for record in intended if not record["equal"]]
outside_mismatches = [record for record in outside if not record["equal"]]
serialized_inputs = json.dumps(
    [
        {
            "category": case.category,
            "sentence": case.sentence,
            "total": case.total,
            "intended_domain": case.intended_domain,
        }
        for case in cases
    ],
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode()

print(f"canonical_path={CANONICAL_PATH}")
print(f"submitted_path={SUBMITTED_PATH}")
print("formal/intended exact grammar: '<A> apples and <B> oranges'")
print("formal constraints: A >= 0, B >= 0, A + B <= N")
print("small grid: A,B in [0,8], mangoes=N-A-B in [0,3]")
print("wide sample: seed=670067, 2000 triples, each component in [0,10^9]")
print(f"total_cases={len(records)}")
print(f"intended_domain_cases={len(intended)}")
print(f"intended_domain_mismatches={len(intended_mismatches)}")
print(f"outside_domain_probes={len(outside)}")
print(f"outside_domain_mismatches={len(outside_mismatches)}")
print(f"input_manifest_sha256={hashlib.sha256(serialized_inputs).hexdigest()}")
print("outside_domain_results=")
print(json.dumps(outside, ensure_ascii=False, indent=2, sort_keys=True))
if intended_mismatches:
    print("intended_domain_mismatch_records=")
    print(json.dumps(intended_mismatches, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(1)
