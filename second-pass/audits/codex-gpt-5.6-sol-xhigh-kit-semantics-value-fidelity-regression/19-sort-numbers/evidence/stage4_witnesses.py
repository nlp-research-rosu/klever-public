#!/usr/bin/env python3
"""Ground witnesses for the two K claim preconditions and result substitution."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def formal_sort_contract(source: str) -> str:
    """Ground interpretation of splitWS + rank-keyed stable sort + joinCodes."""
    tokens = source.split()
    output: list[str] = []
    for word in WORDS:
        output.extend(word for token in tokens if token == word)
    return " ".join(output)


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "trusted_canonical_witness")
    generated = load(
        Path("/tmp/audit-work/reconstruction/solution.py"),
        "generated_solution_witness",
    )

    helper_rows = []
    for expected_rank, word in enumerate(WORDS):
        actual_rank = generated._number_rank(word)
        helper_rows.append(
            {"CS": word, "expected_numberRank": expected_rank, "actual": actual_rank}
        )
        if actual_rank != expected_rank:
            print(json.dumps({"helper_mismatch": helper_rows[-1]}))
            return 1

    main_rows = []
    for source in (
        "",
        "three one five",
        "nine zero eight one",
        "  eight   two zero  ",
    ):
        formal = formal_sort_contract(source)
        canonical_result = canonical.sort_numbers(source)
        generated_result = generated.sort_numbers(source)
        row = {
            "CS": source,
            "validNumberInput": True,
            "formal_ground_result_under_sortKeyVS_contract": formal,
            "canonical": canonical_result,
            "generated": generated_result,
        }
        main_rows.append(row)
        if len({formal, canonical_result, generated_result}) != 1:
            print(json.dumps({"main_mismatch": row}))
            return 1

    print("HELPER_PRECONDITION_WITNESS=" + json.dumps(helper_rows[-1]))
    print(
        "MAIN_PRECONDITION_WITNESS="
        + json.dumps(next(row for row in main_rows if row["CS"] == "three one five"))
    )
    print("HELPER_GROUND_CASES=" + json.dumps(helper_rows))
    print("MAIN_GROUND_CASES=" + json.dumps(main_rows))
    print("MISMATCH_COUNT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
