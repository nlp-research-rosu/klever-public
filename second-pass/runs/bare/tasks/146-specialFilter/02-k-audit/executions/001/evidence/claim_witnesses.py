#!/usr/bin/env python3
"""Ground every submitted entry claim with a satisfiable witness and compare."""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import subprocess


ROOT = Path("/tmp/audit-work/146-specialFilter")
OUT = ROOT / "claim-witnesses"
LOGS = Path("/audit-output/evidence/claim-witnesses")
DEFINITION = ROOT / "candidate/fresh-verification-kompiled"

WITNESSES = [
    (1, [15, -73, 14, -15], 1, True, "ground prompt example 1"),
    (2, [33, -2, -3, 45, 21, 109], 2, True, "ground prompt example 2"),
    (3, [], 0, True, "ground empty list"),
    (4, [-999, -11, 0, 1, 9, 10], 0, True, "ground threshold list"),
    (
        5,
        [11, 12, 21, 22, 313, 314, 423, 424, 50005, 70008, 80007, 90009],
        4,
        True,
        "ground parity/width list",
    ),
    (6, [15, 15, 15, 20, 20], 3, True, "ground repetition list"),
    (7, [10], 0, 10 <= 10, "N=10 satisfies N<=10"),
    (8, [11], 1, 11 <= 11 <= 99 and 11 % 2 == 1 and (11 // 10) % 2 == 1,
     "N=11 satisfies two-digit positive guard"),
    (9, [12], 0, 11 <= 12 <= 99 and not (12 % 2 == 1 and (12 // 10) % 2 == 1),
     "N=12 satisfies two-digit negative guard"),
    (10, [101], 1, 100 <= 101 <= 999 and 101 % 2 == 1 and (101 // 100) % 2 == 1,
     "N=101 satisfies three-digit positive guard"),
    (11, [100], 0, 100 <= 100 <= 999 and not (100 % 2 == 1 and (100 // 100) % 2 == 1),
     "N=100 satisfies three-digit negative guard"),
]


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.specialFilter


def expression(nums: list[int]) -> str:
    if not nums:
        return "ListExpr()"
    return "ListExpr(" + ", ".join(f"Int({value})" for value in nums) + ")"


def main() -> int:
    canonical = load_function(ROOT / "reference/canonical.py", "canonical_claim_witness")
    candidate = load_function(ROOT / "candidate/solution.py", "candidate_claim_witness")
    OUT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    failures = []
    for ordinal, nums, claimed, satisfies, reason in WITNESSES:
        program = OUT / f"claim-{ordinal:02d}.mpy"
        program.write_text(f"SFTest({expression(nums)})\n", encoding="utf-8")
        command = ["krun", str(program), "--definition", str(DEFINITION)]
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
        match = re.search(r"<k>\s*intVal \( (-?\d+) \) ~> \.K\s*</k>", completed.stdout)
        k_value = int(match.group(1)) if match else None
        canonical_value = canonical(list(nums))
        candidate_value = candidate(list(nums))
        ok = (
            satisfies
            and completed.returncode == 0
            and claimed == k_value == canonical_value == candidate_value
        )
        log = LOGS / f"claim-{ordinal:02d}.log"
        log.write_text(
            "\n".join(
                [
                    f"started_utc: {started.isoformat()}",
                    f"cwd: {ROOT / 'candidate'}",
                    f"command: {shlex.join(command)}",
                    f"exit_status: {completed.returncode}",
                    f"finished_utc: {datetime.now(timezone.utc).isoformat()}",
                    f"input: {json.dumps(nums)}",
                    f"precondition_witness: {reason}",
                    f"precondition_satisfied: {'yes' if satisfies else 'no'}",
                    f"claimed_result: {claimed}",
                    f"canonical_python: {canonical_value}",
                    f"candidate_python: {candidate_value}",
                    f"k_result: {k_value}",
                    f"all_equal: {'yes' if ok else 'no'}",
                    "--- output ---",
                    completed.stdout,
                ]
            ),
            encoding="utf-8",
        )
        print(
            f"claim={ordinal:02d} input={json.dumps(nums)} precondition={'yes' if satisfies else 'no'} "
            f"claimed={claimed} canonical={canonical_value} candidate={candidate_value} "
            f"k={k_value} all_equal={'yes' if ok else 'no'} log={log}"
        )
        if not ok:
            failures.append(ordinal)
    print(f"successful_witnesses={len(WITNESSES) - len(failures)}/{len(WITNESSES)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
