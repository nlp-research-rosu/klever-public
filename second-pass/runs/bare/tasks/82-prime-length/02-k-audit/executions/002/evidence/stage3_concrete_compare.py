#!/usr/bin/env python3
"""Run freshly compiled generated semantics and compare with both Python functions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys


REBUILD = Path("/tmp/audit-work/rebuild")
DIFF = Path("/tmp/audit-work/differential")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load("trusted_canonical", DIFF / "canonical.py").prime_length
    candidate = load("generated_candidate", DIFF / "solution.py").prime_length
    cases = [
        "",
        "a",
        "ab",
        "abc",
        "abcd",
        "abcde",
        "orange",
        "Hello",
        "a" * 11,
        "a" * 12,
        "éé",
        "😀😀",
        "你好",
        "e\u0301",
    ]

    mismatches = 0
    for index, value in enumerate(cases):
        literal = json.dumps(value, ensure_ascii=False)
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "concrete-haskell-kompiled",
            f"-cARG=VStr({literal})",
        ]
        print(f"CASE {index} value={value!r} python_length={len(value)}")
        print(f"COMMAND {shlex.join(command)}")
        completed = subprocess.run(
            command,
            cwd=REBUILD,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        match = re.search(r"VBool\s*\(\s*(true|false)\s*\)", completed.stdout)
        k_result = None if match is None else match.group(1) == "true"
        canonical_result = canonical(value)
        candidate_result = candidate(value)
        case_ok = (
            completed.returncode == 0
            and k_result is not None
            and k_result == canonical_result == candidate_result
        )
        print(
            f"EXIT {completed.returncode} K={k_result} "
            f"canonical={canonical_result} candidate={candidate_result} ok={case_ok}"
        )
        if not case_ok:
            print(completed.stdout[:8000])
            mismatches += 1

    print(f"cases={len(cases)} mismatches={mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
