#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with candidate Python."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shlex
import subprocess


BUILD = Path("/tmp/audit-work/clean-build")
DEFINITION = BUILD / "semantic-haskell-kompiled"
PROGRAM = BUILD / "solution.mpy"


def load_solution():
    path = BUILD / "solution.py"
    spec = importlib.util.spec_from_file_location("scratch_solution", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def words_term(words: list[str]) -> str:
    result = "nil"
    for word in reversed(words):
        result = f"cons({json.dumps(word, ensure_ascii=False)}, {result})"
    return result


def main() -> int:
    solution = load_solution()
    cases = [
        ("prompt-1", ["name", "of", "string"]),
        ("empty", []),
        ("singleton-empty-word", [""]),
        ("greater-first", ["abcd", "a"]),
        ("greater-later", ["a", "abcd"]),
        ("tie-replace", ["ba", "ab"]),
        ("tie-no-replace", ["ab", "ba"]),
        ("repeated-chars", ["aaaaaaa", "bb", "cc"]),
        ("combining", ["é", "e\u0301"]),
        ("unicode", ["😀a", "東京", "λλ"]),
    ]
    failures = 0
    for label, words in cases:
        expected = solution.find_max(list(words))
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            "-cINPUT=" + words_term(words),
            "--pattern",
            f"<result> result(strVal({json.dumps(expected, ensure_ascii=False)})) </result>",
            "--output",
            "pretty",
        ]
        print(f"CASE={label} WORDS={words!r} PYTHON_RESULT={expected!r}")
        print("COMMAND=" + shlex.join(command))
        completed = subprocess.run(command, cwd=BUILD, text=True, capture_output=True)
        print(f"EXIT_STATUS={completed.returncode}")
        print("STDOUT_BEGIN")
        print(completed.stdout, end="")
        print("STDOUT_END")
        if completed.stderr:
            print("STDERR_BEGIN")
            print(completed.stderr, end="")
            print("STDERR_END")
        if completed.returncode != 0 or "#Top" not in completed.stdout:
            failures += 1
    print(f"case_count={len(cases)} failures={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
