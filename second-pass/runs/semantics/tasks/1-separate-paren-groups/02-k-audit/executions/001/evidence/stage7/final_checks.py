#!/usr/bin/env python3
"""Mechanical consistency checks for the completed audit package."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path("/audit-output")
REVIEW = ROOT / "REVIEW.md"


def main() -> int:
    failures: list[str] = []

    review_text = REVIEW.read_text(encoding="utf-8")
    expected_footer = "VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n"
    if not review_text.endswith(expected_footer):
        failures.append("REVIEW.md does not end with the exact expected footer")
    markers = re.findall(r"^(?:VERDICT|LEGITIMACY):.*$", review_text, re.MULTILINE)
    if markers != ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]:
        failures.append(f"unexpected verdict markers: {markers!r}")

    cited = sorted(set(re.findall(r"`(evidence/[^`]+)`", review_text)))
    for relative in cited:
        if not (ROOT / relative).exists():
            failures.append(f"missing cited evidence path: {relative}")

    for script in sorted((ROOT / "evidence").rglob("*.py")):
        try:
            ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
        except SyntaxError as error:
            failures.append(f"Python syntax error in {script}: {error}")

    for data_file in (
        ROOT / "evidence/stage2/differential-inputs.jsonl",
        ROOT / "evidence/stage5/k-inventory.jsonl",
        ROOT / "evidence/stage5/k-dispositions.jsonl",
    ):
        try:
            with data_file.open(encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, start=1):
                    json.loads(line)
        except Exception as error:  # report exact malformed artifact
            failures.append(f"JSONL error in {data_file}:{line_number}: {error}")

    positive_logs = [
        "prove-all-balanced-inputs.log",
        "prove-all-balanced-calls.log",
        "prove-empty.log",
        "prove-prompt-example.log",
        "prove-adjacent-and-spaced.log",
        "prove-deep-nesting.log",
        "prove-entry-and-examples-combined.log",
    ]
    for name in positive_logs:
        text = (ROOT / "evidence/stage3" / name).read_text(encoding="utf-8")
        if "\n#Top\n" not in text or not text.endswith("EXIT_STATUS=0\n"):
            failures.append(f"positive proof signal missing from {name}")

    mutation = (ROOT / "evidence/stage6/vacuity-proof.log").read_text(encoding="utf-8")
    if "WarnStuckClaimState" not in mutation or not mutation.endswith(
        "KPROVE_EXIT_STATUS=1\n"
    ):
        failures.append("mutation log lacks the expected stuck-claim/exit-1 signal")

    print(f"cited_evidence_path_count={len(cited)}")
    print(f"python_script_count={len(list((ROOT / 'evidence').rglob('*.py')))}")
    print(f"positive_proof_log_count={len(positive_logs)}")
    print(f"failure_count={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
