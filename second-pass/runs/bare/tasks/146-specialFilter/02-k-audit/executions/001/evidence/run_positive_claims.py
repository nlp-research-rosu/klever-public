#!/usr/bin/env python3
"""Run all split positive claims and preserve one bounded log per claim."""

from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import shlex
import subprocess


ROOT = Path("/tmp/audit-work/146-specialFilter")
SPECS = ROOT / "positive-claims"
DEFINITION = ROOT / "candidate/fresh-verification-kompiled"
LOGS = Path("/audit-output/evidence/positive-claims")
LIMIT = 240_000


def main() -> int:
    LOGS.mkdir(parents=True, exist_ok=True)
    results = []
    for spec in sorted(SPECS.glob("claim-*.k")):
        ordinal = spec.stem.removeprefix("claim-")
        module = f"AUDIT-SPEC-{ordinal}"
        command = [
            "kprove",
            str(spec),
            "--definition",
            str(DEFINITION),
            "--spec-module",
            module,
        ]
        started = datetime.now(timezone.utc)
        completed = subprocess.run(
            command,
            cwd=ROOT / "candidate",
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        )
        output = completed.stdout
        truncated = len(output.encode("utf-8")) > LIMIT
        if truncated:
            output = output.encode("utf-8")[:LIMIT].decode("utf-8", errors="replace")
            output += "\n[LOG TRUNCATED AT 240000 BYTES]\n"
        top = output.strip() == "#Top"
        log = LOGS / f"claim-{ordinal}.log"
        log.write_text(
            "\n".join(
                [
                    f"started_utc: {started.isoformat()}",
                    f"cwd: {ROOT / 'candidate'}",
                    f"command: {shlex.join(command)}",
                    f"exit_status: {completed.returncode}",
                    f"finished_utc: {datetime.now(timezone.utc).isoformat()}",
                    f"output_truncated: {'yes' if truncated else 'no'}",
                    f"exact_top: {'yes' if top else 'no'}",
                    "--- output ---",
                    output,
                ]
            ),
            encoding="utf-8",
        )
        results.append((ordinal, completed.returncode, top, log))
        print(
            f"claim={ordinal} exit_status={completed.returncode} "
            f"exact_top={'yes' if top else 'no'} log={log}"
        )
    successes = sum(status == 0 and top for _, status, top, _ in results)
    print(f"successful_claims={successes}/{len(results)}")
    return 0 if successes == len(results) and results else 1


if __name__ == "__main__":
    raise SystemExit(main())
