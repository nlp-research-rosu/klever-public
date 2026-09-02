#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare with both Pythons."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_k(words: list[str]) -> str:
    result = ".Words"
    for word in reversed(words):
        result = f"WCons({json.dumps(word)},{result})"
    return f"pyList({result})"


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    root = Path("/tmp/audit-work/fresh")
    canonical = load_module("trusted_canonical_k", root / "trusted/canonical.py")
    candidate = load_module("submitted_solution_k", root / "solution.py")
    cases = [
        ("Mary had a little lamb", 4, "normal prompt case"),
        ("", 0, "empty string and zero"),
        ("", 1, "empty string and positive n"),
        ("     ", 0, "only spaces"),
        ("  a  b  ", 0, "leading/trailing/repeated spaces, vowel branch"),
        ("  a  b  ", 1, "leading/trailing/repeated spaces, consonant branch"),
        ("aeiou AEIOU", 0, "lowercase and uppercase vowel branches"),
        ("bcdfg XYZ", 3, "filter false then true"),
        ("a bb ccc dddd", 2, "middle result preserves order"),
    ]
    failures = 0
    for index, (s, n, purpose) in enumerate(cases, 1):
        canonical_result = canonical.select_words(s, n)
        candidate_result = candidate.select_words(s, n)
        expected = expected_k(canonical_result)
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "semantic-kompiled",
            f"-cS={json.dumps(s)}",
            f"-cN={n}",
        ]
        print(f"CASE {index}: {purpose}")
        print(f"COMMAND: {shlex.join(command)}")
        completed = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"EXIT: {completed.returncode}")
        print(completed.stdout.rstrip())
        print(f"CANONICAL: {canonical_result!r}")
        print(f"CANDIDATE: {candidate_result!r}")
        print(f"EXPECTED_K_COMPACT: {expected}")
        observed = compact(completed.stdout)
        matched = (
            completed.returncode == 0
            and canonical_result == candidate_result
            and expected in observed
            and "<k>.K</k>" in observed
        )
        print(f"MATCH: {matched}")
        if not matched:
            failures += 1
    print(f"concrete_cases={len(cases)}")
    print(f"concrete_failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
