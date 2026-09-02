#!/usr/bin/env python3
"""Compare freshly compiled generated K semantics with both Python programs."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "audit-semantic-kompiled"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def parse_result(output: str) -> list[int]:
    match = re.search(
        r"<result>\s*done\s*\(\s*listVal\s*\((.*?)\)\s*\)\s*</result>",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        raise RuntimeError(f"no completed list result in krun output:\n{output}")
    body = match.group(1)
    if re.fullmatch(r"\s*\.List\s*", body):
        return []
    return [
        int(value)
        for value in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", body)
    ]


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "sem_diff_canonical")
    candidate = load_entry(WORK / "solution.py", "sem_diff_candidate")
    inputs = [-1, 0, 1, 2, 3, 4, 5, 8, 10, 12]
    mismatches = 0
    for n in inputs:
        command = [
            "krun",
            "solution.regenerated.mpy",
            f"-cINPUT={n}",
            "--definition",
            str(DEFINITION),
        ]
        print("COMMAND:", " ".join(command))
        result = subprocess.run(
            command,
            cwd=WORK,
            check=False,
            capture_output=True,
            text=True,
        )
        print(f"KRUN_EXIT_STATUS n={n}: {result.returncode}")
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            mismatches += 1
            continue
        k_value = parse_result(result.stdout)
        canonical_value = canonical(n)
        candidate_value = candidate(n)
        same = k_value == canonical_value == candidate_value
        mismatches += not same
        print(
            f"n={n} k={k_value} canonical={canonical_value} "
            f"candidate={candidate_value} match={same}"
        )
    print(f"case_count={len(inputs)}")
    print(f"mismatch_count={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
