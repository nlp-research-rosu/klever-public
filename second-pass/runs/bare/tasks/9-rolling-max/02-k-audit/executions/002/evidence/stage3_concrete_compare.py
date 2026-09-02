#!/usr/bin/env python3
"""Run fresh generated K semantics and compare final values with both Pythons."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import re
import subprocess
import sys


WORK = Path("/tmp/audit-work/candidate")
DEFINITION = WORK / "fresh-semantic-kompiled"


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rolling_max


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"), "canonical_stage3")
    generated = load_function(WORK / "solution.py", "generated_stage3")
    module_term = (WORK / "solution.regenerated.mpy").read_text(encoding="utf-8").strip()
    cases = [
        ("empty", []),
        ("singleton_negative", [-7]),
        ("increase", [1, 2]),
        ("equal", [2, 2]),
        ("decrease", [2, 1]),
        ("all_negative", [-5, -9, -3, -4]),
        ("zero_crossings", [0, -1, 1, -2, 2]),
        ("prompt", [1, 2, 3, 2, 3, 4, 2]),
        (
            "arbitrary_precision",
            [-(10**40), 0, 10**40, -1],
        ),
    ]
    failures = 0
    for name, numbers in cases:
        rendered_numbers = ", ".join(str(number) for number in numbers)
        program = f"Run(\n{module_term},\n[{rendered_numbers}])\n"
        command = [
            "krun",
            "/dev/stdin",
            "--definition",
            str(DEFINITION),
            "--output",
            "pretty",
        ]
        run = subprocess.run(
            command,
            cwd=WORK,
            input=program,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        actual = [
            int(match)
            for match in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", run.stdout)
        ]
        expected_canonical = canonical(numbers.copy())
        expected_generated = generated(numbers.copy())
        clean_terminal = (
            "<functions>\n    .Map\n  </functions>" in run.stdout
            and "<env>\n    .Map\n  </env>" in run.stdout
            and "<stack>\n    .List\n  </stack>" in run.stdout
        )
        ok = (
            run.returncode == 0
            and actual == expected_canonical
            and actual == expected_generated
            and clean_terminal
        )
        failures += not ok
        print(f"CASE: {name}")
        print("INPUT_NUMBERS:", numbers)
        print(
            "INPUT_TERM_SHA256:",
            hashlib.sha256(program.encode("utf-8")).hexdigest(),
        )
        print("COMMAND:", " ".join(command))
        print("EXIT_STATUS:", run.returncode)
        print("K_RESULT:", actual)
        print("CANONICAL_RESULT:", expected_canonical)
        print("GENERATED_PYTHON_RESULT:", expected_generated)
        print("TERMINAL_CELLS_CLEAN:", clean_terminal)
        print("MATCH:", ok)
    print("TOTAL_CASES:", len(cases))
    print("MISMATCHES:", failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
