#!/usr/bin/env python3
"""Run every generated K/canonical assertion in a fresh K configuration."""

from __future__ import annotations

import concurrent.futures
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: run_k_bridge_isolated.py BATCH_PY TRANSLATOR RUNTIME_DEFINITION",
            file=sys.stderr,
        )
        return 64
    batch_path, translator, definition = map(Path, sys.argv[1:])
    lines = batch_path.read_text(encoding="utf-8").splitlines()
    first_assert = next(i for i, line in enumerate(lines) if line.startswith("assert "))
    base = lines[:first_assert]
    assertions = [line for line in lines[first_assert:] if line.startswith("assert ")]

    root = Path(tempfile.mkdtemp(prefix="isolated-k-bridge-", dir="/tmp/audit-work"))

    def run_one(item: tuple[int, str]) -> tuple[int, int, str]:
        index, assertion = item
        py_path = root / f"case-{index:04d}.py"
        mpy_path = root / f"case-{index:04d}.mpy"
        py_path.write_text("\n".join(base + [assertion]) + "\n", encoding="utf-8")
        translated = subprocess.run(
            [sys.executable, str(translator), str(py_path)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if translated.returncode != 0:
            return index, translated.returncode, "translator: " + translated.stderr[-1000:]
        mpy_path.write_text(translated.stdout, encoding="utf-8")
        ran = subprocess.run(
            ["krun", str(mpy_path), "--definition", str(definition)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return index, ran.returncode, ran.stdout[-1500:]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for result in executor.map(run_one, enumerate(assertions, start=1)):
            results.append(result)

    failures = [(i, status, output) for i, status, output in results if status != 0]
    print(f"TOTAL_ISOLATED_CASES={len(results)}")
    print(f"PASSING_ISOLATED_CASES={len(results) - len(failures)}")
    print(f"FAILING_ISOLATED_CASES={len(failures)}")
    for index, status, output in failures[:20]:
        print(f"FAILURE_INDEX={index} EXIT_STATUS={status}")
        print(f"ASSERTION={assertions[index - 1]}")
        print(output)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
