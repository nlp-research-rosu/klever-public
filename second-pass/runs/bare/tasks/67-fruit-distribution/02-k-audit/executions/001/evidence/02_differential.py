#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


def load_function(path: str) -> Callable[[str, int], int]:
    module_path = Path(path)
    spec = importlib.util.spec_from_file_location(
        f"audit_{module_path.stem}_{hashlib.sha256(path.encode()).hexdigest()[:8]}",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fruit_distribution


def outcome(function: Callable[[str, int], int], s: str, n: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(s, n)}
    except Exception as error:  # Deliberately compare exception classes as behavior.
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


canonical = load_function("/reference/canonical.py")
candidate = load_function("/tmp/audit-work/fresh/solution.py")

documented = [
    ("5 apples and 6 oranges", 19),
    ("0 apples and 1 oranges", 3),
    ("2 apples and 3 oranges", 100),
    ("100 apples and 1 oranges", 120),
]
valid_boundaries = [
    ("0 apples and 0 oranges", 0),
    ("0 apples and 0 oranges", 1),
    ("1 apples and 0 oranges", 1),
    ("0 apples and 1 oranges", 1),
    ("999999 apples and 1 oranges", 1000000),
    ("5   apples and   6 oranges", 19),
    ("   5 apples and 6 oranges   ", 19),
]
out_of_domain_robustness = [
    ("", 0),
    ("apples and oranges", 9),
    ("5 apples 6 oranges", 20),
    ("-1 apples and 2 oranges", 5),
    ("5 apples and 6 oranges plus 2 labels", 20),
]

groups = [
    ("documented", documented),
    ("valid_boundary", valid_boundaries),
    ("out_of_domain_robustness", out_of_domain_robustness),
]

all_valid_generated: list[tuple[str, int]] = []
for apples in range(0, 26):
    for oranges in range(0, 26):
        for slack in (0, 1, 7, 101):
            total = apples + oranges + slack
            all_valid_generated.append(
                (f"{apples} apples and {oranges} oranges", total)
            )
groups.append(("generated_valid_grid", all_valid_generated))

overall_valid_mismatches = 0
overall_out_of_domain_mismatches = 0
for group_name, cases in groups:
    mismatches = []
    digest = hashlib.sha256()
    for s, n in cases:
        left = outcome(canonical, s, n)
        right = outcome(candidate, s, n)
        record = {
            "input": {"s": s, "n": n},
            "canonical": left,
            "candidate": right,
        }
        digest.update(
            (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        )
        if left != right:
            mismatches.append(record)
    print(
        json.dumps(
            {
                "group": group_name,
                "case_count": len(cases),
                "record_sha256": digest.hexdigest(),
                "mismatch_count": len(mismatches),
                "mismatches": mismatches,
            },
            sort_keys=True,
        )
    )
    if group_name == "out_of_domain_robustness":
        overall_out_of_domain_mismatches += len(mismatches)
    else:
        overall_valid_mismatches += len(mismatches)

print(f"valid_case_count={sum(len(c) for n, c in groups if n != 'out_of_domain_robustness')}")
print(f"valid_mismatch_count={overall_valid_mismatches}")
print(f"out_of_domain_mismatch_count={overall_out_of_domain_mismatches}")
raise SystemExit(1 if overall_valid_mismatches else 0)
