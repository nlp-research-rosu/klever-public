#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval 124."""

from __future__ import annotations

import importlib.util
import json
import random
import string
from pathlib import Path
from typing import Any, Callable


EVIDENCE_DIR = Path("/audit-output/evidence")


def load_entry(path: str, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def strict_ascii_contract(value: str) -> bool:
    """Independent direct reading of the stated mm-dd-yyyy contract."""
    if len(value) != 10 or value[2] != "-" or value[5] != "-":
        return False
    month_text, day_text, year_text = value[:2], value[3:5], value[6:]
    fields = (month_text, day_text, year_text)
    if not all(field and all("0" <= ch <= "9" for ch in field) for field in fields):
        return False
    month, day = int(month_text), int(day_text)
    if not 1 <= month <= 12 or day < 1:
        return False
    if month == 2:
        return day <= 29
    if month in (4, 6, 9, 11):
        return day <= 30
    return day <= 31


def record_case(cases: list[dict[str, Any]], seen: set[str], label: str, value: str) -> None:
    if value not in seen:
        seen.add(value)
        cases.append({"label": label, "input": value})


def main() -> int:
    canonical = load_entry("/reference/canonical.py", "trusted_canonical")
    generated = load_entry("/tmp/audit-work/candidate-src/solution.py", "generated_solution")

    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    explicit = [
        ("example_valid_31", "03-11-2000"),
        ("example_bad_month", "15-01-2012"),
        ("example_bad_width", "04-0-2040"),
        ("example_valid_30", "06-04-2020"),
        ("example_bad_separator", "06/04/2020"),
        ("empty", ""),
        ("length_9", "03-11-200"),
        ("length_11", "03-11-20000"),
        ("separator_2_bad", "03/11-2000"),
        ("separator_5_bad", "03-11/2000"),
        ("month_nondigit", "a3-11-2000"),
        ("day_nondigit", "03-a1-2000"),
        ("year_nondigit", "03-11-20a0"),
        ("month_00", "00-01-2020"),
        ("month_01", "01-01-2020"),
        ("month_02", "02-01-2020"),
        ("month_12", "12-01-2020"),
        ("month_13", "13-01-2020"),
        ("feb_day_00", "02-00-2020"),
        ("feb_day_01", "02-01-2020"),
        ("feb_day_29", "02-29-1900"),
        ("feb_day_30", "02-30-2020"),
        ("thirty_day_30", "04-30-2020"),
        ("thirty_day_31", "04-31-2020"),
        ("thirtyone_day_31", "01-31-0000"),
        ("thirtyone_day_32", "01-32-9999"),
        ("trimmed_valid", " 03-11-2000 "),
        ("single_digit_month", "3-11-2000"),
        ("single_digit_day", "03-1-2000"),
        ("short_year", "03-11-20"),
        ("arabic_indic_digits", "٠٣-١١-٢٠٠٠"),
        ("superscript_isdigit_not_int", "⁰3-11-2000"),
    ]
    for label, value in explicit:
        record_case(cases, seen, label, value)

    for year in ("0000", "2000", "9999"):
        for month in range(0, 14):
            for day in range(0, 33):
                record_case(
                    cases,
                    seen,
                    "exhaustive_ascii_boundary_grid",
                    f"{month:02d}-{day:02d}-{year}",
                )

    rng = random.Random(124)
    alphabet = string.digits + "-/ab " + "٠١٢"
    for _ in range(1000):
        length = rng.randrange(0, 15)
        value = "".join(rng.choice(alphabet) for _ in range(length))
        record_case(cases, seen, "seeded_malformed_sample", value)

    mismatches: list[dict[str, Any]] = []
    contract_mismatches: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    for case in cases:
        value = case["input"]
        try:
            canonical_result: Any = canonical(value)
        except Exception as exc:  # Canonical is the oracle, but preserve any unexpected behavior.
            canonical_result = {"exception": type(exc).__name__, "message": str(exc)}
        try:
            generated_result: Any = generated(value)
        except Exception as exc:
            generated_result = {"exception": type(exc).__name__, "message": str(exc)}
        contract_result = strict_ascii_contract(value)
        result = {
            **case,
            "canonical": canonical_result,
            "generated": generated_result,
            "strict_ascii_contract": contract_result,
        }
        results.append(result)
        if canonical_result != generated_result:
            mismatches.append(result)
        if generated_result != contract_result:
            contract_mismatches.append(result)

    scope = {
        "seed": 124,
        "case_count": len(cases),
        "explicit_case_count": len(explicit),
        "ascii_boundary_grid": {
            "years": ["0000", "2000", "9999"],
            "months": [0, 13],
            "days": [0, 32],
        },
        "seeded_malformed_requested": 1000,
        "canonical_generated_mismatch_count": len(mismatches),
        "generated_strict_contract_mismatch_count": len(contract_mismatches),
    }
    (EVIDENCE_DIR / "differential_inputs.json").write_text(
        json.dumps({"scope": scope, "cases": cases}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (EVIDENCE_DIR / "differential_results.json").write_text(
        json.dumps(
            {
                "scope": scope,
                "canonical_generated_mismatches": mismatches,
                "generated_strict_contract_mismatches": contract_mismatches,
                "all_results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(scope, ensure_ascii=False, sort_keys=True))
    print("canonical/generated mismatches:")
    for mismatch in mismatches:
        print(json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
    print("generated/strict-contract mismatches:")
    for mismatch in contract_mismatches:
        print(json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
