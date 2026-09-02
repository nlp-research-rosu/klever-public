#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with independent Python."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path
from typing import Callable


SOURCE = Path("/tmp/audit-work/candidate-src/solution.mpy")
DEFINITION = Path("/tmp/audit-work/build/semantic-llvm-kompiled")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


def int_seq(values: list[int]) -> str:
    term = ".Ints"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def parse_result(output: str) -> int:
    compact = " ".join(output.split())
    match = re.search(r"<result> VInt \( (-?[0-9]+) \) </result>", compact)
    if match is None:
        raise AssertionError(f"cannot find VInt result in: {compact}")
    return int(match.group(1))


def main() -> None:
    generated = load_entry(
        Path("/tmp/audit-work/candidate-src/solution.py"), "generated_python_69"
    )
    canonical = load_entry(
        Path("/tmp/audit-work/trusted/canonical.py"), "canonical_python_69_for_k"
    )
    cases = [
        ("empty_out_of_domain", []),
        ("singleton_qualifies", [1]),
        ("singleton_fails", [2]),
        ("frequency_below", [3, 3]),
        ("frequency_equal", [3, 3, 3]),
        ("inner_if_false", [2, 2, 1]),
        ("example_one", [4, 1, 2, 2, 3, 1]),
        ("example_two", [1, 2, 2, 3, 3, 3, 4, 4, 4]),
        ("example_three", [5, 5, 4, 4, 4]),
        ("multiple_qualifiers", [1, 2, 2, 3, 3, 3]),
    ]
    for label, values in cases:
        input_term = f"VList({int_seq(values)})"
        command = [
            "krun",
            str(SOURCE),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={input_term}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"CASE {label} input={values}")
        print("COMMAND " + " ".join(command))
        print(f"K_EXIT {completed.returncode}")
        if completed.stderr:
            print("K_STDERR " + " ".join(completed.stderr.split()))
        assert completed.returncode == 0
        k_result = parse_result(completed.stdout)
        generated_result = generated(list(values))
        if values:
            canonical_result: object = canonical(list(values))
        else:
            try:
                canonical(list(values))
            except Exception as error:
                canonical_result = f"{type(error).__name__}: {error}"
            else:
                raise AssertionError("trusted canonical unexpectedly accepted []")
        print(
            f"RESULT K={k_result} generated_python={generated_result} "
            f"canonical_python={canonical_result}"
        )
        assert k_result == generated_result
        if values:
            assert k_result == canonical_result
    print("FRESH_CONCRETE_SEMANTICS_PASS")


if __name__ == "__main__":
    main()
