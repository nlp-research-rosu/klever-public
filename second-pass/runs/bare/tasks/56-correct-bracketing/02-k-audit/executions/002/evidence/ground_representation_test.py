#!/usr/bin/env python3
"""Ground fixed-string versus proof-surrogate operational comparison."""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path


def run(command: list[str]) -> tuple[int, bool | None, str]:
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command, check=False, capture_output=True, text=True
    )
    combined = completed.stdout + completed.stderr
    match = re.search(
        r"result\s*\(\s*BVal\s*\(\s*(true|false)\s*\)\s*\)", combined
    )
    value = None if match is None else match.group(1) == "true"
    return completed.returncode, value, combined


def main() -> None:
    root = Path("/tmp/audit-work/proof")
    definition = root / "seq-test-llvm-kompiled"
    cases = [
        ("", root / "seq-empty.mpy"),
        ("<>", root / "seq-pair.mpy"),
        (">", root / "seq-close.mpy"),
    ]
    mismatches = 0
    for real_string, surrogate_program in cases:
        escaped = real_string.replace("\\", "\\\\").replace('"', '\\"')
        actual_command = [
            "krun",
            str(root / "solution.mpy"),
            "--definition",
            str(definition),
            f'-cINPUT="{escaped}"',
        ]
        seq_command = [
            "krun",
            str(surrogate_program),
            "--definition",
            str(definition),
            '-cINPUT=""',
        ]
        actual_exit, actual, actual_output = run(actual_command)
        seq_exit, seq, seq_output = run(seq_command)
        ok = actual_exit == 0 and seq_exit == 0 and actual == seq
        print(
            f"GROUND_BRIDGE input={real_string!r} actual={actual!r} "
            f"surrogate={seq!r} actual_exit={actual_exit} "
            f"surrogate_exit={seq_exit} match={ok}"
        )
        if not ok:
            mismatches += 1
            print(actual_output[:4000])
            print(seq_output[:4000])
    print(f"GROUND_BRIDGE_MISMATCHES count={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
