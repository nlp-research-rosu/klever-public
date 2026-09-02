#!/usr/bin/env python3
"""Probe behavior outside the prompt's comma/literal-space separator domain."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

from concrete_compare import extract_result


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--definition", required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "canonical_scope")
    candidate = load_entry(args.candidate, "candidate_scope")
    cases = ["a\tb", "a\nb", "a\rb", "a\u00a0b"]
    records = []
    for value in cases:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            args.definition,
            f"-cINPUT={json.dumps(value)}",
            "--output",
            "json",
        ]
        completed = subprocess.run(
            command,
            cwd=args.workdir,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        k_result = extract_result(json.loads(completed.stdout))
        python_result = candidate(value)
        canonical_result = canonical(value)
        records.append(
            {
                "input": value,
                "command": command,
                "krun_exit": completed.returncode,
                "k": k_result,
                "candidate": python_result,
                "canonical": canonical_result,
                "diverges": (
                    k_result != python_result
                    and python_result == canonical_result
                ),
            }
        )
    divergence_count = sum(record["diverges"] for record in records)
    print(
        json.dumps(
            {
                "scope": "outside prompt domain: separators are whitespace other than literal space",
                "case_count": len(cases),
                "expected_divergence_count": len(cases),
                "observed_divergence_count": divergence_count,
                "cases": records,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if divergence_count == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
