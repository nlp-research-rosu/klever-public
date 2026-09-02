#!/usr/bin/env python3
"""Independent differential test for HumanEval/80."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/80-is-happy")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


canonical = load_entry(SCRATCH / "trusted-canonical.py", "trusted_canonical")
generated = load_entry(SCRATCH / "solution.py", "generated_solution")


def contract_oracle(text: str) -> bool:
    return len(text) >= 3 and all(
        text[index] != text[index + 1]
        and text[index] != text[index + 2]
        and text[index + 1] != text[index + 2]
        for index in range(len(text) - 2)
    )


named_cases = {
    "empty": "",
    "length_one": "a",
    "length_two": "aa",
    "first_valid_length": "abc",
    "equal_0_1": "aab",
    "equal_0_2": "aba",
    "equal_1_2": "abb",
    "recursive_true": "abcd",
    "recursive_equal_0_2": "abcb",
    "recursive_equal_1_2": "abcc",
    "prompt_aabb": "aabb",
    "prompt_adb": "adb",
    "prompt_xyy": "xyy",
    "nul_character": "\x00ab",
    "non_ascii_distinct": "😀éa",
    "non_ascii_repeat": "😀a😀",
    "combining_code_point": "e\u0301e",
}

checked = 0
mismatches: list[tuple[str, bool, bool, bool]] = []


def check(text: str) -> None:
    global checked
    expected = contract_oracle(text)
    canonical_value = canonical(text)
    generated_value = generated(text)
    checked += 1
    if canonical_value != expected or generated_value != expected:
        mismatches.append((text, expected, canonical_value, generated_value))


print("Named boundary and branch cases:")
for name, text in named_cases.items():
    check(text)
    print(
        f"  {name}: input={text!r} "
        f"oracle={contract_oracle(text)} "
        f"canonical={canonical(text)} generated={generated(text)}"
    )

for size in range(9):
    for letters in itertools.product("abc", repeat=size):
        check("".join(letters))

rng = random.Random(0x80)
alphabet = ["a", "b", "c", "é", "😀", "\x00", "\u0301"]
for _ in range(3000):
    check("".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 81))))

print(f"total_cases={checked}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    raise SystemExit(1)
