#!/usr/bin/env python3
"""Run the concrete-K differential corpus in parser-bounded batches."""

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


def build_cases() -> list[list[int]]:
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
    exhaustive = [
        list(values)
        for length in range(5)
        for values in itertools.product(range(4), repeat=length)
    ]
    result: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for values in named + exhaustive:
        key = tuple(values)
        if key not in seen:
            seen.add(key)
            result.append(values)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", required=True, type=Path)
    parser.add_argument("--translator", required=True, type=Path)
    parser.add_argument("--definition", required=True, type=Path)
    parser.add_argument("--batch-dir", required=True, type=Path)
    parser.add_argument("--inputs-out", required=True, type=Path)
    parser.add_argument("--batch-size", type=int, default=40)
    args = parser.parse_args()

    selected_cases = build_cases()
    args.batch_dir.mkdir(parents=True, exist_ok=True)
    with args.inputs_out.open("w", encoding="utf-8") as inputs:
        for case_id, values in enumerate(selected_cases):
            inputs.write(
                json.dumps(
                    {"id": case_id, "input": values, "oracle": oracle(values)},
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            )

    original_source = args.solution.read_text(encoding="utf-8").rstrip()
    combined_digest = hashlib.sha256()
    failures = 0
    batch_count = 0
    for start in range(0, len(selected_cases), args.batch_size):
        batch_count += 1
        batch = selected_cases[start : start + args.batch_size]
        assertions = "\n".join(
            f"assert is_sorted({values!r}) == {oracle(values)!r}"
            for values in batch
        )
        source = original_source + "\n\n" + assertions + "\n"
        py_path = args.batch_dir / f"batch-{batch_count:02d}.py"
        mpy_path = args.batch_dir / f"batch-{batch_count:02d}.mpy"
        py_path.write_text(source, encoding="utf-8")

        translated = subprocess.run(
            ["python3", str(args.translator), str(py_path)],
            text=True,
            capture_output=True,
            check=False,
        )
        mpy_path.write_text(translated.stdout, encoding="utf-8")
        combined_digest.update(py_path.read_bytes())
        combined_digest.update(b"\0")
        combined_digest.update(mpy_path.read_bytes())
        combined_digest.update(b"\0")

        executed = subprocess.run(
            ["krun", str(mpy_path), "--definition", str(args.definition)],
            text=True,
            capture_output=True,
            check=False,
        )
        compact = "".join(executed.stdout.split())
        passed = (
            translated.returncode == 0
            and executed.returncode == 0
            and "<exc>NoExc</exc>" in compact
            and "<exit-code>0</exit-code>" in compact
        )
        failures += not passed
        print(
            f"BATCH={batch_count} START={start} COUNT={len(batch)} "
            f"TRANSLATOR_EXIT={translated.returncode} K_EXIT={executed.returncode} "
            f"PASS={str(passed).lower()}"
        )
        if not passed:
            print("TRANSLATOR_STDERR=" + translated.stderr.strip())
            print("K_STDERR=" + executed.stderr.strip())

    print(f"CASES={len(selected_cases)}")
    print(f"BATCHES={batch_count}")
    print(f"BATCH_FAILURES={failures}")
    print(f"PROGRAM_SET_SHA256={combined_digest.hexdigest()}")
    print(
        "INPUTS_SHA256="
        + hashlib.sha256(args.inputs_out.read_bytes()).hexdigest()
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
