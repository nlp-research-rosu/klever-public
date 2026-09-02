#!/usr/bin/env python3
"""Independent docstring-first differential for HumanEval task 134."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Callable


SCRATCH = Path("/tmp/audit-work/134-check-last-char")


def load_entry(path: Path, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


def docstring_oracle(txt: str) -> bool:
    """Literal reading: the last space-delimited group must be one letter."""
    final_group = txt.split(" ")[-1]
    return len(final_group) == 1 and final_group.isalpha()


documented = [
    ("apple pie", False),
    ("apple pi e", True),
    ("apple pi e ", False),
    ("", False),
]

branch_boundaries = [
    "",
    "a",
    "Z",
    "1",
    "!",
    " ",
    " a",
    "  a",
    "aa",
    "a ",
    "a  ",
    "a b",
    "a  b",
    "ab c",
    "ab cd",
    "\ta",
    "a\tb",
    "a\nb",
]

alphabet = (" ", "a", "Z", "1", "!", "\t")
generated = [
    "".join(chars)
    for length in range(0, 6)
    for chars in itertools.product(alphabet, repeat=length)
]

unicode_and_exotic = [
    "é",
    " É",
    "α",
    "x β",
    "βγ",
    "xβ",
    "中",
    "x 中",
    "🙂",
    "x 🙂",
    "İ",
    "x İ",
    "e\u0301",
    "x e\u0301",
]

all_inputs = list(
    dict.fromkeys(
        [value for value, _expected in documented]
        + branch_boundaries
        + generated
        + unicode_and_exotic
    )
)


def outcome(function: Callable[[str], bool], value: str) -> tuple[str, object]:
    try:
        return ("return", function(value))
    except Exception as error:  # noqa: BLE001 - differences in exceptions matter
        return ("exception", f"{type(error).__name__}: {error}")


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--inputs-only":
        json.dump(all_inputs, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    canonical = load_entry(SCRATCH / "canonical.py", "audit_trusted_canonical")
    candidate = load_entry(SCRATCH / "solution.py", "audit_candidate_solution")

    serialized = json.dumps(all_inputs, ensure_ascii=False, separators=(",", ":")).encode()
    print(f"input_count={len(all_inputs)}")
    print(f"input_corpus_sha256={hashlib.sha256(serialized).hexdigest()}")
    print(f"generated_exhaustive_lengths=0..5 alphabet={alphabet!r}")
    print(f"unicode_and_exotic_count={len(unicode_and_exotic)}")

    documented_failures: list[tuple[str, object, object]] = []
    for value, expected in documented:
        oracle_value = docstring_oracle(value)
        candidate_value = outcome(candidate, value)
        print(
            "DOCUMENTED "
            f"input={value!r} stated={expected!r} oracle={oracle_value!r} "
            f"candidate={candidate_value!r} canonical={outcome(canonical, value)!r}"
        )
        if oracle_value != expected or candidate_value != ("return", expected):
            documented_failures.append((value, expected, candidate_value))

    candidate_mismatches: list[tuple[str, object, object]] = []
    canonical_mismatches: list[tuple[str, object, object]] = []
    for value in all_inputs:
        expected = ("return", docstring_oracle(value))
        candidate_value = outcome(candidate, value)
        canonical_value = outcome(canonical, value)
        if candidate_value != expected:
            candidate_mismatches.append((value, expected, candidate_value))
        if canonical_value != expected:
            canonical_mismatches.append((value, expected, canonical_value))

    print(f"documented_failure_count={len(documented_failures)}")
    print(f"candidate_docstring_mismatch_count={len(candidate_mismatches)}")
    for mismatch in candidate_mismatches[:25]:
        print(f"CANDIDATE_MISMATCH {mismatch!r}")
    print(f"canonical_docstring_mismatch_count={len(canonical_mismatches)}")
    for mismatch in canonical_mismatches[:25]:
        print(f"CANONICAL_OBSERVATION {mismatch!r}")

    print("BRANCH_BOUNDARY_RESULTS")
    for value in branch_boundaries:
        print(
            f"input={value!r} oracle={docstring_oracle(value)!r} "
            f"candidate={outcome(candidate, value)!r} canonical={outcome(canonical, value)!r}"
        )

    print("UNICODE_AND_EXOTIC_RESULTS")
    for value in unicode_and_exotic:
        print(
            f"input={value!r} oracle={docstring_oracle(value)!r} "
            f"candidate={outcome(candidate, value)!r} canonical={outcome(canonical, value)!r}"
        )

    return 1 if documented_failures or candidate_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
