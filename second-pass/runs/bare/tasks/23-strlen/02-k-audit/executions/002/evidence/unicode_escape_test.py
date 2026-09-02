#!/usr/bin/env python3
"""Ground K string-escape witnesses beyond Latin-1."""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/23-strlen.30KKVy/work")


def main() -> None:
    cases = [
        ("U+0100", "Ā", r'"\u0100"'),
        ("U+1F600", "😀", r'"\U0001F600"'),
    ]
    failures = 0
    for label, python_value, k_literal in cases:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "verification-kompiled",
            f"-cINPUT={k_literal}",
        ]
        print(f"COMMAND {shlex.join(command)}")
        result = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(f"KRUN_EXIT={result.returncode}")
        print(result.stdout.rstrip())
        match = re.search(
            r"<result>\s*Int\s*\(\s*([0-9]+)\s*\)\s*</result>",
            result.stdout,
        )
        observed = int(match.group(1)) if match else None
        expected = len(python_value)
        print(
            f"WITNESS {label} python_value={python_value!r} "
            f"python_len={expected} k_lengthString={observed}"
        )
        if result.returncode != 0 or observed == expected:
            # This test succeeds only when it reproduces the known mismatch.
            failures += 1
    print(f"EXPECTED_MISMATCHES={len(cases) - failures}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
