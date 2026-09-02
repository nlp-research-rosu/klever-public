#!/usr/bin/env python3
"""Final structural and evidence-link validation for REVIEW.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("/audit-output")
REVIEW = ROOT / "REVIEW.md"


def main() -> int:
    errors: list[str] = []
    text = REVIEW.read_text(encoding="utf-8")
    lines = text.splitlines()
    expected_tail = ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
    if lines[-2:] != expected_tail:
        errors.append(f"incorrect final lines: {lines[-2:]!r}")
    if text.count("VERDICT:") != 1:
        errors.append(f"VERDICT marker count is {text.count('VERDICT:')}")
    if text.count("LEGITIMACY:") != 1:
        errors.append(f"LEGITIMACY marker count is {text.count('LEGITIMACY:')}")

    for stage in range(1, 8):
        if not re.search(rf"^## {stage}\.", text, re.MULTILINE):
            errors.append(f"missing stage heading {stage}")

    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    local_links = [link for link in links if "://" not in link and not link.startswith("#")]
    missing_links: list[str] = []
    for link in local_links:
        target = (ROOT / link).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            missing_links.append(f"outside output root: {link}")
            continue
        if not target.exists():
            missing_links.append(link)
    if missing_links:
        errors.append(f"missing/invalid local links: {missing_links}")

    compiled_outputs = sorted(
        str(path)
        for path in ROOT.rglob("*-kompiled")
        if path.is_dir()
    )
    if compiled_outputs:
        errors.append(f"compiled definitions leaked into audit output: {compiled_outputs}")

    required_log_signals = {
        "evidence/stage3-kprove-all.log": ("#Top", "EXIT_STATUS: 0"),
        "evidence/stage5-nested-list-bridge-proof.log": ("#Top", "EXIT_STATUS: 0"),
        "evidence/stage6-vacuity-dry-run.log": ("EXIT_STATUS: 0",),
        "evidence/stage6-vacuity-proof.log": (
            "WarnStuckClaimState",
            "<k>\n    0 ~> .K",
            "EXIT_STATUS: 1",
        ),
    }
    for relative, signals in required_log_signals.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        for signal in signals:
            if signal not in content:
                errors.append(f"{relative} lacks expected signal {signal!r}")

    print(f"review_bytes={len(text.encode())}")
    print(f"review_lines={len(lines)}")
    print(f"markdown_links={len(links)}")
    print(f"local_links_checked={len(local_links)}")
    print(f"evidence_files={sum(1 for path in (ROOT / 'evidence').rglob('*') if path.is_file())}")
    print(f"final_lines={lines[-2:]!r}")
    print(f"errors={errors!r}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
