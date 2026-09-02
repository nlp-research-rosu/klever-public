#!/usr/bin/env python3
"""Ground substitutions for the sole entry claim."""

from __future__ import annotations

import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def numeric_is_prime(value: int) -> bool:
    return value >= 2 and all(
        value % divisor for divisor in range(2, math.isqrt(value) + 1)
    )


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: stage4_substitution.py DEFINITION PROGRAM GENERATED.py CANONICAL.py"
        )
    definition, program, generated_path, canonical_path = sys.argv[1:]
    generated = load_module("stage4_generated", Path(generated_path))
    canonical = load_module("stage4_canonical", Path(canonical_path))
    cases = ["", "ab", "Hello", "λ", "🙂🙂"]
    failures = []
    adequacy_mismatches = []
    for text in cases:
        argument = f"VStr({json.dumps(text, ensure_ascii=False)})"
        command = [
            "krun",
            program,
            "--definition",
            definition,
            f"-cARG={argument}",
        ]
        run = subprocess.run(command, text=True, capture_output=True)
        n_match = re.search(r'"n"\s*\|->\s*VInt\s*\(\s*(\d+)\s*\)', run.stdout)
        result_match = re.search(r"VBool\s*\(\s*(true|false)\s*\)", run.stdout)
        k_length = None if n_match is None else int(n_match.group(1))
        k_return = None if result_match is None else result_match.group(1) == "true"
        formal_rhs = None if k_length is None else numeric_is_prime(k_length)
        generated_result = generated.prime_length(text)
        canonical_result = canonical.prime_length(text)
        row = {
            "input": text,
            "python_length": len(text),
            "k_lengthString_observed": k_length,
            "formal_postcondition_isPrime": formal_rhs,
            "k_return": k_return,
            "generated_python": generated_result,
            "trusted_canonical_python": canonical_result,
            "krun_exit": run.returncode,
        }
        print("COMMAND:", json.dumps(command, ensure_ascii=False))
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))
        if run.stderr:
            print("STDERR:", run.stderr.rstrip())
        if not (
            run.returncode == 0
            and k_return is not None
            and formal_rhs is not None
            and k_return == formal_rhs
        ):
            failures.append({"kind": "formal-claim-mismatch", **row})
        if generated_result != canonical_result:
            failures.append({"kind": "python-differential", **row})
        if k_return != generated_result or formal_rhs != generated_result:
            adequacy_mismatches.append(row)
    print(
        json.dumps(
            {
                "formal_execution_failure_count": sum(
                    item["kind"] == "formal-claim-mismatch" for item in failures
                ),
                "python_differential_failure_count": sum(
                    item["kind"] == "python-differential" for item in failures
                ),
                "formal_to_python_adequacy_mismatch_count": len(adequacy_mismatches),
                "formal_to_python_adequacy_mismatches": adequacy_mismatches,
                "note": (
                    "Differences between K/formal and both Python values are "
                    "reported in the rows but do not make this script exit nonzero; "
                    "they are adequacy failures, not failures of internal K closure."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
