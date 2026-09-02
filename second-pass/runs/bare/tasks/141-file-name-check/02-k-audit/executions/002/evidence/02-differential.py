#!/usr/bin/env python3
"""Independent differential test for HumanEval 141.

The candidate implementation and trusted canonical implementation are loaded
from the clean scratch copy.  `prompt_oracle` is independently written from the
literal prompt contract: ASCII letters, ASCII digits, exactly one dot, and one
of the three exact suffixes.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


ROOT = Path("/tmp/audit-work/141-file-name-check")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


canonical = load_entry("trusted_canonical", ROOT / "canonical.py")
generated = load_entry("generated_solution", ROOT / "solution.py")


def prompt_oracle(name: str) -> str:
    if sum("0" <= char <= "9" for char in name) > 3:
        return "No"
    if name.count(".") != 1:
        return "No"
    stem, suffix = name.split(".")
    if not stem:
        return "No"
    if not (("a" <= stem[0] <= "z") or ("A" <= stem[0] <= "Z")):
        return "No"
    return "Yes" if suffix in {"txt", "exe", "dll"} else "No"


named_cases = [
    # Documented examples.
    "example.txt",
    "1example.dll",
    # Empty and dot-count boundaries.
    "",
    ".",
    ".txt",
    "a",
    "a.",
    "a.txt",
    "a..txt",
    "a.b.txt",
    # First-character ASCII boundaries and accepted suffixes.
    "A.exe",
    "Z.dll",
    "z.txt",
    "@.txt",
    "[.txt",
    "`.txt",
    "{.txt",
    # Digit-count boundaries.
    "a123.txt",
    "a1234.txt",
    "a0b1c2.dll",
    "a0b1c2d3.dll",
    # Suffix and case boundaries.
    "a.tx",
    "a.txtx",
    "a.TXT",
    "a.exe",
    "a.dll",
    # Unicode witnesses exposing canonical/source-contract differences.
    "é.txt",
    "Ω.exe",
    "a١٢٣٤.txt",
    "a１２３４.dll",
    "é١٢٣٤.txt",
    # Embedded NUL and non-BMP strings remain ordinary Python strings.
    "a\x00.txt",
    "a😀.dll",
]

alphabet = ("a", "A", "z", "Z", "0", "3", ".", "_", "é", "١")
generated_cases = (
    "".join(chars)
    for length in range(0, 5)
    for chars in itertools.product(alphabet, repeat=length)
)
suffix_cases = (
    stem + suffix
    for stem_length in range(0, 4)
    for chars in itertools.product(alphabet, repeat=stem_length)
    for stem in ("".join(chars),)
    for suffix in (".txt", ".exe", ".dll", ".TXT", ".txtx", "")
)

cases = list(dict.fromkeys(itertools.chain(named_cases, generated_cases, suffix_cases)))
generated_prompt_mismatches: list[tuple[str, str, str]] = []
generated_canonical_mismatches: list[tuple[str, str, str, str]] = []
canonical_prompt_mismatches: list[tuple[str, str, str]] = []

for value in cases:
    expected = prompt_oracle(value)
    got_generated = generated(value)
    got_canonical = canonical(value)
    if got_generated != expected:
        generated_prompt_mismatches.append((value, got_generated, expected))
    if got_generated != got_canonical:
        generated_canonical_mismatches.append(
            (value, got_generated, got_canonical, expected)
        )
    if got_canonical != expected:
        canonical_prompt_mismatches.append((value, got_canonical, expected))

print("case_count:", len(cases))
print("generated_vs_prompt_mismatch_count:", len(generated_prompt_mismatches))
print("generated_vs_canonical_mismatch_count:", len(generated_canonical_mismatches))
print("canonical_vs_prompt_mismatch_count:", len(canonical_prompt_mismatches))
print("generated_vs_canonical_samples:")
for row in generated_canonical_mismatches[:20]:
    print(repr(row))

if generated_prompt_mismatches:
    print("generated_vs_prompt_samples:")
    for row in generated_prompt_mismatches[:20]:
        print(repr(row))
    raise SystemExit(1)
