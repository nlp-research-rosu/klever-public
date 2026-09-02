#!/usr/bin/env python3
"""Run fresh generated K semantics and compare with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/78-hex-key/candidate-src")
DEFINITION = Path("/tmp/audit-work/78-hex-key/clean-semantic-kompiled")
RESULTS = Path("/audit-output/evidence/semantic-concrete-results.jsonl")
TRUSTED = Path("/reference/canonical.py")
GENERATED = WORK / "solution.py"
CASES = [
    "",
    "AB",
    "1077E",
    "ABED1A33",
    "123456789ABCDEF0",
    "2020",
    *list("0123456789ABCDEF"),
    "0000000000000000",
    "22335577BBDD",
    "FFFFFFFFFFFFFFFF",
]
RESULT_RE = re.compile(r"intVal\s*\(\s*(-?\d+)\s*\)")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


def main() -> int:
    canonical = load_entry("trusted_canonical_semantics_check", TRUSTED)
    generated = load_entry("generated_solution_semantics_check", GENERATED)
    mismatch_count = 0

    with RESULTS.open("w", encoding="utf-8") as stream:
        for value in CASES:
            command = [
                "krun",
                "solution.mpy",
                "--definition",
                str(DEFINITION),
                f"-cINPUT={json.dumps(value)}",
                "--output",
                "pretty",
            ]
            print(f"COMMAND: {shlex.join(command)}")
            completed = subprocess.run(
                command,
                cwd=WORK,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            print(completed.stdout.rstrip())
            print(f"EXIT STATUS: {completed.returncode}")
            match = RESULT_RE.search(completed.stdout)
            k_result = int(match.group(1)) if match else None
            canonical_result = canonical(value)
            generated_result = generated(value)
            equal = (
                completed.returncode == 0
                and k_result == canonical_result
                and k_result == generated_result
            )
            if not equal:
                mismatch_count += 1
            stream.write(
                json.dumps(
                    {
                        "input": value,
                        "k_exit": completed.returncode,
                        "k_result": k_result,
                        "canonical_result": canonical_result,
                        "generated_result": generated_result,
                        "all_equal": equal,
                    },
                    sort_keys=True,
                )
                + "\n"
            )

    print(f"case_count={len(CASES)}")
    print(f"mismatch_count={mismatch_count}")
    print(f"results={RESULTS}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
