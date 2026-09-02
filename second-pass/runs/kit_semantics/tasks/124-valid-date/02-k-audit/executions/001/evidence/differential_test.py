#!/usr/bin/env python3
"""Independent contract/canonical/generated differential test for valid_date."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/fresh/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


canonical_valid_date = load_entry(CANONICAL_PATH, "trusted_canonical")
generated_valid_date = load_entry(GENERATED_PATH, "generated_solution")


def contract_oracle(date: str) -> bool:
    """Literal mm-dd-yyyy contract, with ASCII decimal digits."""
    if len(date) != 10 or date[2] != "-" or date[5] != "-":
        return False
    digit_positions = (0, 1, 3, 4, 6, 7, 8, 9)
    if any(not ("0" <= date[index] <= "9") for index in digit_positions):
        return False
    month = int(date[:2])
    day = int(date[3:5])
    month_limits = {
        1: 31,
        2: 29,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    return month in month_limits and 1 <= day <= month_limits[month]


documented_examples = [
    ("03-11-2000", True),
    ("15-01-2012", False),
    ("04-0-2040", False),
    ("06-04-2020", True),
    ("06/04/2020", False),
]

branch_boundaries = [
    "",
    "-",
    "03-11-200",
    "03-11-20000",
    "03/11/2000",
    "03-11/2000",
    "00-01-2000",
    "01-00-2000",
    "01-01-2000",
    "01-31-2000",
    "01-32-2000",
    "02-00-2000",
    "02-01-2000",
    "02-28-2000",
    "02-29-2000",
    "02-30-2000",
    "03-31-2000",
    "03-32-2000",
    "04-29-2000",
    "04-30-2000",
    "04-31-2000",
    "06-30-2000",
    "06-31-2000",
    "09-30-2000",
    "09-31-2000",
    "11-30-2000",
    "11-31-2000",
    "12-31-2000",
    "12-32-2000",
    "13-01-2000",
    "99-99-9999",
    "02-29-0000",
    "02-29-9999",
    "0a-11-2000",
    "03-b1-2000",
    "03-11-20c0",
    "０3-11-2000",
    "03-11-２０００",
]

# These are deliberately outside literal mm-dd-yyyy. They expose the trusted
# canonical implementation's permissive strip/int behavior without treating
# that behavior as the natural-language format contract.
canonical_extensions = [
    " 03-11-2000 ",
    "\t03-11-2000\n",
    "3-1-2000",
    "03-1-2000",
    "3-01-2000",
    "03-11-20",
    "03-11-+2000",
    "+3-11-2000",
    "03-+1-2000",
]

position_mutations = []
base = "03-11-2000"
for index in (0, 1, 3, 4, 6, 7, 8, 9):
    position_mutations.append(base[:index] + "x" + base[index + 1 :])
for index in (2, 5):
    position_mutations.append(base[:index] + "/" + base[index + 1 :])

formatted_grid = [
    f"{month:02d}-{day:02d}-{year}"
    for year in ("0000", "1999", "2000", "9999")
    for month in range(100)
    for day in range(100)
]

rng = random.Random(124)
alphabet = "0123456789-/+ xABC"
random_strings = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 16)))
    for _ in range(5000)
]

categories = {
    "documented_examples": [item[0] for item in documented_examples],
    "branch_boundaries": branch_boundaries,
    "position_mutations": position_mutations,
    "formatted_grid": formatted_grid,
    "canonical_extensions": canonical_extensions,
    "deterministic_random": random_strings,
}


def collect_mismatches():
    generated_vs_contract = []
    canonical_vs_contract = []
    generated_vs_canonical = []
    category_counts = {}
    tested = set()

    for category, cases in categories.items():
        category_counts[category] = len(cases)
        for date in cases:
            if date in tested:
                continue
            tested.add(date)
            expected = contract_oracle(date)
            generated = generated_valid_date(date)
            canonical = canonical_valid_date(date)
            if generated != expected:
                generated_vs_contract.append((date, generated, expected))
            if canonical != expected:
                canonical_vs_contract.append((date, canonical, expected))
            if generated != canonical:
                generated_vs_canonical.append((date, generated, canonical))

    example_failures = []
    for date, expected in documented_examples:
        actual = generated_valid_date(date)
        canonical = canonical_valid_date(date)
        if actual != expected or canonical != expected:
            example_failures.append((date, actual, canonical, expected))

    return (
        len(tested),
        category_counts,
        example_failures,
        generated_vs_contract,
        canonical_vs_contract,
        generated_vs_canonical,
    )


def main() -> None:
    (
        total,
        category_counts,
        example_failures,
        generated_vs_contract,
        canonical_vs_contract,
        generated_vs_canonical,
    ) = collect_mismatches()

    print(f"category_counts={category_counts}")
    print(f"unique_inputs={total}")
    print(f"documented_example_failures={len(example_failures)}")
    print(f"generated_vs_contract_mismatches={len(generated_vs_contract)}")
    print(f"canonical_vs_contract_mismatches={len(canonical_vs_contract)}")
    print(f"generated_vs_canonical_mismatches={len(generated_vs_canonical)}")
    print(f"generated_vs_contract_first={generated_vs_contract[:12]!r}")
    print(f"canonical_vs_contract_first={canonical_vs_contract[:12]!r}")
    print(f"generated_vs_canonical_first={generated_vs_canonical[:12]!r}")

    if example_failures or generated_vs_contract:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
