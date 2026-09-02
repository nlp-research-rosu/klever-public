#!/usr/bin/env python3
"""Run the freshly rebuilt generated K semantics against Python executions."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/63-fibfib")
CANDIDATE = ROOT / "candidate"
DEFINITION = ROOT / "build" / "concrete-kompiled"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


def main() -> None:
    generated_python = load_entry(CANDIDATE / "solution.py", "concrete_generated")
    cases = [0, 1, 2, 3, 4, 5, 8, 10, 25]
    mismatches = []
    for n in cases:
        command = [
            "krun",
            str(CANDIDATE / "solution.mpy"),
            f"-cN={n}",
            "--definition",
            str(DEFINITION),
        ]
        completed = subprocess.run(
            command,
            cwd=CANDIDATE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print("COMMAND:", " ".join(command))
        print(f"KRUN_EXIT_STATUS={completed.returncode}")
        print(completed.stdout.rstrip())
        match = re.search(r"<result>\s*(-?\d+)\s*</result>", completed.stdout)
        expected = generated_python(n)
        actual = int(match.group(1)) if match else None
        print(f"COMPARE n={n} python={expected} k={actual}")
        if completed.returncode != 0 or actual != expected:
            mismatches.append((n, completed.returncode, expected, actual))
    print(f"SUMMARY cases={len(cases)} mismatches={len(mismatches)}")
    assert mismatches == [], mismatches


if __name__ == "__main__":
    main()
