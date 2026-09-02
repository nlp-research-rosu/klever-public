#!/usr/bin/env python3
"""Compare fresh generated K-semantics executions with both Python versions."""

from __future__ import annotations

import hashlib
import importlib.util
import argparse
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


DEFAULT_WORK = Path("/tmp/audit-work/reconstruction/candidate")
CANONICAL = Path("/tmp/audit-work/reconstruction/trusted/canonical.py")
INPUTS = [
    1,
    3,
    4,
    5,
    8,
    9,
    10,
    19,
    39,
    40,
    49,
    50,
    89,
    90,
    99,
    100,
    152,
    399,
    400,
    426,
    499,
    500,
    899,
    900,
    944,
    999,
    1000,
]
RESULT_RE = re.compile(r'<result>\s*result\s*\(\s*vStr\s*\(\s*"([^"]*)"\s*\)\s*\)\s*</result>', re.S)


def load_function(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.int_to_mini_roman


def run_k(number: int, work: Path, definition: Path) -> tuple[int, int, str, str]:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(definition),
        f"-cINPUT={number}",
    ]
    completed = subprocess.run(
        command,
        cwd=work,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    match = RESULT_RE.search(completed.stdout)
    result = match.group(1) if match else "<NO_RESULT_MATCH>"
    return number, completed.returncode, result, completed.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=DEFAULT_WORK)
    parser.add_argument("--definition", type=Path)
    args = parser.parse_args()
    work = args.work
    definition = args.definition or (work / "semantic-haskell-fresh-kompiled")

    canonical = load_function("concrete_oracle", CANONICAL)
    candidate = load_function("concrete_candidate", work / "solution.py")
    with ThreadPoolExecutor(max_workers=4) as executor:
        raw_rows = list(
            executor.map(lambda number: run_k(number, work, definition), INPUTS)
        )

    failures = 0
    for number, returncode, k_result, output in raw_rows:
        expected = canonical(number)
        python_result = candidate(number)
        final_k = bool(re.search(r"<k>\s*\.K\s*</k>", output, re.S))
        output_hash = hashlib.sha256(output.encode()).hexdigest()
        ok = (
            returncode == 0
            and final_k
            and k_result == expected
            and python_result == expected
        )
        failures += not ok
        print(
            f"input={number} k_exit={returncode} final_k={final_k} "
            f"k={k_result!r} candidate_py={python_result!r} "
            f"canonical_py={expected!r} output_sha256={output_hash} ok={ok}"
        )
        if not ok:
            print("BEGIN_UNEXPECTED_K_OUTPUT")
            print(output)
            print("END_UNEXPECTED_K_OUTPUT")
    print(
        f"definition={definition} cases={len(raw_rows)} "
        f"failures={failures}"
    )
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
