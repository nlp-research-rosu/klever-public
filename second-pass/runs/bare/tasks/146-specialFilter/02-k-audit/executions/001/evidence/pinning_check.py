#!/usr/bin/env python3
"""Compare SFTest's expanded Run term with the freshly translated program Run term."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from pathlib import Path
import re
import shlex
import subprocess


ROOT = Path("/tmp/audit-work/146-specialFilter")
DEFINITION = ROOT / "candidate/fresh-verification-kompiled"
DIRECT = ROOT / "concrete-inputs/prompt1.mpy"
WRAPPED = ROOT / "candidate/example1.mpy"
LOG = Path("/audit-output/evidence/stage4-pinning-detail.log")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT / "candidate",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )


def balanced_run(output: str) -> str:
    start = output.index("Run (")
    depth = 0
    opened = False
    for index in range(start, len(output)):
        char = output[index]
        if char == "(":
            depth += 1
            opened = True
        elif char == ")":
            depth -= 1
            if opened and depth == 0:
                return output[start : index + 1]
    raise ValueError("unbalanced Run term")


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


def main() -> int:
    direct_command = [
        "krun",
        str(DIRECT),
        "--definition",
        str(DEFINITION),
        "--depth",
        "0",
    ]
    wrapper_command = [
        "krun",
        str(WRAPPED),
        "--definition",
        str(DEFINITION),
        "--depth",
        "1",
    ]
    started = datetime.now(timezone.utc)
    direct = run(direct_command)
    wrapper = run(wrapper_command)
    direct_term = normalize(balanced_run(direct.stdout))
    wrapper_term = normalize(balanced_run(wrapper.stdout))
    same = direct_term == wrapper_term
    direct_digest = hashlib.sha256(direct_term.encode()).hexdigest()
    wrapper_digest = hashlib.sha256(wrapper_term.encode()).hexdigest()
    LOG.write_text(
        "\n".join(
            [
                f"started_utc: {started.isoformat()}",
                f"cwd: {ROOT / 'candidate'}",
                f"direct_command: {shlex.join(direct_command)}",
                f"direct_exit_status: {direct.returncode}",
                f"wrapper_command: {shlex.join(wrapper_command)}",
                f"wrapper_exit_status: {wrapper.returncode}",
                f"finished_utc: {datetime.now(timezone.utc).isoformat()}",
                f"direct_normalized_run_sha256: {direct_digest}",
                f"wrapper_normalized_run_sha256: {wrapper_digest}",
                f"terms_identical: {'yes' if same else 'no'}",
                "--- direct output ---",
                direct.stdout,
                "--- wrapper output ---",
                wrapper.stdout,
            ]
        ),
        encoding="utf-8",
    )
    print(f"direct_exit_status={direct.returncode}")
    print(f"wrapper_exit_status={wrapper.returncode}")
    print(f"direct_normalized_run_sha256={direct_digest}")
    print(f"wrapper_normalized_run_sha256={wrapper_digest}")
    print(f"terms_identical={'yes' if same else 'no'}")
    print(f"log={LOG}")
    return 0 if direct.returncode == wrapper.returncode == 0 and same else 1


if __name__ == "__main__":
    raise SystemExit(main())
