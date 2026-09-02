#!/usr/bin/env python3
"""Probe K String/set behavior at escapes and code points outside Latin-1."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")

# Python values and independently written K String tokens. Keeping K tokens as
# ASCII permits testing lone surrogate code points without putting a surrogate
# in an OS process argument.
CASES = [
    ("\u0100", "\u0100\u0100", r'"\u0100"', r'"\u0100\u0100"'),
    ("\U0001f600", "\U0001f600\U0001f600",
     r'"\U0001F600"', r'"\U0001F600\U0001F600"'),
    ("\U0001f600", "\U0001f601", r'"\U0001F600"', r'"\U0001F601"'),
    ("\U0010ffff", "\U0010ffff\U0010ffff",
     r'"\U0010FFFF"', r'"\U0010FFFF\U0010FFFF"'),
    ("\ud800", "\ud800\ud800", r'"\uD800"', r'"\uD800\uD800"'),
    ("\ud800", "\ud801", r'"\uD800"', r'"\uD801"'),
    ("\x00", "\x00\x00", r'"\x00"', r'"\x00\x00"'),
    ("\\", "\\\\", r'"\\"', r'"\\\\"'),
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    oracle = load(
        Path("/tmp/audit-work/trusted/canonical.py"), "trusted_unicode_oracle"
    ).same_chars
    mismatches = []
    unsupported = []
    for index, (left, right, k_left, k_right) in enumerate(CASES, start=1):
        command = [
            "krun",
            str(WORK / "solution.mpy"),
            "--definition",
            str(WORK / "semantic-kompiled"),
            f"-cS0={k_left}",
            f"-cS1={k_right}",
        ]
        print(
            f"CASE={index} PYTHON_INPUT={left!r},{right!r} "
            f"K_INPUT={k_left},{k_right}"
        )
        print(f"+ {shlex.join(command)}")
        completed = subprocess.run(command, text=True, capture_output=True)
        output = completed.stdout + completed.stderr
        match = re.search(r"result\s*\(\s*boolValue\s*\(\s*(true|false)", output)
        observed = None if match is None else match.group(1) == "true"
        expected = oracle(left, right)
        print(
            f"EXIT_STATUS={completed.returncode} "
            f"K_RESULT={observed!r} PYTHON_RESULT={expected!r}"
        )
        if completed.returncode != 0 or observed is None:
            unsupported.append((index, left, right, completed.returncode))
            print("K_OUTPUT_BEGIN")
            print(output.rstrip())
            print("K_OUTPUT_END")
        elif observed != expected:
            mismatches.append((index, left, right, observed, expected))

    print(f"cases={len(CASES)}")
    print(f"mismatches={len(mismatches)}")
    print(f"unsupported={len(unsupported)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
    if unsupported:
        print(f"first_unsupported={unsupported[0]!r}")
    # Unsupported cases are reported as adequacy evidence, not a harness error.
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
