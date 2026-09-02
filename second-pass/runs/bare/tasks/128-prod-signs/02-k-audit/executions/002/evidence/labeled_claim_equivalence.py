#!/usr/bin/env python3
"""Check that the audit-only labels did not change the submitted claims."""

from __future__ import annotations

import re
from pathlib import Path


def normalize(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    text = text.replace("SPEC-LABELED", "SPEC")
    text = re.sub(r"claim\s+\[[^\]]+\]:", "claim", text)
    return " ".join(text.split())


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/labeled_claim_equivalence.py")
    work = Path("/tmp/audit-work/fresh")
    submitted = normalize((work / "spec.k").read_text(encoding="utf-8"))
    labeled = normalize((work / "spec-labeled.k").read_text(encoding="utf-8"))
    print(f"normalized_claim_files_identical={str(submitted == labeled).lower()}")
    if submitted != labeled:
        raise SystemExit(1)
    print("STATUS: PASS")


if __name__ == "__main__":
    main()
