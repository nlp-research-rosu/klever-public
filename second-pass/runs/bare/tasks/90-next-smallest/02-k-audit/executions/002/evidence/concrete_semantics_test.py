#!/usr/bin/env python3
"""Compare freshly rebuilt generated K semantics with independent Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shlex
import subprocess


ROOT = Path("/tmp/audit-work/90-next-smallest")
SOLUTION = ROOT / "candidate-src" / "solution.mpy"
DEFINITION = ROOT / "semantic-fresh-kompiled"


def load_generated():
    path = ROOT / "candidate-src" / "solution.py"
    spec = importlib.util.spec_from_file_location("semantics_generated_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


def oracle(values: list[int]):
    least = None
    second = None
    for value in values:
        if least is None or value < least:
            if least is None or value != least:
                second = least
            least = value
        elif value != least and (second is None or value < second):
            second = value
    return second


def k_list(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value},{result})"
    return result


def parse_result(output: str):
    match = re.search(r"<result>\s*(.*?)\s*</result>", output, flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"no <result> cell in K output:\n{output}")
    text = " ".join(match.group(1).split())
    if text == "none":
        return None
    if re.fullmatch(r"-?[0-9]+", text):
        return int(text)
    raise AssertionError(f"unexpected K result term: {text}")


def main() -> int:
    generated = load_generated()
    cases = [
        [],
        [0],
        [1, 1],
        [-1, 4],
        [4, -1],
        [1, 2, 3, 4, 5],
        [5, 1, 4, 3, 2],
        [-5, -5, -4],
        [9, 9, -8, 9, -8],
        [3, 1, 2, 2, 8, 1],
        [7, 7, 7, 7, 7],
        [10**30, -(10**30), 0, 10**30],
    ]
    for values in cases:
        input_term = k_list(values)
        command = [
            "krun",
            str(SOLUTION),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={input_term}",
        ]
        print(f"COMMAND: {shlex.join(command)}")
        completed = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(completed.stdout.rstrip())
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        assert completed.returncode == 0
        actual_k = parse_result(completed.stdout)
        expected = oracle(values)
        actual_python = generated(list(values))
        print(
            f"COMPARE input={values!r} K={actual_k!r} "
            f"generated_python={actual_python!r} oracle={expected!r}"
        )
        assert actual_k == expected
        assert actual_python == expected
    print(f"CONCRETE_SEMANTICS_STATUS OK cases={len(cases)} mismatches=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
