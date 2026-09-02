#!/usr/bin/env python3
"""Run the freshly built K semantics and compare its result with both Python programs."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/106-f")
EVIDENCE = Path("/audit-output/evidence")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def parse_result(stdout: str) -> list[int]:
    match = re.search(r"<result>(.*?)</result>", stdout, re.DOTALL)
    if match is None:
        raise ValueError("fresh krun output has no <result> cell")
    result_cell = match.group(1)
    if "done" not in result_cell or "listVal" not in result_cell:
        raise ValueError(f"fresh krun did not return a list: {result_cell!r}")
    return [
        int(item)
        for item in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", result_cell)
    ]


def main() -> int:
    canonical = load_entry(WORK / "reference/canonical.py", "concrete_canonical")
    generated = load_entry(WORK / "source/solution.py", "concrete_generated")
    inputs = [0, 1, 2, 5, 8, 10]
    mismatches = 0
    print(f"INPUTS: {inputs}")
    for n in inputs:
        command = [
            "krun",
            "solution.mpy",
            f"-cINPUT={n}",
            "--definition",
            str(WORK / "build/semantic-kompiled"),
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=WORK / "source",
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        raw_log = (
            f"COMMAND: {' '.join(command)}\n"
            f"STDOUT:\n{completed.stdout}"
            f"STDERR:\n{completed.stderr}"
            f"EXIT_STATUS: {completed.returncode}\n"
        )
        (EVIDENCE / f"02_krun_input_{n}.log").write_text(raw_log)
        print(raw_log, end="")
        try:
            k_value = parse_result(completed.stdout)
        except ValueError as error:
            print(f"PARSE_ERROR: {error}")
            mismatches += 1
            continue
        canonical_value = canonical(n)
        generated_value = generated(n)
        same = (
            completed.returncode == 0
            and k_value == canonical_value
            and k_value == generated_value
        )
        if not same:
            mismatches += 1
        print(
            f"COMPARISON n={n}: same={same} "
            f"K={k_value!r} canonical={canonical_value!r} generated={generated_value!r}"
        )
    print(f"MISMATCH_COUNT: {mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
