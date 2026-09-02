#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def parse_k_result(stdout: str) -> str:
    k_cell_match = re.search(r"<k>\s*(.*?)\s*</k>", stdout, re.DOTALL)
    if not k_cell_match:
        raise ValueError("no <k> cell in krun output")
    k_cell = " ".join(k_cell_match.group(1).split())
    if re.fullmatch(r"pyStr \( \.Chars \) ~> \.K", k_cell):
        return ""
    vowel = re.fullmatch(
        r"pyStr \( snoc \( \.Chars , vow \( v_([aeiouAEIOU]) \) \) \) ~> \.K",
        k_cell,
    )
    if vowel:
        return vowel.group(1)
    raise ValueError(f"unexpected final <k> cell: {k_cell}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-out", required=True, type=Path)
    args = parser.parse_args()

    canonical = load_entry("trusted_canonical_kdiff", Path("/reference/canonical.py"))
    candidate = load_entry(
        "scratch_candidate_kdiff", Path("/tmp/audit-work/candidate-src/solution.py")
    )

    inputs = [
        "",
        "a",
        "Z",
        "ab",
        "aba",
        "bAb",
        "abb",
        "aab",
        "baa",
        "bbb",
        "cabd",
        "zaBcd",
        "baeb",
        "xUyz",
        "AEIOU",
        "BCDFG",
        "yogurt",
        "FULL",
        "quick",
        "rhythm",
        "trIple",
        "baXaeiob",
    ]
    args.inputs_out.write_text(json.dumps(inputs, indent=2) + "\n", encoding="utf-8")

    workdir = Path("/tmp/audit-work/build-concrete")
    mismatches = []
    for word in inputs:
        command = [
            "krun",
            "solution.fresh.mpy",
            f'-cARG=word("{word}")',
            "--definition",
            "concrete-kompiled",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=workdir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        print(f"COMMAND: (cd {workdir} && {shlex.join(command)})")
        print(f"EXIT_STATUS: {completed.returncode}")
        if completed.returncode != 0:
            print(f"STDOUT: {completed.stdout[-1000:]}")
            print(f"STDERR: {completed.stderr[-1000:]}")
            mismatches.append({"word": word, "krun_exit": completed.returncode})
            continue
        try:
            k_value = parse_k_result(completed.stdout)
        except ValueError as error:
            print(f"PARSE_ERROR: {error}")
            mismatches.append({"word": word, "parse_error": str(error)})
            continue
        canonical_value = canonical(word)
        candidate_value = candidate(word)
        print(
            f"RESULT: input={word!r} k={k_value!r} "
            f"canonical={canonical_value!r} candidate={candidate_value!r}"
        )
        if k_value != canonical_value or k_value != candidate_value:
            mismatches.append(
                {
                    "word": word,
                    "k": k_value,
                    "canonical": canonical_value,
                    "candidate": candidate_value,
                }
            )
    print(f"TOTAL_INPUTS: {len(inputs)}")
    print(f"MISMATCHES: {len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
