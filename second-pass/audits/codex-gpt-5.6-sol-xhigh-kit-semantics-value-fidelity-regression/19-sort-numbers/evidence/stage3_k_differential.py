#!/usr/bin/env python3
"""Generate and run a bounded independent LLVM/K differential assertion batch."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
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


def counting_oracle(source: str) -> str:
    tokens = source.split()
    ordered: list[str] = []
    for word in WORDS:
        ordered.extend([word] * tokens.count(word))
    return " ".join(ordered)


def cases() -> list[str]:
    result = [
        " ".join(items)
        for length in range(3)
        for items in itertools.product(WORDS, repeat=length)
    ]
    result.extend(
        [
            "three one five",
            " ".join(WORDS),
            " ".join(reversed(WORDS)),
            "nine nine zero zero five five one",
            "  eight   two zero  ",
            "three\tone\nfive",
        ]
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    arguments = parser.parse_args()
    test_cases = cases()
    arguments.inputs_out.write_text(
        json.dumps(
            [
                {"input": source, "expected": counting_oracle(source)}
                for source in test_cases
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    source = (arguments.root / "solution.py").read_text(encoding="utf-8")
    assertions = "".join(
        f"\nassert sort_numbers({case!r}) == {counting_oracle(case)!r}\n"
        for case in test_cases
    )
    smoke_python = arguments.root / "audit-k-differential.py"
    smoke_mpy = arguments.root / "audit-k-differential.mpy"
    smoke_python.write_text(source + assertions, encoding="utf-8")
    with smoke_mpy.open("w", encoding="utf-8") as output:
        translated = subprocess.run(
            [
                "python3",
                "/reference/py2mpy.py",
                str(smoke_python),
            ],
            check=False,
            text=True,
            stdout=output,
        )
    if translated.returncode != 0:
        print(f"TRANSLATOR_EXIT={translated.returncode}")
        return translated.returncode
    completed = subprocess.run(
        [
            "krun",
            str(smoke_mpy),
            "--definition",
            str(arguments.root / "runtime-kompiled"),
            "--output",
            "none",
        ],
        check=False,
    )
    print("ORACLE=independent_counting_by_fixed_zero_through_nine_order")
    print(f"K_CASE_COUNT={len(test_cases)}")
    print(f"KRUN_EXIT={completed.returncode}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
