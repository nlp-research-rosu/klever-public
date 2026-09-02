#!/usr/bin/env python3
"""Independent differential test for HumanEval 141.

The explicit prompt contract is checked separately from the trusted canonical
implementation because canonical.py uses Unicode-aware str.isalpha() despite
the prompt's narrower A-Z/a-z requirement.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)


def prompt_contract(file_name: str) -> str:
    """Direct transcription of the natural-language contract."""
    if file_name.count(".") != 1:
        return "No"
    prefix, extension = file_name.split(".")
    if not prefix:
        return "No"
    if prefix[0] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return "No"
    if extension not in {"txt", "exe", "dll"}:
        return "No"
    if sum(character in "0123456789" for character in file_name) > 3:
        return "No"
    return "Yes"


documented = {
    "example.txt": "Yes",
    "1example.dll": "No",
}

boundaries = {
    "": "No",                 # empty
    ".": "No",                # one dot, invalid initial and extension
    ".txt": "No",             # empty prefix
    "a": "No",                # zero dots
    "a.": "No",               # empty extension
    "a.b.txt": "No",          # two dots
    "1.txt": "No",            # digit initial
    "_a.txt": "No",           # punctuation initial
    "a.pdf": "No",            # unsupported extension
    "a.tx": "No",             # short extension
    "a.atxt": "No",           # misleading tail
    "a.txtx": "No",           # trailing character
    "a.TXT": "No",            # case-sensitive extension
    "a.txt": "Yes",           # first allowed extension
    "a.exe": "Yes",           # second allowed extension
    "a.dll": "Yes",           # third allowed extension
    "A0b1c2.txt": "Yes",      # exactly three digits
    "A0b1c23.txt": "No",      # exactly four digits
    "aé中🙂.exe": "Yes",       # Unicode away from first position
    "é.txt": "No",            # prompt says Latin; canonical uses isalpha()
    "中.dll": "No",           # second canonical/contract boundary
}

for case, expected in documented.items() | boundaries.items():
    actual = generated(case)
    contract = prompt_contract(case)
    assert actual == expected, (case, actual, expected)
    assert contract == expected, (case, contract, expected)

small_alphabet = "aZ09.txedl?é中"
exhaustive = (
    "".join(chars)
    for length in range(6)
    for chars in itertools.product(small_alphabet, repeat=length)
)
rng = random.Random(14120260729)
sample_alphabet = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789._-? é中🙂"
)
random_cases = (
    "".join(rng.choice(sample_alphabet) for _ in range(rng.randrange(25)))
    for _ in range(20_000)
)

cases = set(documented) | set(boundaries)
cases.update(exhaustive)
cases.update(random_cases)

generated_contract_mismatches = []
canonical_generated_mismatches = []
canonical_contract_mismatches = []
for case in sorted(cases):
    generated_result = generated(case)
    canonical_result = canonical(case)
    contract_result = prompt_contract(case)
    if generated_result != contract_result:
        generated_contract_mismatches.append(
            (case, generated_result, contract_result)
        )
    if canonical_result != generated_result:
        canonical_generated_mismatches.append(
            (case, canonical_result, generated_result)
        )
    if canonical_result != contract_result:
        canonical_contract_mismatches.append(
            (case, canonical_result, contract_result)
        )

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"total_unique_cases={len(cases)}")
print(
    "generated_vs_prompt_contract_mismatches="
    f"{len(generated_contract_mismatches)}"
)
print(
    "canonical_vs_generated_mismatches="
    f"{len(canonical_generated_mismatches)}"
)
print(
    "canonical_vs_prompt_contract_mismatches="
    f"{len(canonical_contract_mismatches)}"
)
print(
    "canonical_generated_examples="
    f"{canonical_generated_mismatches[:10]!r}"
)
assert not generated_contract_mismatches
assert canonical_generated_mismatches == canonical_contract_mismatches
print("DIFFERENTIAL_PROMPT_CONTRACT=PASS")
print("CANONICAL_DIVERGENCE_CLASS=non-Latin alphabetic initial")
