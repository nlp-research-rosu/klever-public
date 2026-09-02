#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with both Python functions."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/reconstruction")
DEFINITION = ROOT / "fresh-llvm-kompiled"
PROGRAM = ROOT / "candidate-src/solution.mpy"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_result(brackets: str) -> tuple[bool, int]:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cINPUT={json.dumps(brackets)}",
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    output = completed.stdout + completed.stderr
    matches = re.findall(
        r"result\s*\(\s*BVal\s*\(\s*(true|false)\s*\)\s*\)", output
    )
    if completed.returncode != 0 or len(matches) != 1:
        print(f"command={command!r}")
        print(f"raw_output={output!r}")
        raise RuntimeError(
            f"krun failure for {brackets!r}: exit={completed.returncode}, "
            f"result_matches={matches!r}"
        )
    return matches[0] == "true", completed.returncode


def main() -> int:
    canonical = load_module(
        "trusted_canonical", ROOT / "reference/canonical.py"
    ).correct_bracketing
    candidate = load_module(
        "generated_solution", ROOT / "candidate-src/solution.py"
    ).correct_bracketing

    cases = [
        "",
        "<",
        ">",
        "<>",
        "><",
        "<<",
        ">>",
        "<<>>",
        "<><>",
        "<>>",
        "<<><>>",
        "<<<>>>",
        "<<><>",
        "><<>",
    ]
    mismatches = 0
    print(f"definition={DEFINITION}")
    print(f"program={PROGRAM}")
    for brackets in cases:
        expected = canonical(brackets)
        python_result = candidate(brackets)
        semantics_result, krun_status = k_result(brackets)
        equal = expected == python_result == semantics_result
        mismatches += int(not equal)
        print(
            f"input={brackets!r} canonical={expected!r} "
            f"candidate_python={python_result!r} "
            f"fresh_krun={semantics_result!r} krun_exit={krun_status} "
            f"all_equal={equal}"
        )
    print(f"cases={len(cases)} mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
