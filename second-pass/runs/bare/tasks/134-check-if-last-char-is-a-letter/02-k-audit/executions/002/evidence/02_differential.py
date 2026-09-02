#!/usr/bin/env python3
"""Independent differential test of trusted canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


canonical = load_function(
    Path("/reference/canonical.py"), "trusted_canonical_check_last"
)
submitted = load_function(
    Path("/tmp/audit-work/task134/solution.py"), "submitted_check_last"
)

named_cases = [
    ("example_false_word", "apple pie"),
    ("example_true_standalone", "apple pi e"),
    ("example_trailing_space", "apple pi e "),
    ("example_empty", ""),
    ("length_one_ascii_upper", "A"),
    ("length_one_ascii_lower", "z"),
    ("length_one_digit", "7"),
    ("length_one_punctuation", "!"),
    ("length_one_unicode_letter", "é"),
    ("length_one_greek_letter", "λ"),
    ("length_one_cjk_letter", "界"),
    ("length_one_combining_mark", "\u0301"),
    ("length_two_word", "ab"),
    ("length_two_standalone", " a"),
    ("length_two_space", "  "),
    ("previous_space_ascii_letter", "x Z"),
    ("previous_space_digit", "x 7"),
    ("previous_nonspace_letter", "xZ"),
    ("previous_space_unicode_letter", "x é"),
    ("previous_tab_ascii_letter", "x\tZ"),
    ("multiple_spaces_ascii_letter", "x  Z"),
    ("newline_before_ascii_letter", "x\nZ"),
]

alphabet = ["", " ", "a", "Z", "0", "!", "é", "λ", "界", "\t"]
generated = sorted(
    {
        "".join(chars)
        for size in range(0, 5)
        for chars in itertools.product(alphabet[1:], repeat=size)
    }
)

print("ORACLE=/reference/canonical.py::check_if_last_char_is_a_letter")
print("SUBMITTED=/tmp/audit-work/task134/solution.py::check_if_last_char_is_a_letter")
print("GENERATED_SCOPE=all strings of lengths 0..4 over repr alphabet below")
print(f"ALPHABET={alphabet!r}")
print(f"GENERATED_COUNT={len(generated)}")

mismatches: list[tuple[str, bool, bool]] = []
print("NAMED_CASE_RESULTS")
for label, text in named_cases:
    expected = canonical(text)
    actual = submitted(text)
    print(f"{label}\t{text!r}\tcanonical={expected!r}\tsubmitted={actual!r}")
    if expected != actual:
        mismatches.append((text, expected, actual))

for text in generated:
    expected = canonical(text)
    actual = submitted(text)
    if expected != actual:
        mismatches.append((text, expected, actual))

unique_mismatches = list(dict.fromkeys(mismatches))
print(f"MISMATCH_COUNT={len(unique_mismatches)}")
for text, expected, actual in unique_mismatches[:80]:
    print(f"MISMATCH\t{text!r}\tcanonical={expected!r}\tsubmitted={actual!r}")
if len(unique_mismatches) > 80:
    print(f"MISMATCHES_OMITTED={len(unique_mismatches) - 80}")

raise SystemExit(1 if unique_mismatches else 0)
