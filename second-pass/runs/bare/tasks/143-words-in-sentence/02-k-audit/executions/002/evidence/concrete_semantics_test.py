#!/usr/bin/env python3
"""Run the fresh generated K semantics and compare results with both Python programs."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path


DEFINITION = Path("/tmp/audit-work/clean/build/semantic-haskell-kompiled")
PROGRAM = Path("/tmp/audit-work/clean/candidate/solution.mpy")
CANONICAL = Path("/tmp/audit-work/clean/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/clean/candidate/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_in_sentence


def parse_result(output: str) -> str:
    match = re.search(
        r"<result>\s*Str\s*\(\s*(\"(?:\\\\.|[^\"\\\\])*\")\s*\)\s*</result>",
        output,
        re.DOTALL,
    )
    if match is None:
        raise RuntimeError(f"could not parse result cell from:\n{output}")
    return json.loads(match.group(1))


def main() -> int:
    canonical = load_entry(CANONICAL, "trusted_concrete_oracle")
    candidate = load_entry(CANDIDATE, "candidate_concrete_oracle")
    cases = [
        ("documented-one", "This is a test"),
        ("documented-two", "lets go for swimming"),
        ("empty-boundary", ""),
        ("length-one", "a"),
        ("prime-two", "aa"),
        ("composite-four", "aaaa"),
        ("both-result-branches", "aa aaa"),
        ("no-selected-word", "a aaaa"),
        ("length-100-prime-pair", "aa " + "a" * 97),
        ("length-100-composite", "a" * 100),
        ("repeated-space-observation", "aa  aaa"),
        # Greek lambda is a Unicode letter. Python len("λλλ") is 3, while the
        # K String backend used here counts its UTF-8 bytes and sees 6.
        ("unicode-greek-three", "λλλ"),
    ]
    failures = []
    for label, sentence in cases:
        encoded = json.dumps(sentence, ensure_ascii=False)
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cSENTENCE={encoded}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        print(f"CASE {label} input={sentence!r} length={len(sentence)}")
        print(f"COMMAND {shlex.join(command)}")
        print(f"EXIT {completed.returncode}")
        if completed.stderr:
            print(f"STDERR {completed.stderr.strip()}")
        try:
            k_result = parse_result(completed.stdout)
        except RuntimeError as error:
            k_result = None
            print(str(error))
        canonical_result = canonical(sentence)
        candidate_result = candidate(sentence)
        print(
            f"RESULT k={k_result!r} canonical={canonical_result!r} "
            f"candidate={candidate_result!r}"
        )
        matches = (
            completed.returncode == 0
            and k_result == canonical_result
            and k_result == candidate_result
        )
        print(f"MATCH {matches}")
        if not matches:
            failures.append(label)
    print(f"case_count={len(cases)} failure_count={len(failures)} failures={failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
