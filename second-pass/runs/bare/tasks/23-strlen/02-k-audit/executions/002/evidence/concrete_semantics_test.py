#!/usr/bin/env python3
"""Run the rebuilt generated semantics and compare each result with Python."""

from __future__ import annotations

import json
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/23-strlen.30KKVy/work")
DEFINITION = WORK / "semantic-kompiled"
PROGRAM = WORK / "solution.mpy"


def main() -> None:
    cases = [
        "",
        "a",
        "abc",
        "\n",
        "\"'\\",
        "é",
        "e\u0301",
        "😀",
        "a😀é",
        "👩\u200d💻",
        "a" * 257,
    ]
    mismatches = 0
    for index, value in enumerate(cases):
        config_value = json.dumps(value, ensure_ascii=False)
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={config_value}",
        ]
        print(f"COMMAND[{index}] {shlex.join(command)}")
        result = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(f"EXIT[{index}] {result.returncode}")
        print(result.stdout.rstrip())
        match = re.search(
            r"<result>\s*Int\s*\(\s*(-?[0-9]+)\s*\)\s*</result>",
            result.stdout,
            re.MULTILINE,
        )
        expected = len(value)
        observed = int(match.group(1)) if match else None
        print(
            f"COMPARE[{index}] input={value!r} "
            f"python={expected} k={observed}"
        )
        if result.returncode != 0 or observed != expected:
            mismatches += 1
    print(f"TOTAL_CASES={len(cases)} MISMATCHES={mismatches}")
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
