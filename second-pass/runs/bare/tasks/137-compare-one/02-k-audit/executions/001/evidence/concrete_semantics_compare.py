#!/usr/bin/env python3
"""Compare fresh K concrete executions with independent Python executions."""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Case:
    label: str
    a: object
    b: object
    k_a: str
    k_b: str
    domain: str = "valid"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def python_outcome(fn, a, b):
    try:
        return ("return", fn(a, b))
    except Exception as exc:
        return ("raise", type(exc).__name__)


def compact(term: str) -> str:
    return re.sub(r"\s+", "", term)


def expected_term(outcome, a, b, k_a, k_b):
    if outcome[0] == "raise":
        return f"RAISE:{outcome[1]}"
    value = outcome[1]
    if value is None:
        return "pyNone"
    if value is a:
        return compact(k_a)
    if value is b:
        return compact(k_b)
    raise AssertionError(f"result {value!r} is not either original argument")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    args = parser.parse_args()

    generated = load_entry(args.solution, "generated_solution_for_k_compare")
    canonical = load_entry(args.canonical, "canonical_for_k_compare")

    cases = [
        Case("prompt-1", 1, 2.5, "pyInt(1)", "pyFloat(25,10)"),
        Case("prompt-2", 1, "2,3", "pyInt(1)", 'pyStr("2,3")'),
        Case("prompt-3", "5,1", "6", 'pyStr("5,1")', 'pyStr("6")'),
        Case("prompt-4", "1", 1, 'pyStr("1")', "pyInt(1)"),
        Case("equal-int", 7, 7, "pyInt(7)", "pyInt(7)"),
        Case("a-greater-int", 8, 7, "pyInt(8)", "pyInt(7)"),
        Case("b-greater-int", 7, 8, "pyInt(7)", "pyInt(8)"),
        Case("negative-mixed", -3, -4.5, "pyInt(-3)", "pyFloat(-45,10)"),
        Case("equal-rational-floats", 0.5, 0.5, "pyFloat(1,2)", "pyFloat(2,4)"),
        Case("a-greater-rational-floats", 1.5, 1.0, "pyFloat(3,2)", "pyFloat(1,1)"),
        Case("b-greater-rational-floats", 0.5, 1.0, "pyFloat(1,2)", "pyFloat(1,1)"),
        Case("comma-negative", "-2,5", -3, 'pyStr("-2,5")', "pyInt(-3)"),
        Case(
            "ieee-int-rounding",
            2**53 + 1,
            2**53,
            f"pyInt({2**53 + 1})",
            f"pyInt({2**53})",
        ),
        Case(
            "ieee-string-rounding",
            str(2**53 + 1),
            2**53,
            f'pyStr("{2**53 + 1}")',
            f"pyInt({2**53})",
        ),
        Case("empty-a", "", 0, 'pyStr("")', "pyInt(0)", "invalid-string"),
        Case("empty-b", 0, "", "pyInt(0)", 'pyStr("")', "invalid-string"),
    ]

    mismatch_count = 0
    for case in cases:
        generated_outcome = python_outcome(generated, case.a, case.b)
        canonical_outcome = python_outcome(canonical, case.a, case.b)
        expected = expected_term(
            generated_outcome, case.a, case.b, case.k_a, case.k_b
        )
        command = [
            "krun",
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cA={case.k_a}",
            f"-cB={case.k_b}",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        match = re.search(r"<result>(.*?)</result>", completed.stdout, re.S)
        actual = compact(match.group(1)) if match else "<NO_RESULT_CELL>"
        same_python = generated_outcome == canonical_outcome
        same_k = completed.returncode == 0 and actual == expected
        if not same_python or not same_k:
            mismatch_count += 1

        print(f"CASE={case.label} DOMAIN={case.domain}")
        print("COMMAND:", " ".join(command))
        print(f"KRUN_EXIT_STATUS={completed.returncode}")
        print(f"GENERATED_PYTHON={generated_outcome!r}")
        print(f"CANONICAL_PYTHON={canonical_outcome!r}")
        print(f"EXPECTED_FROM_PYTHON={expected}")
        print(f"K_RESULT={actual}")
        print(f"PYTHON_AGREES={same_python} K_AGREES={same_k}")
        if completed.stderr:
            print("KRUN_STDERR_BEGIN")
            print(completed.stderr.rstrip())
            print("KRUN_STDERR_END")

    print(f"CASE_COUNT={len(cases)}")
    print(f"MISMATCH_COUNT={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
