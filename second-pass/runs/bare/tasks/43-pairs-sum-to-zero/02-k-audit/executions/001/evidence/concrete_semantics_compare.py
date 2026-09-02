#!/usr/bin/env python3
"""Compare fresh K concrete execution with independent Python execution."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
from pathlib import Path


def load_candidate(path: Path):
    spec = importlib.util.spec_from_file_location("candidate_concrete_oracle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero


def iseq(values: list[int]) -> str:
    return " :: ".join([*(str(value) for value in values), ".ISeq"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    args = parser.parse_args()

    candidate = load_candidate(args.python)
    cases = []
    with args.inputs.open(encoding="utf-8") as source:
        for line in source:
            record = json.loads(line)
            cases.append((record["label"], record["input"]))
    mismatches = 0
    for label, values in cases:
        expected = candidate(list(values))
        command = [
            "krun",
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cINPUT={iseq(values)}",
            "--output",
            "pretty",
        ]
        result = subprocess.run(command, text=True, capture_output=True)
        match = re.search(r"pyBool\s*\(\s*(true|false)\s*\)", result.stdout)
        actual = None if match is None else match.group(1) == "true"
        ok = result.returncode == 0 and actual == expected
        print(json.dumps({
            "label": label,
            "input": values,
            "python": expected,
            "k": actual,
            "krun_exit": result.returncode,
            "match": ok,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }, sort_keys=True))
        if not ok:
            mismatches += 1
    print(f"cases={len(cases)} mismatches={mismatches}")
    return int(mismatches != 0)


if __name__ == "__main__":
    raise SystemExit(main())
