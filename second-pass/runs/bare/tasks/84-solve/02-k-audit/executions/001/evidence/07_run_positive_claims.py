#!/usr/bin/env python3
"""Run every target claim independently and preserve one bounded log per claim."""

from __future__ import annotations

import concurrent.futures
import pathlib
import shlex
import subprocess


CLAIMS = [
    "SPEC.inputs-00000-00999",
    "SPEC.inputs-01000-01999",
    "SPEC.inputs-02000-02999",
    "SPEC.inputs-03000-03999",
    "SPEC.inputs-04000-04999",
    "SPEC.inputs-05000-05999",
    "SPEC.inputs-06000-06999",
    "SPEC.inputs-07000-07999",
    "SPEC.inputs-08000-08999",
    "SPEC.inputs-09000-09999",
    "SPEC.input-10000",
]
WORK = pathlib.Path("/tmp/audit-work/src")
DEFINITION = pathlib.Path("/tmp/audit-work/proof-kompiled")
LOG_DIR = pathlib.Path("/audit-output/evidence/positive-claims")


def run_claim(claim: str) -> tuple[str, int, bool, pathlib.Path]:
    command = [
        "/usr/bin/kprove",
        "spec.k",
        "--definition",
        str(DEFINITION),
        "--spec-module",
        "SPEC",
        "--claims",
        claim,
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        capture_output=True,
        check=False,
    )
    top = any(line.strip() == "#Top" for line in completed.stdout.splitlines())
    log_path = LOG_DIR / f"{claim.replace('.', '__')}.log"
    body = "\n".join(
        [
            f"$ cd {shlex.quote(str(WORK))}",
            f"$ {shlex.join(command)}",
            f"[exit {completed.returncode}]",
            f"[stdout has exact #Top line: {top}]",
            "--- stdout ---",
            completed.stdout.rstrip(),
            "--- stderr ---",
            completed.stderr.rstrip(),
            "",
        ]
    )
    log_path.write_text(body, encoding="utf-8")
    return claim, completed.returncode, top, log_path


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run_claim, claim) for claim in CLAIMS]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"claim={result[0]} exit={result[1]} top={result[2]} "
                f"log={result[3]}"
            )
    by_claim = {result[0]: result for result in results}
    failures = [
        claim
        for claim in CLAIMS
        if by_claim[claim][1] != 0 or not by_claim[claim][2]
    ]
    print(f"claims_run={len(CLAIMS)}")
    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
