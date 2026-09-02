#!/usr/bin/env python3
"""Compare fresh generated K semantics with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def k_string(text: str) -> str:
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def main() -> None:
    canonical = load_entry(Path("/reference/canonical.py"), "sem_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/proof/solution.py"), "sem_generated"
    )
    cases = [
        "",
        "<",
        ">",
        "<>",
        "<<",
        ">>",
        "<<>>",
        "<><>",
        "<>>",
        "><<>",
        "<<><>>",
        "<" * 16 + ">" * 16,
    ]
    mismatch_count = 0
    for text in cases:
        command = [
            "krun",
            "/tmp/audit-work/proof/solution.mpy",
            "--definition",
            "/tmp/audit-work/proof/audit-llvm-kompiled",
            f"-cINPUT={k_string(text)}",
        ]
        print(f"COMMAND: {shlex.join(command)}")
        completed = subprocess.run(
            command, check=False, capture_output=True, text=True
        )
        combined = completed.stdout + completed.stderr
        match = re.search(
            r"result\s*\(\s*BVal\s*\(\s*(true|false)\s*\)\s*\)",
            combined,
        )
        k_result = None if match is None else match.group(1) == "true"
        expected = canonical(text)
        candidate = generated(text)
        ok = completed.returncode == 0 and k_result == expected == candidate
        print(
            f"RESULT input={text!r} krun_exit={completed.returncode} "
            f"k={k_result!r} canonical={expected!r} "
            f"generated={candidate!r} match={ok}"
        )
        if not ok:
            mismatch_count += 1
            print("KRUN OUTPUT BEGIN")
            print(combined[:8000])
            print("KRUN OUTPUT END")
    print(f"CONCRETE_CASES count={len(cases)} mismatches={mismatch_count}")
    if mismatch_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
