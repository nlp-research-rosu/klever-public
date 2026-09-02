#!/usr/bin/env python3
"""Independent differential tests for HumanEval 141.

The trusted canonical and submitted solution are imported from paths supplied
on the command line.  The prompt-level oracle is independently implemented
from the English contract so that canonical/prompt disagreements are visible.
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


def prompt_oracle(file_name: str) -> str:
    if file_name.count(".") != 1:
        return "No"
    stem, suffix = file_name.split(".")
    if suffix not in {"txt", "exe", "dll"}:
        return "No"
    if not stem or not (("a" <= stem[0] <= "z") or ("A" <= stem[0] <= "Z")):
        return "No"
    if sum(ch in "0123456789" for ch in file_name) > 3:
        return "No"
    return "Yes"


def build_cases() -> list[str]:
    explicit = [
        # Documented examples and emptiness.
        "example.txt",
        "1example.dll",
        "",
        # Dot-count boundaries.
        "a",
        "a.",
        ".txt",
        "a.txt",
        "a..txt",
        "a.b.txt",
        # Accepted/rejected suffix boundaries.
        "a.exe",
        "A.dll",
        "a.tx",
        "a.txtx",
        "a.TXT",
        "a.py",
        # ASCII digit-count boundary 0, 3, 4, including suffix-adjacent.
        "a0.txt",
        "a1b2c3.exe",
        "a1b2c3d4.exe",
        "Z999.dll",
        "Z9999.dll",
        # Initial-character boundaries around ASCII letter ranges.
        "@.txt",
        "A.txt",
        "Z.txt",
        "[.txt",
        "`.txt",
        "a.txt",
        "z.txt",
        "{.txt",
        # Unicode probes exposing the prompt/canonical semantic difference.
        "é.txt",
        "Ω.exe",
        "中.dll",
        "A١٢٣.txt",
        "A١٢٣٤.txt",
        "é١٢٣٤.txt",
        # Miscellaneous string boundaries.
        "a\x00.txt",
        "a txt",
        "\n.txt",
        "a...dll",
    ]

    generated: list[str] = []
    starts = ["", "A", "z", "1", "_", "é"]
    middles = ["", "b", "0", "123", "1234", "١٢٣٤", ".", "x.y"]
    endings = [".txt", ".exe", ".dll", ".py", "", "..txt"]
    for start, middle, ending in itertools.product(starts, middles, endings):
        generated.append(start + middle + ending)

    # Deduplicate while preserving deterministic order.
    return list(dict.fromkeys(explicit + generated))


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: differential_test.py CANONICAL.py SOLUTION.py")
    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    solution = load_entry(Path(sys.argv[2]), "submitted_solution")
    cases = build_cases()

    canonical_mismatches: list[tuple[str, str, str]] = []
    prompt_mismatches: list[tuple[str, str, str]] = []
    print(f"CASE_COUNT={len(cases)}")
    for index, value in enumerate(cases):
        expected_canonical = canonical(value)
        expected_prompt = prompt_oracle(value)
        actual = solution(value)
        if actual != expected_canonical:
            canonical_mismatches.append((value, expected_canonical, actual))
        if actual != expected_prompt:
            prompt_mismatches.append((value, expected_prompt, actual))
        print(
            f"CASE {index:03d} input={value!r} "
            f"canonical={expected_canonical!r} prompt={expected_prompt!r} "
            f"solution={actual!r}"
        )

    print(f"CANONICAL_MISMATCH_COUNT={len(canonical_mismatches)}")
    for value, expected, actual in canonical_mismatches:
        print(
            f"CANONICAL_MISMATCH input={value!r} "
            f"expected={expected!r} actual={actual!r}"
        )
    print(f"PROMPT_MISMATCH_COUNT={len(prompt_mismatches)}")
    for value, expected, actual in prompt_mismatches:
        print(
            f"PROMPT_MISMATCH input={value!r} "
            f"expected={expected!r} actual={actual!r}"
        )

    # Prompt conformance is the executable pass/fail gate. Canonical
    # disagreements remain in the evidence and are judged in the review.
    return 0 if not prompt_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
