#!/usr/bin/env python3
"""Compare fresh K execution with both Python implementations and an oracle."""

from __future__ import annotations

import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def oracle(text: str) -> bool:
    length = len(text)
    return length >= 2 and all(
        length % divisor for divisor in range(2, math.isqrt(length) + 1)
    )


def shell_quote(arg: str) -> str:
    return "'" + arg.replace("'", "'\\''") + "'"


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: stage3_concrete.py DEFINITION PROGRAM GENERATED.py CANONICAL.py"
        )
    definition, program, generated_path, canonical_path = sys.argv[1:]
    generated = load_module("generated_solution_for_k_compare", Path(generated_path))
    canonical = load_module("trusted_canonical_for_k_compare", Path(canonical_path))

    cases = [
        ("empty", ""),
        ("one-ascii", "a"),
        ("two-ascii", "ab"),
        ("three-prime", "abc"),
        ("four-composite", "abcd"),
        ("five-prime", "abcde"),
        ("six-composite", "orange"),
        ("eight-composite", "abcdefgh"),
        ("square-49", "x" * 49),
        ("prime-97", "x" * 97),
        ("one-accented-codepoint", "é"),
        ("two-unicode-codepoints", "éλ"),
        ("one-non-BMP-codepoint", "🙂"),
        ("two-non-BMP-codepoints", "🙂🙂"),
    ]
    failures = []
    for label, text in cases:
        arg = f"VStr({json.dumps(text, ensure_ascii=False)})"
        command = [
            "krun",
            program,
            "--definition",
            definition,
            f"-cARG={arg}",
        ]
        print("CASE", label, "PYTHON_LENGTH", len(text), "INPUT", repr(text))
        print("COMMAND:", " ".join(shell_quote(part) for part in command))
        run = subprocess.run(command, text=True, capture_output=True)
        print("KRUN_EXIT:", run.returncode)
        print("KRUN_STDOUT:")
        print(run.stdout.rstrip())
        if run.stderr:
            print("KRUN_STDERR:")
            print(run.stderr.rstrip())
        match = re.search(r"VBool\s*\(\s*(true|false)\s*\)", run.stdout)
        k_result = None if match is None else match.group(1) == "true"
        expected = oracle(text)
        generated_result = generated.prime_length(text)
        canonical_result = canonical.prime_length(text)
        row = {
            "label": label,
            "length": len(text),
            "expected": expected,
            "generated": generated_result,
            "canonical": canonical_result,
            "k": k_result,
            "krun_exit": run.returncode,
        }
        print("RESULT:", json.dumps(row, ensure_ascii=False, sort_keys=True))
        if not (
            run.returncode == 0
            and k_result is not None
            and type(generated_result) is bool
            and type(canonical_result) is bool
            and k_result == generated_result == canonical_result == expected
        ):
            failures.append(row)
        print()

    print(
        json.dumps(
            {
                "total_cases": len(cases),
                "failure_count": len(failures),
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
