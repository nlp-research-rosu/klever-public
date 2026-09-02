#!/usr/bin/env python3
"""Independent Python differential test for HumanEval/64."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
import random
from typing import Callable


WORK = Path("/tmp/audit-work/64-vowels-count")
EXPLICIT = Path("/audit-output/evidence/differential-explicit-inputs.json")


def load_entry(path: Path, module_name: str) -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


def independently_stated_contract(value: str) -> int:
    ordinary = sum(character in "aeiouAEIOU" for character in value)
    final_y = int(bool(value) and value[-1] in "yY")
    return ordinary + final_y


canonical = load_entry(WORK / "trusted-canonical.py", "trusted_canonical")
generated = load_entry(WORK / "solution.py", "generated_solution")

explicit = json.loads(EXPLICIT.read_text(encoding="utf-8"))
alphabet = tuple("aeiouAEIOUyYbcZ0é🙂")
exhaustive_nonempty = [
    "".join(items)
    for length in range(1, 5)
    for items in itertools.product(alphabet, repeat=length)
]
random_source = random.Random(640026)
random_alphabet = tuple("aeiouAEIOUyYbcdfgXYZ09 -_'éΩ🙂\n\t")
generated_random = [
    "".join(
        random_source.choice(random_alphabet)
        for _ in range(random_source.randint(1, 40))
    )
    for _ in range(3000)
]

all_cases = list(dict.fromkeys(explicit + exhaustive_nonempty + generated_random))
nonempty_cases = [value for value in all_cases if value]

canonical_mismatches: list[tuple[str, object, object]] = []
contract_mismatches: list[tuple[str, object, object]] = []
for value in nonempty_cases:
    canonical_result = canonical(value)
    generated_result = generated(value)
    contract_result = independently_stated_contract(value)
    if generated_result != canonical_result:
        canonical_mismatches.append((value, generated_result, canonical_result))
    if generated_result != contract_result:
        contract_mismatches.append((value, generated_result, contract_result))

empty_observations: dict[str, object] = {}
for label, implementation in (
    ("canonical", canonical),
    ("generated", generated),
    ("independent_contract", independently_stated_contract),
):
    try:
        empty_observations[label] = {"return": implementation("")}
    except Exception as error:  # Evidence records exact exception type and message.
        empty_observations[label] = {
            "exception": type(error).__name__,
            "message": str(error),
        }

print(f"explicit_case_count={len(explicit)}")
print(f"exhaustive_alphabet={''.join(alphabet)!r}")
print("exhaustive_lengths=1..4")
print(f"exhaustive_nonempty_count={len(exhaustive_nonempty)}")
print("random_seed=640026")
print("random_lengths=1..40")
print(f"random_case_count={len(generated_random)}")
print(f"unique_nonempty_case_count={len(nonempty_cases)}")
print(f"canonical_mismatch_count={len(canonical_mismatches)}")
print(f"contract_mismatch_count={len(contract_mismatches)}")
print(f"empty_observations={json.dumps(empty_observations, sort_keys=True)}")
print(f"canonical_mismatches_sample={canonical_mismatches[:10]!r}")
print(f"contract_mismatches_sample={contract_mismatches[:10]!r}")

assert canonical_mismatches == []
assert contract_mismatches == []
assert empty_observations["canonical"]["exception"] == "IndexError"
assert empty_observations["generated"] == {"return": 0}
assert empty_observations["independent_contract"] == {"return": 0}
print("DIFFERENTIAL_TEST_OK")
