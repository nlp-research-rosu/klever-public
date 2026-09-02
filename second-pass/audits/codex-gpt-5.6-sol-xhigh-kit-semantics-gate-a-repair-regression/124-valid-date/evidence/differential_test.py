#!/usr/bin/env python3
"""Independent canonical/generated/prompt-contract differential audit."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import re
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def prompt_contract(value: str) -> bool:
    """Literal mm-dd-yyyy reading of the natural-language contract."""
    match = re.fullmatch(r"([0-9]{2})-([0-9]{2})-([0-9]{4})", value)
    if match is None:
        return False
    month = int(match.group(1))
    day = int(match.group(2))
    if not 1 <= month <= 12 or day < 1:
        return False
    upper = 29 if month == 2 else 30 if month in (4, 6, 9, 11) else 31
    return day <= upper


def generate_cases() -> tuple[list[str], dict[str, int]]:
    cases: list[str] = []
    sections: dict[str, int] = {}

    def add(section: str, values):
        before = len(cases)
        cases.extend(values)
        sections[section] = len(cases) - before

    add(
        "documented_examples",
        (
            "03-11-2000",
            "15-01-2012",
            "04-0-2040",
            "06-04-2020",
            "06/04/2020",
        ),
    )
    add(
        "empty_and_branch_boundaries",
        (
            "",
            "-",
            "0",
            "00-00-000",
            "00-00-0000",
            "01-01-0000",
            "12-31-9999",
            "13-01-2000",
            "01-00-2000",
            "02-28-2000",
            "02-29-2000",
            "02-30-2000",
            "04-30-2000",
            "04-31-2000",
            "01-31-2000",
            "01-32-2000",
            "03/11-2000",
            "03-11/2000",
            "03-11-200a",
            "a3-11-2000",
            "03-a1-2000",
        ),
    )
    add(
        "canonical_format_sensitivity",
        (
            "3-11-2000",
            "03-1-2000",
            "03-11-20",
            "03-11-20000",
            " 03-11-2000",
            "03-11-2000 ",
            " 03-11-2000 ",
            "03-11-+200",
            "03-11- 2000",
            "０３-１１-２０００",
            "٠٣-١١-٢٠٠٠",
            "03-11-²000",
        ),
    )
    add(
        "calendar_grid",
        (
            f"{month:02d}-{day:02d}-{year}"
            for month in range(0, 14)
            for day in range(0, 34)
            for year in ("0000", "2000", "9999")
        ),
    )
    near_digit = ("/", "0", "9", ":", "a", "０", "٠")
    digit_positions = (0, 1, 3, 4, 6, 7, 8, 9)
    digit_mutants = []
    baseline = list("03-11-2000")
    for position in digit_positions:
        for char in near_digit:
            mutant = baseline.copy()
            mutant[position] = char
            digit_mutants.append("".join(mutant))
    add("every_digit_guard_boundary", digit_mutants)

    separator_mutants = []
    for position in (2, 5):
        for char in (",", "-", ".", "/", "—"):
            mutant = baseline.copy()
            mutant[position] = char
            separator_mutants.append("".join(mutant))
    add("separator_guard_boundaries", separator_mutants)

    rng = random.Random(124_2026_07_23)
    alphabet = "0123456789-/+ abcXYZ０١"
    random_cases = []
    for _ in range(3000):
        length = rng.randrange(0, 15)
        random_cases.append("".join(rng.choice(alphabet) for _ in range(length)))
    add("deterministic_generated_strings", random_cases)

    unique = list(dict.fromkeys(cases))
    sections["duplicates_removed"] = len(cases) - len(unique)
    sections["unique_total"] = len(unique)
    return unique, sections


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--cases-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry("audit_canonical", args.canonical)
    generated = load_entry("audit_generated", args.generated)
    cases, sections = generate_cases()

    canonical_mismatches = []
    prompt_mismatches = []
    args.cases_out.parent.mkdir(parents=True, exist_ok=True)
    with args.cases_out.open("w", encoding="utf-8") as stream:
        for index, value in enumerate(cases):
            canonical_result = canonical(value)
            generated_result = generated(value)
            prompt_result = prompt_contract(value)
            record = {
                "index": index,
                "input": value,
                "canonical": canonical_result,
                "generated": generated_result,
                "prompt_contract": prompt_result,
            }
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            if canonical_result != generated_result:
                canonical_mismatches.append(record)
            if prompt_result != generated_result:
                prompt_mismatches.append(record)

    print("sections=" + json.dumps(sections, sort_keys=True))
    print(f"tested={len(cases)}")
    print(f"canonical_generated_mismatches={len(canonical_mismatches)}")
    print(f"prompt_generated_mismatches={len(prompt_mismatches)}")
    print("canonical_generated_mismatch_examples")
    for record in canonical_mismatches[:40]:
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    print("prompt_generated_mismatch_examples")
    for record in prompt_mismatches[:40]:
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))

    # A canonical divergence is deliberately a nonzero audit signal. The
    # separate prompt mismatch count lets the review judge a reference/contract
    # conflict instead of silently treating either oracle as authoritative.
    return 1 if canonical_mismatches or prompt_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
