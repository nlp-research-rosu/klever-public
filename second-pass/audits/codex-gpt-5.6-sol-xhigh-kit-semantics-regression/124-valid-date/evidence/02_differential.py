#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval 124."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def prompt_oracle(value: str) -> bool:
    """Literal mm-dd-yyyy reading: fixed width, ASCII decimal digits."""
    if len(value) != 10 or value[2] != "-" or value[5] != "-":
        return False
    digit_positions = (0, 1, 3, 4, 6, 7, 8, 9)
    if any(value[index] not in "0123456789" for index in digit_positions):
        return False
    month = int(value[0:2])
    day = int(value[3:5])
    if not (1 <= month <= 12 and day >= 1):
        return False
    if month == 2:
        return day <= 29
    if month in (4, 6, 9, 11):
        return day <= 30
    return day <= 31


def add_case(
    cases: dict[str, dict[str, str]], category: str, label: str, value: str
) -> None:
    cases.setdefault(category, {})[label] = value


def build_cases() -> dict[str, dict[str, str]]:
    cases: dict[str, dict[str, str]] = {}

    documented = (
        ("example-valid-march", "03-11-2000"),
        ("example-invalid-month", "15-01-2012"),
        ("example-short-day", "04-0-2040"),
        ("example-valid-june", "06-04-2020"),
        ("example-bad-separator", "06/04/2020"),
    )
    for label, value in documented:
        add_case(cases, "documented_examples", label, value)

    for label, value in (
        ("empty", ""),
        ("one-separator", "-"),
        ("all-zero", "00-00-0000"),
        ("month-00", "00-01-2000"),
        ("month-01", "01-01-2000"),
        ("month-12", "12-31-2000"),
        ("month-13", "13-01-2000"),
        ("feb-00", "02-00-2000"),
        ("feb-01", "02-01-2000"),
        ("feb-29", "02-29-2000"),
        ("feb-30", "02-30-2000"),
        ("apr-30", "04-30-2000"),
        ("apr-31", "04-31-2000"),
        ("jan-31", "01-31-2000"),
        ("jan-32", "01-32-2000"),
        ("year-0000", "01-01-0000"),
        ("year-9999", "01-01-9999"),
        ("nine-chars", "01-01-000"),
        ("eleven-chars", "001-01-2000"),
    ):
        add_case(cases, "empty_and_boundaries", label, value)

    valid = "12-31-2000"
    for index in (0, 1, 3, 4, 6, 7, 8, 9):
        add_case(cases, "character_perturbations", f"letter-at-{index}", valid[:index] + "x" + valid[index + 1 :])
        add_case(cases, "character_perturbations", f"space-at-{index}", valid[:index] + " " + valid[index + 1 :])
    for index in (2, 5):
        add_case(cases, "character_perturbations", f"slash-at-{index}", valid[:index] + "/" + valid[index + 1 :])

    for label, value in (
        ("leading-space", " 03-11-2000"),
        ("trailing-space", "03-11-2000 "),
        ("both-spaces", " 03-11-2000 "),
        ("leading-tab", "\t03-11-2000"),
        ("short-month", "3-11-2000"),
        ("short-day", "03-1-2000"),
        ("short-year", "03-11-20"),
        ("long-year", "03-11-02000"),
        ("signed-month", "+3-11-2000"),
        ("signed-year", "03-11-+123"),
        ("arabic-indic", "٠٣-١١-٢٠٠٠"),
        ("newline-wrapped", "\n03-11-2000\n"),
    ):
        add_case(cases, "canonical_permissiveness", label, value)

    for year in ("0000", "2000", "9999"):
        for month in range(100):
            for day in range(100):
                value = f"{month:02d}-{day:02d}-{year}"
                add_case(
                    cases,
                    "generated_strict_ascii",
                    f"m{month:02d}-d{day:02d}-y{year}",
                    value,
                )

    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--canonical",
        type=Path,
        default=Path("/tmp/audit-work/124-valid-date/trusted/canonical.py"),
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path("/tmp/audit-work/124-valid-date/solution.py"),
    )
    parser.add_argument("--write-inputs", type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical_124")
    candidate = load_entry(args.candidate, "candidate_solution_124")
    cases = build_cases()
    if args.write_inputs is not None:
        args.write_inputs.write_text(
            json.dumps(cases, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )

    total = 0
    canonical_candidate_mismatches: list[tuple[str, str, str, bool, bool]] = []
    candidate_prompt_mismatches: list[tuple[str, str, str, bool, bool]] = []
    category_counts: dict[str, dict[str, int]] = {}
    digest = hashlib.sha256()

    for category, entries in cases.items():
        cc_count = 0
        cp_count = 0
        for label, value in entries.items():
            total += 1
            canonical_result = canonical(value)
            candidate_result = candidate(value)
            prompt_result = prompt_oracle(value)
            digest.update(
                json.dumps(
                    [category, label, value, canonical_result, candidate_result, prompt_result],
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode()
            )
            if canonical_result != candidate_result:
                cc_count += 1
                canonical_candidate_mismatches.append(
                    (category, label, value, canonical_result, candidate_result)
                )
            if candidate_result != prompt_result:
                cp_count += 1
                candidate_prompt_mismatches.append(
                    (category, label, value, candidate_result, prompt_result)
                )
        category_counts[category] = {
            "cases": len(entries),
            "canonical_candidate_mismatches": cc_count,
            "candidate_prompt_mismatches": cp_count,
        }

    print(f"canonical={args.canonical}")
    print(f"candidate={args.candidate}")
    print(f"total_cases={total}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"canonical_candidate_mismatches={len(canonical_candidate_mismatches)}")
    for mismatch in canonical_candidate_mismatches[:40]:
        print(f"CANONICAL_CANDIDATE_MISMATCH={mismatch!r}")
    if len(canonical_candidate_mismatches) > 40:
        print(
            "CANONICAL_CANDIDATE_MISMATCH_OMITTED="
            f"{len(canonical_candidate_mismatches) - 40}"
        )
    print(f"candidate_prompt_mismatches={len(candidate_prompt_mismatches)}")
    for mismatch in candidate_prompt_mismatches[:40]:
        print(f"CANDIDATE_PROMPT_MISMATCH={mismatch!r}")
    if len(candidate_prompt_mismatches) > 40:
        print(
            f"CANDIDATE_PROMPT_MISMATCH_OMITTED={len(candidate_prompt_mismatches) - 40}"
        )
    print(f"result_digest_sha256={digest.hexdigest()}")

    # Canonical divergence is deliberately reported, not treated as a script error.
    return 0 if not candidate_prompt_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
