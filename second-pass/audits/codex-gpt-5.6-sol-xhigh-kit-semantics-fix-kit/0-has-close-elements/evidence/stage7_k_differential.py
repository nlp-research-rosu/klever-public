#!/usr/bin/env python3
"""Independent canonical-oracle differential against the clean LLVM MPY build."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable


EntryPoint = Callable[[list[float], float], bool]


def load_entry(path: Path, name: str) -> EntryPoint:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "has_close_elements")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True, type=Path)
    parser.add_argument("--generated", required=True, type=Path)
    parser.add_argument("--translator", required=True, type=Path)
    parser.add_argument("--definition", required=True, type=Path)
    parser.add_argument("--program-out", required=True, type=Path)
    parser.add_argument("--mpy-out", required=True, type=Path)
    parser.add_argument("--cases-out", required=True, type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "stage7_trusted_canonical")
    generated = load_entry(args.generated, "stage7_generated_solution")
    cases: list[tuple[list[float], float]] = [
        ([], 0.5),
        ([1.0], 100.0),
        ([1.0, 2.0, 3.0], 0.5),
        ([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
        ([1.0, 1.0], 0.1),
        ([1.0, 1.0], 0.0),
        ([1.0, 1.5], 0.5),
        ([1.0, 1.5], math.nextafter(0.5, math.inf)),
        ([-0.0, 0.0], math.ulp(0.0)),
        ([0.0, math.ulp(0.0)], math.nextafter(math.ulp(0.0), math.inf)),
        ([-3.0, 3.0], -1.0),
        ([0.0, 0.01, 100.0, 200.0], 0.02),
    ]

    rng = random.Random(20260722)
    for _ in range(200):
        numbers = [rng.uniform(-1.0e6, 1.0e6) for _ in range(rng.randrange(0, 9))]
        threshold = rng.uniform(-100.0, 1.0e6)
        cases.append((numbers, threshold))

    assertions = []
    serialized = []
    python_mismatches = 0
    for index, (numbers, threshold) in enumerate(cases):
        expected = canonical(numbers, threshold)
        actual = generated(numbers, threshold)
        if actual != expected:
            python_mismatches += 1
        assertions.append(
            f"assert has_close_elements({numbers!r}, {threshold!r}) == {expected!r}"
        )
        serialized.append(
            {
                "index": index,
                "numbers": [value.hex() for value in numbers],
                "threshold": threshold.hex(),
                "canonical": expected,
            }
        )
    args.cases_out.write_text(json.dumps(serialized, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.program_out.write_text(
        args.generated.read_text(encoding="utf-8") + "\n\n" + "\n".join(assertions) + "\n",
        encoding="utf-8",
    )

    translate_command = ["python3", str(args.translator), str(args.program_out)]
    print(f"TRANSLATE_COMMAND={shlex.join(translate_command)} > {shlex.quote(str(args.mpy_out))}")
    with args.mpy_out.open("w", encoding="utf-8") as output:
        translate = subprocess.run(translate_command, stdout=output, stderr=subprocess.PIPE, text=True)
    print(f"TRANSLATE_EXIT={translate.returncode}")
    if translate.stderr:
        print(translate.stderr)
    if translate.returncode != 0:
        return 2

    run_command = ["krun", str(args.mpy_out), "--definition", str(args.definition)]
    print(f"KRUN_COMMAND={shlex.join(run_command)}")
    run = subprocess.run(run_command, capture_output=True, text=True)
    terminated = bool(re.search(r"<k>\s*\.K\s*</k>", run.stdout))
    no_exception = bool(re.search(r"<exc>\s*NoExc\s*</exc>", run.stdout))
    zero_exit_cell = bool(re.search(r"<exit-code>\s*0\s*</exit-code>", run.stdout))
    print(f"KRUN_EXIT={run.returncode}")
    print(f"case_count={len(cases)} python_mismatch_count={python_mismatches}")
    print(f"terminated={terminated} no_exception={no_exception} zero_exit_cell={zero_exit_cell}")
    print(f"cases_file={args.cases_out}")
    if run.returncode != 0 or not terminated or not no_exception or not zero_exit_cell:
        print("KRUN_STDOUT_BEGIN")
        print(run.stdout)
        print("KRUN_STDOUT_END")
        print("KRUN_STDERR_BEGIN")
        print(run.stderr)
        print("KRUN_STDERR_END")
        return 3
    return 1 if python_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
