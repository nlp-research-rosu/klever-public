#!/usr/bin/env python3
"""Compare clean-built generated K semantics with CPython execution."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


CASES = (
    ("empty", "DictVal()", {}, False),
    (
        "ascii-lower",
        'DictVal(StrVal("a") StrVal("b"))',
        {"a": 0, "b": 0},
        True,
    ),
    (
        "ascii-upper",
        'DictVal(StrVal("STATE") StrVal("ZIP"))',
        {"STATE": 0, "ZIP": 0},
        True,
    ),
    (
        "mixed",
        'DictVal(StrVal("a") StrVal("A"))',
        {"a": 0, "A": 0},
        False,
    ),
    (
        "non-string",
        'DictVal(StrVal("a") IntVal(8))',
        {"a": 0, 8: 0},
        False,
    ),
    (
        "uncased-only",
        'DictVal(StrVal("123"))',
        {"123": 0},
        False,
    ),
    (
        "unicode-lower-boundary",
        'DictVal(StrVal("é"))',
        {"é": 0},
        True,
    ),
    (
        "unicode-upper-boundary",
        'DictVal(StrVal("É"))',
        {"É": 0},
        True,
    ),
)


def load_solution(path: Path):
    spec = importlib.util.spec_from_file_location("generated_solution_for_k", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: k_concrete_differential.py SCRATCH", file=sys.stderr)
        return 2
    scratch = Path(sys.argv[1])
    solution = load_solution(scratch / "solution.py")
    mismatch_count = 0
    for label, k_input, python_input, prompt_expected in CASES:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "concrete-fresh-kompiled",
            f"-cINPUT={k_input}",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=scratch,
            text=True,
            capture_output=True,
            check=False,
        )
        match = re.search(r"BoolVal \( (true|false) \)", completed.stdout)
        k_result = None if match is None else match.group(1) == "true"
        python_result = solution(python_input)
        matches = (
            completed.returncode == 0
            and k_result == python_result
            and python_result == prompt_expected
        )
        if not matches:
            mismatch_count += 1
        print(
            json.dumps(
                {
                    "label": label,
                    "command": command,
                    "command_exit": completed.returncode,
                    "k_input": k_input,
                    "k_result": k_result,
                    "python_keys": [repr(key) for key in python_input],
                    "python_result": python_result,
                    "prompt_expected": prompt_expected,
                    "all_equal": matches,
                    "krun_stdout": completed.stdout.strip(),
                    "krun_stderr": completed.stderr.strip(),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    print(
        json.dumps(
            {"cases": len(CASES), "mismatch_count": mismatch_count},
            sort_keys=True,
        )
    )
    return 0 if mismatch_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
