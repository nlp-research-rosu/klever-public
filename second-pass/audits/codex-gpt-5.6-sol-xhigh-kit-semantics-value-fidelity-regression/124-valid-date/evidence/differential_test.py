#!/usr/bin/env python3
"""Independent differential audit of trusted canonical vs generated solution."""

from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path
import random
import re
from typing import Callable


EXPLICIT_PATH = Path("/audit-output/evidence/differential_cases.json")
INPUTS_PATH = Path("/audit-output/evidence/04-differential-inputs.jsonl")
RESULTS_PATH = Path("/audit-output/evidence/04-differential-results.json")
CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/124-valid-date/solution.py")


def load_function(path: Path, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


STRICT_DATE = re.compile(r"[0-9]{2}-[0-9]{2}-[0-9]{4}\Z")


def prompt_oracle(value: str) -> bool:
    """Direct strict reading of the prompt's mm-dd-yyyy contract."""
    if STRICT_DATE.fullmatch(value) is None:
        return False
    month = int(value[0:2])
    day = int(value[3:5])
    if not 1 <= month <= 12 or day < 1:
        return False
    if month == 2:
        cap = 29
    elif month in {4, 6, 9, 11}:
        cap = 30
    else:
        cap = 31
    return day <= cap


def observed(function: Callable[[str], bool], value: str) -> dict[str, object]:
    try:
        return {"kind": "return", "value": function(value)}
    except BaseException as error:  # Deliberately records all observable failures.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def add_case(
    cases: dict[str, set[str]], category: str, value: str
) -> None:
    cases.setdefault(category, set()).add(value)


def construct_cases() -> list[tuple[str, str]]:
    cases: dict[str, set[str]] = {}
    explicit = json.loads(EXPLICIT_PATH.read_text(encoding="utf-8"))
    for category, values in explicit.items():
        for value in values:
            add_case(cases, category, value)

    # Exhaust the two parsed fields while keeping exact strict format.
    for year in ("0000", "2000", "9999"):
        for month in range(100):
            for day in range(100):
                add_case(
                    cases,
                    f"exhaustive_fields_year_{year}",
                    f"{month:02d}-{day:02d}-{year}",
                )

    # Independently perturb each format/digit position around both comparisons.
    base = "03-11-2000"
    for position in range(len(base)):
        for replacement in ("/", "0", "9", ":", "A", "é", "٠", "０"):
            value = base[:position] + replacement + base[position + 1 :]
            add_case(cases, f"position_{position}_mutations", value)

    # Deterministic representative strings across the broader string domain.
    rng = random.Random(124_20260723)
    alphabet = "0123456789-/+: AaZzé٠９"
    for _ in range(5000):
        length = rng.randrange(0, 16)
        value = "".join(rng.choice(alphabet) for _ in range(length))
        add_case(cases, "deterministic_generated_strings", value)

    flattened: list[tuple[str, str]] = []
    seen: set[str] = set()
    for category in sorted(cases):
        for value in sorted(cases[category]):
            if value not in seen:
                flattened.append((category, value))
                seen.add(value)
    return flattened


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical_124")
    generated = load_function(GENERATED_PATH, "generated_solution_124")
    cases = construct_cases()

    category_counts: Counter[str] = Counter()
    canonical_mismatches: list[dict[str, object]] = []
    prompt_mismatches: list[dict[str, object]] = []
    records: list[str] = []
    for index, (category, value) in enumerate(cases):
        category_counts[category] += 1
        canonical_result = observed(canonical, value)
        generated_result = observed(generated, value)
        oracle_result = {"kind": "return", "value": prompt_oracle(value)}
        record = {
            "index": index,
            "category": category,
            "input": value,
            "canonical": canonical_result,
            "generated": generated_result,
            "prompt_oracle": oracle_result,
        }
        records.append(json.dumps(record, ensure_ascii=True, sort_keys=True))
        if generated_result != canonical_result:
            canonical_mismatches.append(record)
        if generated_result != oracle_result:
            prompt_mismatches.append(record)

    INPUTS_PATH.write_text("\n".join(records) + "\n", encoding="utf-8")
    report = {
        "canonical_path": str(CANONICAL_PATH),
        "generated_path": str(GENERATED_PATH),
        "explicit_inputs_path": str(EXPLICIT_PATH),
        "complete_inputs_and_outputs_path": str(INPUTS_PATH),
        "total_unique_inputs": len(cases),
        "category_counts": dict(sorted(category_counts.items())),
        "generated_vs_canonical_mismatch_count": len(canonical_mismatches),
        "generated_vs_prompt_oracle_mismatch_count": len(prompt_mismatches),
        "canonical_mismatch_examples": canonical_mismatches[:100],
        "prompt_mismatch_examples": prompt_mismatches[:100],
    }
    RESULTS_PATH.write_text(
        json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"total_unique_inputs={len(cases)}")
    print(
        "generated_vs_canonical_mismatches="
        f"{len(canonical_mismatches)}"
    )
    print(
        "generated_vs_prompt_oracle_mismatches="
        f"{len(prompt_mismatches)}"
    )
    print(f"results={RESULTS_PATH}")
    for record in canonical_mismatches[:25]:
        print(
            "CANONICAL_MISMATCH "
            f"input={record['input']!r} "
            f"canonical={record['canonical']} "
            f"generated={record['generated']} "
            f"prompt_oracle={record['prompt_oracle']}"
        )
    for record in prompt_mismatches[:25]:
        print(
            "PROMPT_MISMATCH "
            f"input={record['input']!r} "
            f"generated={record['generated']} "
            f"prompt_oracle={record['prompt_oracle']}"
        )
    return 1 if prompt_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
