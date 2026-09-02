#!/usr/bin/env python3
"""Self-check required audit logs and terminal REVIEW.md markers."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"

success_logs = [
    "01-semantics-integrity.log",
    "02-trusted-source-identity.log",
    "04-translation-identity.log",
    "05-differential.log",
    "07-build-concrete.log",
    "08-build-verification-base.log",
    "09-build-verification-body.log",
    "10-build-verification-full.log",
    "11-prove-connection-initial.log",
    "12-prove-connection-steady.log",
    "13-prove-loop.log",
    "14-prove-target-loop.log",
    "15-prove-target-entry.log",
    "16-prove-continuation-base.log",
    "17-prove-continuation-extended.log",
    "19-program-macro-identity.log",
    "20-ground-witness-empty.log",
    "21-ground-witness-example.log",
    "22-python-witnesses.log",
    "24-false-mutation-build.log",
    "27-build-operational-mutant.log",
    "30-k-decision-ledger.log",
    "31-untrusted-generation-summary.log",
    "32-krun-concrete-harness.log",
]
top_logs = [
    "11-prove-connection-initial.log",
    "12-prove-connection-steady.log",
    "13-prove-loop.log",
    "14-prove-target-loop.log",
    "15-prove-target-entry.log",
    "16-prove-continuation-base.log",
    "17-prove-continuation-extended.log",
    "20-ground-witness-empty.log",
    "21-ground-witness-example.log",
]
expected_failure_logs = [
    "25-false-mutation-proof.log",
    "28-operational-mutant-initial-proof.log",
    "29-operational-mutant-steady-proof.log",
]

for name in success_logs:
    text = (EVIDENCE / name).read_text(errors="replace")
    assert "EXIT_STATUS: 0\n" in text, name
for name in top_logs:
    text = (EVIDENCE / name).read_text(errors="replace")
    assert re.search(r"^#Top$", text, re.MULTILINE), name
for name in expected_failure_logs:
    text = (EVIDENCE / name).read_text(errors="replace")
    assert "EXIT_STATUS: 1\n" in text, name
    assert "WarnStuckClaimState" in text, name

review_lines = (ROOT / "REVIEW.md").read_text().splitlines()
assert review_lines[-2:] == [
    "VERDICT: PASS",
    "LEGITIMACY: LEGIT",
]
print(f"success_logs_checked={len(success_logs)}")
print(f"top_logs_checked={len(top_logs)}")
print(f"expected_failure_logs_checked={len(expected_failure_logs)}")
print("review_terminal_markers=valid")
