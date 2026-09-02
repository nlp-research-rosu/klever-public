#!/usr/bin/env python3
"""Compare fresh K execution with independent CPython executions."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/124-valid-date")
CANDIDATE_ROOT = ROOT / "candidate"
DEFINITION = ROOT / "build" / "semantic-kompiled"


def import_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


solution = import_path("candidate_solution_for_k", CANDIDATE_ROOT / "solution.py")
canonical = import_path("trusted_canonical_for_k", ROOT / "canonical.py")
program = " ".join((CANDIDATE_ROOT / "solution.regenerated.mpy").read_text().splitlines())

cases = [
    "",
    "03-11-2000",
    "15-01-2012",
    "04-0-2040",
    "06/04/2020",
    "aa-bb-cccc",
    "00-01-2020",
    "13-01-2020",
    "12-00-2020",
    "02-29-1900",
    "02-30-2020",
    "04-30-2020",
    "04-31-2020",
    "01-31-0000",
    "01-32-2020",
    "٠٣-١١-٢٠٠٠",
    "０３-１１-２０００",
]

failures = 0
for value in cases:
    k_string = json.dumps(value, ensure_ascii=False)
    term = (
        f"runProgram({program}, \"valid_date\", "
        f"vals(strVal({k_string})))"
    )
    command = [
        "krun",
        "--definition",
        str(DEFINITION),
        f"-cPGM={term}",
        "--output",
        "program",
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    match = re.search(r"boolVal\s*\(\s*(true|false)\s*\)", result.stdout)
    k_value = None if match is None else match.group(1) == "true"
    python_value = solution.valid_date(value)
    canonical_value = canonical.valid_date(value)
    same = result.returncode == 0 and k_value == python_value
    failures += int(not same)
    print("COMMAND=" + shlex.join(command))
    print(f"EXIT_STATUS={result.returncode}")
    print(f"STDOUT={result.stdout.strip()!r}")
    print(f"STDERR={result.stderr.strip()!r}")
    print(
        f"RESULT input={value!r} k={k_value!r} "
        f"candidate_python={python_value!r} canonical_python={canonical_value!r} "
        f"K_EQUALS_CANDIDATE={same}"
    )

print(f"TOTAL_CASES={len(cases)}")
print(f"K_CANDIDATE_MISMATCHES={failures}")
raise SystemExit(0 if failures == 0 else 1)
