#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted solution."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path, module_name: str) -> Callable[[Any, Any], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def normalize_value(value: Any) -> dict[str, str]:
    if isinstance(value, float) and math.isnan(value):
        representation = "nan"
    else:
        representation = repr(value)
    return {"kind": "return", "type": type(value).__name__, "repr": representation}


def observe(function: Callable[[Any, Any], Any], a: Any, b: Any) -> dict[str, str]:
    try:
        return normalize_value(function(a, b))
    except Exception as error:  # noqa: BLE001 - exception behavior is observed.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "repr": str(error),
        }


def is_intended_value(value: Any) -> bool:
    if type(value) is int:
        return True
    if type(value) is float:
        return math.isfinite(value)
    if type(value) is str:
        try:
            converted = float(value.replace(",", "."))
        except ValueError:
            return False
        return math.isfinite(converted)
    return False


def key(value: Any) -> tuple[str, str]:
    return (type(value).__name__, repr(value))


def bounded_record(record: dict[str, Any]) -> dict[str, Any]:
    display = json.loads(json.dumps(record))
    for side in ("a", "b", "canonical", "submitted"):
        representation = display[side]["repr"]
        if len(representation) > 160:
            display[side]["repr"] = (
                representation[:72]
                + f"...<{len(representation)} chars>..."
                + representation[-32:]
            )
    return display


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
    submitted = load_function(
        Path("/tmp/audit-work/137-compare-one/solution.py"), "submitted_solution"
    )

    documented = [
        (1, 2.5),
        (1, "2,3"),
        ("5,1", "6"),
        ("1", 1),
    ]
    branch_boundaries = [
        (0, 0),
        (-1, 0),
        (1, 0),
        (1.0, 1),
        (-0.0, 0.0),
        ("-2,5", -2),
        ("2.5", "2,50"),
        ("1e3", 999.0),
        (2**53, float(2**53)),
        (2**53 + 1, float(2**53)),
        (-(2**53 + 1), -float(2**53)),
        (10**400, 10**400 - 1),
    ]
    empty_and_invalid = [
        ("", 0),
        (" ", 0),
        (",", 0),
        (".", 0),
        ("abc", 0),
        ("1,2,3", 0),
    ]
    generated_values = [
        -(10**400),
        -(2**53 + 1),
        -(2**53),
        -101,
        -1,
        0,
        1,
        2,
        2**53,
        2**53 + 1,
        10**400,
        -math.inf,
        -float(2**53),
        -2.5,
        -0.0,
        0.0,
        0.5,
        1.0,
        2.5,
        float(2**53),
        math.inf,
        math.nan,
        "-9007199254740993",
        "-2,5",
        "-0",
        "0",
        "0,0",
        "1",
        "1.0",
        "1,5",
        "2.5",
        "5,1",
        "6",
        "1e3",
        "+3.25",
        " 2.0 ",
        "",
        " ",
        ",",
        ".",
        "abc",
        "1,2,3",
    ]

    cases: list[tuple[str, Any, Any]] = []
    for index, (a, b) in enumerate(documented):
        cases.append((f"documented-{index}", a, b))
    for index, (a, b) in enumerate(branch_boundaries):
        cases.append((f"boundary-{index}", a, b))
    for index, (a, b) in enumerate(empty_and_invalid):
        cases.append((f"invalid-{index}", a, b))
    cases.extend(
        (f"cross-{index}", a, b)
        for index, (a, b) in enumerate(
            itertools.product(generated_values, generated_values)
        )
    )

    # Preserve order while removing duplicates from overlapping categories.
    unique_cases: list[tuple[str, Any, Any]] = []
    seen: set[tuple[tuple[str, str], tuple[str, str]]] = set()
    for label, a, b in cases:
        pair_key = (key(a), key(b))
        if pair_key not in seen:
            seen.add(pair_key)
            unique_cases.append((label, a, b))

    mismatch_records: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    intended_count = 0
    intended_mismatches = 0
    extended_mismatches = 0
    documented_mismatches = 0
    for label, a, b in unique_cases:
        intended = is_intended_value(a) and is_intended_value(b)
        intended_count += int(intended)
        canonical_result = observe(canonical, a, b)
        submitted_result = observe(submitted, a, b)
        record = {
            "label": label,
            "a": {"type": type(a).__name__, "repr": repr(a)},
            "b": {"type": type(b).__name__, "repr": repr(b)},
            "intended_domain": intended,
            "canonical": canonical_result,
            "submitted": submitted_result,
        }
        all_records.append(record)
        if canonical_result != submitted_result:
            mismatch_records.append(record)
            intended_mismatches += int(intended)
            extended_mismatches += int(not intended)
            documented_mismatches += int(label.startswith("documented-"))

    encoded_records = json.dumps(
        all_records, sort_keys=True, separators=(",", ":")
    ).encode()
    print(f"DOCUMENTED_CASES: {len(documented)}")
    print(f"UNIQUE_CASES: {len(unique_cases)}")
    print(f"INTENDED_DOMAIN_CASES: {intended_count}")
    print(f"DOCUMENTED_MISMATCHES: {documented_mismatches}")
    print(f"INTENDED_DOMAIN_MISMATCHES: {intended_mismatches}")
    print(f"EXTENDED_OR_INVALID_MISMATCHES: {extended_mismatches}")
    print(f"ALL_OBSERVATIONS_SHA256: {hashlib.sha256(encoded_records).hexdigest()}")
    print("MISMATCHES_BEGIN")
    for record in mismatch_records[:12]:
        print(json.dumps(bounded_record(record), sort_keys=True))
    if len(mismatch_records) > 12:
        print(f"... {len(mismatch_records) - 12} additional mismatches omitted from log")
    print("MISMATCHES_END")
    return 1 if intended_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
