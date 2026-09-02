#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable

EVIDENCE = Path("/audit-output/evidence")
WORK = Path("/tmp/audit-work/79-decimal-to-binary")


def load_entry(module_name: str, path: Path) -> Callable[[Any], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decimal_to_binary


def outcome(function: Callable[[Any], str], value: Any) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(value)}
    except Exception as err:  # Intentional: compare rejection behavior too.
        return {
            "kind": "exception",
            "type": type(err).__name__,
            "message": str(err),
        }


canonical = load_entry("trusted_canonical", WORK / "canonical.py")
candidate = load_entry("generated_candidate", WORK / "solution.py")

documented = [15, 32]
nonnegative_boundaries = [0, 1, 2, 3]
for exponent in range(1, 129):
    pivot = 1 << exponent
    nonnegative_boundaries.extend([pivot - 1, pivot, pivot + 1])

rng = random.Random(790079)
generated_nonnegative = []
for _ in range(512):
    bits = rng.randrange(0, 1025)
    generated_nonnegative.append(rng.getrandbits(bits))

out_of_domain_informational = [-32, -2, -1, True, False, None, "", [], 3.5]
valid_cases = documented + nonnegative_boundaries + generated_nonnegative
all_cases = valid_cases + out_of_domain_informational

(EVIDENCE / "differential_inputs.json").write_text(
    json.dumps(
        {
            "seed": 790079,
            "documented": documented,
            "nonnegative_boundaries": nonnegative_boundaries,
            "generated_nonnegative": generated_nonnegative,
            "out_of_domain_informational": out_of_domain_informational,
        },
        indent=2,
        sort_keys=True,
    )
    + "\n"
)

mismatches = []
valid_return_shape_failures = []
for index, value in enumerate(all_cases):
    expected = outcome(canonical, value)
    actual = outcome(candidate, value)
    if actual != expected:
        mismatches.append(
            {"index": index, "input": value, "canonical": expected, "candidate": actual}
        )
    if index < len(valid_cases) and actual["kind"] == "return":
        rendered = actual["value"]
        payload = rendered[2:-2] if rendered.startswith("db") and rendered.endswith("db") else ""
        if (
            not rendered.startswith("db")
            or not rendered.endswith("db")
            or not payload
            or set(payload) - {"0", "1"}
        ):
            valid_return_shape_failures.append(
                {"index": index, "input": value, "result": rendered}
            )

summary = {
    "valid_case_count": len(valid_cases),
    "out_of_domain_informational_count": len(out_of_domain_informational),
    "total_case_count": len(all_cases),
    "mismatch_count": len(mismatches),
    "valid_return_shape_failure_count": len(valid_return_shape_failures),
    "mismatches": mismatches,
    "valid_return_shape_failures": valid_return_shape_failures,
}
(EVIDENCE / "differential_results.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(0 if not mismatches and not valid_return_shape_failures else 1)
