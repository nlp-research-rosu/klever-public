#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from types import ModuleType


DEFINITION = "/tmp/audit-work/build/semantic-fresh-kompiled"
PROGRAM = "/tmp/audit-work/candidate-src/solution.mpy"
RESULTS = Path("/audit-output/evidence/semantic-concrete-results.jsonl")
CASES = (
    "",
    "1234",
    "ab",
    "#a@C",
    "a1",
    "1a",
    "é",
    "é1",
    "αΒ",
    "ß",
    "中",
    "🙂",
    "Ⅰ",
    "aⅠ",
)


def load(name: str, path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decode_result(output: str) -> str:
    match = re.search(r"<result>\s*(.*?)\s*</result>", output, re.DOTALL)
    if match is None:
        raise ValueError("no <result> cell")
    term = match.group(1)
    codepoints = [int(value) for value in re.findall(r"(-?\d+)\s*::", term)]
    if not codepoints and ".PString" not in term:
        raise ValueError(f"unexpected result term: {term!r}")
    return "".join(chr(value) for value in codepoints)


def main() -> int:
    canonical = load("trusted_canonical_kcheck", "/tmp/audit-work/trusted/canonical.py")
    generated = load("generated_solution_kcheck", "/tmp/audit-work/candidate-src/solution.py")
    failures = 0

    with RESULTS.open("w", encoding="utf-8") as result_stream:
        for value in CASES:
            k_input = f"pstr({json.dumps(value, ensure_ascii=False)})"
            command = [
                "krun",
                PROGRAM,
                "--definition",
                DEFINITION,
                f"-cINPUT={k_input}",
            ]
            print("COMMAND:", shlex.join(command))
            completed = subprocess.run(command, text=True, capture_output=True, check=False)
            print(f"EXIT_STATUS: {completed.returncode}")
            if completed.stderr:
                print("STDERR:", completed.stderr.rstrip())
            try:
                k_result = decode_result(completed.stdout) if completed.returncode == 0 else None
                decode_error = None
            except Exception as error:  # diagnostic evidence, not recovery
                k_result = None
                decode_error = repr(error)
            candidate_result = generated.solve(value)
            canonical_result = canonical.solve(value)
            record = {
                "input": value,
                "k_exit": completed.returncode,
                "k_result": k_result,
                "decode_error": decode_error,
                "generated_python": candidate_result,
                "canonical_python": canonical_result,
                "k_matches_generated": completed.returncode == 0
                and k_result == candidate_result,
                "k_matches_canonical": completed.returncode == 0
                and k_result == canonical_result,
            }
            result_stream.write(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            )
            print("RESULT:", json.dumps(record, ensure_ascii=False, sort_keys=True))
            if not record["k_matches_generated"]:
                failures += 1

    print(f"cases={len(CASES)} k_vs_generated_failures={failures}")
    print(f"full_results={RESULTS}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
