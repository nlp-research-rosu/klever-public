#!/usr/bin/env python3
"""Mechanical final report/evidence consistency checks."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/audit-output")


def main() -> int:
    review = (ROOT / "REVIEW.md").read_text()
    lines = review.splitlines()
    assert lines[-2:] == ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
    links = re.findall(r"\]\((evidence/[^)]+)\)", review)
    missing = [link for link in links if not (ROOT / link).is_file()]
    assert not missing, missing
    positive = [
        "07-kompile-llvm.log",
        "08-krun-concrete.log",
        "09-kompile-haskell.log",
        "10-kprove-all-balanced-inputs.log",
        "11-kprove-entry-and-examples-modular.log",
        "14-body-pinning.log",
        "15-kprove-witnesses.log",
        "17-kompile-body-mutant.log",
    ]
    for name in positive:
        text = (ROOT / "evidence" / name).read_text()
        assert "EXIT_STATUS: 0" in text, name
    for name in (
        "10-kprove-all-balanced-inputs.log",
        "11-kprove-entry-and-examples-modular.log",
        "15-kprove-witnesses.log",
    ):
        assert "#Top" in (ROOT / "evidence" / name).read_text(), name
    for name in ("16-kprove-false-result-mutation.log", "18-kprove-body-mutant.log"):
        text = (ROOT / "evidence" / name).read_text()
        assert "EXIT_STATUS: 1" in text, name
        assert "WarnStuckClaimState" in text, name
    concrete = (ROOT / "evidence" / "08-krun-concrete.log").read_text()
    assert "<exc>" in concrete and "NoExc" in concrete
    print(f"review_lines={len(lines)}")
    print(f"review_evidence_links={len(links)}")
    print("missing_links=0")
    print("positive_statuses_ok=true")
    print("negative_residuals_ok=true")
    print("final_markers_ok=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
