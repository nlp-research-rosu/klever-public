#!/usr/bin/env python3
"""Locate the first concrete K/canonical assertion mismatch in a generated batch."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: bisect_k_bridge.py BATCH_PY TRANSLATOR RUNTIME_DEFINITION EVIDENCE_DIR",
            file=sys.stderr,
        )
        return 64

    batch_path, translator, definition, evidence_dir = (
        Path(sys.argv[1]),
        Path(sys.argv[2]),
        Path(sys.argv[3]),
        Path(sys.argv[4]),
    )
    lines = batch_path.read_text(encoding="utf-8").splitlines()
    first_assert = next(i for i, line in enumerate(lines) if line.startswith("assert "))
    base = lines[:first_assert]
    assertions = [line for line in lines[first_assert:] if line.startswith("assert ")]

    scratch = Path("/tmp/audit-work/k-bridge-diagnostic")
    scratch.mkdir(parents=True, exist_ok=True)

    def run_prefix(count: int) -> tuple[int, str]:
        py_path = scratch / "prefix.py"
        mpy_path = scratch / "prefix.mpy"
        py_path.write_text("\n".join(base + assertions[:count]) + "\n", encoding="utf-8")
        translated = subprocess.run(
            [sys.executable, str(translator), str(py_path)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if translated.returncode != 0:
            return translated.returncode, "translator: " + translated.stderr[-1000:]
        mpy_path.write_text(translated.stdout, encoding="utf-8")
        ran = subprocess.run(
            ["krun", str(mpy_path), "--definition", str(definition)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return ran.returncode, ran.stdout

    low, high = 1, len(assertions)
    while low < high:
        middle = (low + high) // 2
        status, output = run_prefix(middle)
        print(f"PREFIX_COUNT={middle} EXIT_STATUS={status}")
        if status == 0:
            low = middle + 1
        elif status == 1 and "AssertionError" in output:
            high = middle
        else:
            print("UNEXPECTED_DIAGNOSTIC_OUTPUT:")
            print(output[-3000:])
            return 2

    failure_index = low
    before_status, _ = run_prefix(failure_index - 1) if failure_index > 1 else (0, "")
    fail_status, fail_output = run_prefix(failure_index)
    print(f"FIRST_FAILURE_INDEX_1_BASED={failure_index}")
    print(f"PREVIOUS_PREFIX_EXIT_STATUS={before_status}")
    print(f"FAILING_PREFIX_EXIT_STATUS={fail_status}")
    print(f"FAILING_ASSERTION={assertions[failure_index - 1]}")
    if before_status != 0 or fail_status != 1 or "AssertionError" not in fail_output:
        print(fail_output[-3000:])
        return 3

    failing_py = evidence_dir / "05_k_bridge_failing_prefix.py"
    failing_mpy = evidence_dir / "05_k_bridge_failing_prefix.mpy"
    failing_py.write_text(
        "\n".join(base + assertions[:failure_index]) + "\n", encoding="utf-8"
    )
    translated = subprocess.run(
        [sys.executable, str(translator), str(failing_py)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if translated.returncode != 0:
        print(translated.stderr)
        return 4
    failing_mpy.write_text(translated.stdout, encoding="utf-8")

    match = re.fullmatch(
        r"assert triangle_area\((.*)\) == (.*)", assertions[failure_index - 1]
    )
    if match is None:
        return 5
    args, expected = match.groups()
    probe_py = evidence_dir / "05_k_bridge_result_probe.py"
    probe_mpy = evidence_dir / "05_k_bridge_result_probe.mpy"
    probe_py.write_text(
        "\n".join(base + [f"result = triangle_area({args})"]) + "\n",
        encoding="utf-8",
    )
    translated = subprocess.run(
        [sys.executable, str(translator), str(probe_py)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if translated.returncode != 0:
        print(translated.stderr)
        return 6
    probe_mpy.write_text(translated.stdout, encoding="utf-8")
    probe = subprocess.run(
        ["krun", str(probe_mpy), "--definition", str(definition)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(f"EXPECTED_CANONICAL={expected}")
    print(f"RESULT_PROBE_EXIT_STATUS={probe.returncode}")
    result_lines = [line.strip() for line in probe.stdout.splitlines() if '"result"' in line]
    print("K_RESULT_LINES=" + repr(result_lines))
    return 0 if probe.returncode == 0 and result_lines else 7


if __name__ == "__main__":
    raise SystemExit(main())
