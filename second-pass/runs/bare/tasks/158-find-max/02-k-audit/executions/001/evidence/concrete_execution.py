#!/usr/bin/env python3
"""Execute the freshly rebuilt generated semantics and compare with Python."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


SOURCE = Path("/tmp/audit-work/source")
DEFINITION = Path(
    "/tmp/audit-work/reconstruction/semantics-haskell-kompiled"
)
PROGRAM = SOURCE / "solution.mpy"
INPUTS_FILE = Path("/audit-output/evidence/concrete-inputs.jsonl")

CASES = [
    ("prompt-1", ["name", "of", "string"]),
    ("prompt-2", ["name", "enam", "game"]),
    ("prompt-3", ["aaaaaaa", "bb", "cc"]),
    ("empty-list-boundary", []),
    ("singleton-empty-string", [""]),
    ("greater-count-replaces", ["aa", "abc"]),
    ("smaller-count-retains", ["abc", "aa"]),
    ("equal-count-lex-smaller-replaces", ["ba", "ab"]),
    ("equal-count-lex-larger-retains", ["ab", "ba"]),
    ("unicode-distinct-count", ["é", "e\u0301", "😀😀a"]),
    ("unicode-lex-tie", ["éa", "êa", "😀a"]),
]


def load_entry(module_name: str, path: Path) -> Callable[[list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_max


def outcome(function: Callable[[list[str]], str], words: list[str]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(list(words))}
    except Exception as error:
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


def k_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def k_words(words: list[str]) -> str:
    term = "nil"
    for word in reversed(words):
        term = f"cons({k_string(word)}, {term})"
    return term


def main() -> int:
    generated = load_entry("generated_concrete_oracle", SOURCE / "solution.py")
    canonical = load_entry("canonical_concrete_oracle", SOURCE / "canonical.py")
    mismatches = 0
    with INPUTS_FILE.open("w", encoding="utf-8") as evidence:
        for label, words in CASES:
            python_result = outcome(generated, words)
            canonical_result = outcome(canonical, words)
            if python_result["kind"] != "return":
                raise RuntimeError(f"generated Python raised for {label}: {python_result}")
            expected = python_result["value"]
            command = [
                "krun",
                str(PROGRAM),
                "--definition",
                str(DEFINITION),
                f"-cINPUT={k_words(words)}",
                "--pattern",
                f"<result> result(strVal({k_string(expected)})) </result>",
                "--output",
                "pretty",
            ]
            print("$ " + shlex.join(command))
            completed = subprocess.run(
                command,
                cwd=SOURCE,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            print(completed.stdout.rstrip())
            matched = completed.returncode == 0 and completed.stdout.strip() != "#Bottom"
            print(f"EXIT_STATUS: {completed.returncode}")
            print(
                f"CASE: {label} PYTHON: {python_result} "
                f"CANONICAL: {canonical_result} K_MATCHED: {matched}"
            )
            evidence.write(
                json.dumps(
                    {
                        "label": label,
                        "words": words,
                        "python": python_result,
                        "canonical": canonical_result,
                        "k_input": k_words(words),
                        "k_expected_pattern": command[-3],
                        "k_exit_status": completed.returncode,
                        "k_output": completed.stdout.strip(),
                        "matched": matched,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )
            if not matched:
                mismatches += 1
    print(f"cases={len(CASES)}")
    print(f"k_python_mismatches={mismatches}")
    print(f"inputs_file={INPUTS_FILE}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
