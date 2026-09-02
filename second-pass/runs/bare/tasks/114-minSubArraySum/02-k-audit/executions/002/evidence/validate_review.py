#!/usr/bin/env python3
"""Final structural validation of the audit report and preserved evidence."""

from __future__ import annotations

import re
from pathlib import Path


def main() -> int:
    root = Path("/audit-output")
    review = root / "REVIEW.md"
    text = review.read_text(encoding="utf-8")
    lines = text.splitlines()
    failures: list[str] = []

    expected_tail = ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
    if lines[-2:] != expected_tail:
        failures.append(f"bad verdict tail: {lines[-2:]!r}")

    for stage in range(1, 8):
        if f"## {stage}." not in text:
            failures.append(f"missing stage {stage}")

    links = re.findall(r"\]\((evidence/[^)]+)\)", text)
    missing = [link for link in links if not (root / link).is_file()]
    if missing:
        failures.append(f"missing linked evidence: {missing!r}")

    logs = sorted((root / "evidence").glob("*.log"))
    malformed_logs = [
        str(log.name)
        for log in logs
        if "--- RESULT ---" not in log.read_text(encoding="utf-8", errors="replace")
    ]
    if malformed_logs:
        failures.append(f"logs without result trailers: {malformed_logs!r}")

    inventory = (root / "evidence" / "RULE-INVENTORY.md").read_text(encoding="utf-8")
    missing_rules = [
        f"R{number:02d}" for number in range(1, 46) if f"| R{number:02d} |" not in inventory
    ]
    missing_verification = [
        f"V{number:02d}" for number in range(1, 7) if f"| V{number:02d} |" not in inventory
    ]
    if missing_rules or missing_verification:
        failures.append(
            f"incomplete rule inventory: semantic={missing_rules}, verification={missing_verification}"
        )

    if (
        (root / "evidence" / "spec-vacuity.k").read_bytes()
        != Path("/tmp/audit-work/source/spec-vacuity.k").read_bytes()
    ):
        failures.append("preserved vacuity mutation differs from executed mutation")

    print(f"review_lines={len(lines)}")
    print(f"linked_evidence_count={len(links)}")
    print(f"command_log_count={len(logs)}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"failure={failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
