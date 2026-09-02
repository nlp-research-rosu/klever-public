#!/usr/bin/env python3
"""Run fresh K semantics on boundary inputs and compare returned values."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


RESULT_RE = re.compile(
    r"<result>\s*returned\s*\(\s*pyStr\s*\(\s*(\"(?:\\.|[^\"\\])*\")"
    r"\s*\)\s*\)\s*</result>",
    re.DOTALL,
)


def load_encode(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path)
    parser.add_argument("definition", type=Path)
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    trusted_encode = load_encode(args.canonical, "trusted_canonical_for_k")
    python_encode = load_encode(args.candidate, "candidate_python_for_k")
    cases = [
        ("empty-zero-iteration", ""),
        ("lower-vowel-then-nonvowel", "ab"),
        ("upper-vowel-then-nonvowel", "AB"),
        ("spaces-and-all-vowels", " aeiou AEIOU "),
        ("normal-example", "This is a message"),
        ("ascii-domain", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "),
    ]

    mismatch_count = 0
    for name, message in cases:
        command = [
            "krun",
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cMESSAGE={json.dumps(message)}",
        ]
        print("COMMAND: " + shlex.join(command))
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        print(f"KRUN_EXIT_STATUS: {completed.returncode}")
        match = RESULT_RE.search(completed.stdout)
        if completed.returncode != 0 or match is None:
            print(f"CASE {name}: unable to extract returned pyStr")
            print("STDOUT_PREFIX: " + completed.stdout[:1000].replace("\n", "\\n"))
            print("STDERR_PREFIX: " + completed.stderr[:1000].replace("\n", "\\n"))
            mismatch_count += 1
            continue
        k_result = json.loads(match.group(1))
        canonical_result = trusted_encode(message)
        python_result = python_encode(message)
        matches = k_result == canonical_result == python_result
        print(
            "CASE "
            + json.dumps(
                {
                    "name": name,
                    "input": message,
                    "k": k_result,
                    "trusted_python": canonical_result,
                    "candidate_python": python_result,
                    "all_equal": matches,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        if not matches:
            mismatch_count += 1

    print(f"case_count={len(cases)}")
    print(f"mismatch_count={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
