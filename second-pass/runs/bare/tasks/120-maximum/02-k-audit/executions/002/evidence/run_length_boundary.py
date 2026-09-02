#!/usr/bin/env python3
"""Execute the 1,000-element boundary harness and summarize its final state."""

from __future__ import annotations

import hashlib
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/120-maximum/candidate")
PROGRAM = Path("/audit-output/evidence/boundary1000.mpy")


def main() -> None:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        "boundary-harness-kompiled",
        "-cARGS=.List",
    ]
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    print(f"exit={completed.returncode}")
    print(f"stdout_sha256={hashlib.sha256(completed.stdout.encode()).hexdigest()}")
    if completed.returncode != 0:
        print(completed.stdout[-4000:])
        raise SystemExit(completed.returncode)
    out_match = re.search(r"<out>\s*listVal\s*\((.*?)\)\s*</out>", completed.stdout, re.DOTALL)
    env_match = re.search(r'"arr"\s*\|->\s*listVal\s*\((.*?)\)\s*"k"\s*\|->', completed.stdout, re.DOTALL)
    if out_match is None or env_match is None:
        print(completed.stdout[-4000:])
        raise SystemExit("could not identify final out/env cells")
    out_values = [int(value) for value in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", out_match.group(1))]
    env_values = [int(value) for value in re.findall(r"ListItem\s*\(\s*(-?\d+)\s*\)", env_match.group(1))]
    expected = [0, 0, 0]
    print(f"final_env_arr_length={len(env_values)}")
    print(f"final_output={out_values}")
    print(f"expected_python_output={expected}")
    print(f"match={len(env_values) == 1000 and out_values == expected}")
    if len(env_values) != 1000 or out_values != expected:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
