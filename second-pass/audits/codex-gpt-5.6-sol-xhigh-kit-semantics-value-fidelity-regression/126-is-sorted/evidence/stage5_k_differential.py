#!/usr/bin/env python3
"""Independent concrete-K differential against an adjacent/Counter oracle."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path


def oracle(values: list[int]) -> bool:
    return (
        all(left <= right for left, right in zip(values, values[1:]))
        and all(count <= 2 for count in Counter(values).values())
    )


def cases() -> list[list[int]]:
    named = [
        [],
        [5],
        [1, 2, 3, 4, 5],
        [1, 3, 2, 4, 5],
        [1, 2, 2, 3, 3, 4],
        [1, 2, 2, 2, 3, 4],
        [0, 0],
        [0, 0, 0],
        [1, 0],
        [0, 10**40],
        [10**40, 0],
    ]
    generated = [
        list(values)
        for length in range(5)
        for values in itertools.product(range(4), repeat=length)
    ]
    unique: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for values in named + generated:
        key = tuple(values)
        if key not in seen:
            seen.add(key)
            unique.append(values)
    return unique


def write_text_with_hash(path: Path, text: str) -> str:
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", required=True, type=Path)
    parser.add_argument("--translator", required=True, type=Path)
    parser.add_argument("--definition", required=True, type=Path)
    parser.add_argument("--program-py", required=True, type=Path)
    parser.add_argument("--program-mpy", required=True, type=Path)
    parser.add_argument("--inputs-out", required=True, type=Path)
    args = parser.parse_args()

    selected_cases = cases()
    with args.inputs_out.open("w", encoding="utf-8") as inputs:
        for case_id, values in enumerate(selected_cases):
            inputs.write(
                json.dumps(
                    {
                        "id": case_id,
                        "input": values,
                        "oracle": oracle(values),
                    },
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            )

    original_source = args.solution.read_text(encoding="utf-8").rstrip()
    assertions = "\n".join(
        f"assert is_sorted({values!r}) == {oracle(values)!r}"
        for values in selected_cases
    )
    program_source = original_source + "\n\n" + assertions + "\n"
    py_hash = write_text_with_hash(args.program_py, program_source)

    translated = subprocess.run(
        ["python3", str(args.translator), str(args.program_py)],
        text=True,
        capture_output=True,
        check=False,
    )
    if translated.stderr:
        print("TRANSLATOR_STDERR=" + translated.stderr.strip())
    mpy_hash = write_text_with_hash(args.program_mpy, translated.stdout)
    print(f"TRANSLATOR_EXIT={translated.returncode}")

    executed = subprocess.run(
        ["krun", str(args.program_mpy), "--definition", str(args.definition)],
        text=True,
        capture_output=True,
        check=False,
    )
    compact = "".join(executed.stdout.split())
    no_exception = "<exc>NoExc</exc>" in compact
    zero_exit_cell = "<exit-code>0</exit-code>" in compact
    print(f"K_RUN_EXIT={executed.returncode}")
    print(f"K_NO_EXCEPTION={str(no_exception).lower()}")
    print(f"K_EXIT_CELL_ZERO={str(zero_exit_cell).lower()}")
    if executed.stderr:
        print("K_STDERR=" + executed.stderr.strip())
    print(f"CASES={len(selected_cases)}")
    print(f"PROGRAM_PY_SHA256={py_hash}")
    print(f"PROGRAM_MPY_SHA256={mpy_hash}")
    print(
        "INPUTS_SHA256="
        + hashlib.sha256(args.inputs_out.read_bytes()).hexdigest()
    )
    failures = (
        translated.returncode != 0
        or executed.returncode != 0
        or not no_exception
        or not zero_exit_cell
    )
    print(f"ASSERTION_FAILURES={int(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
