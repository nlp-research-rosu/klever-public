#!/usr/bin/env python3
"""Check decisive log signals and write a checksum manifest."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/audit-output/evidence")


def text(name: str) -> str:
    value = (ROOT / name).read_text(errors="replace")
    assert "timed_out: false" in value
    return value


def main() -> None:
    for name in (
        "01_integrity.log",
        "02_translation.log",
        "02_differential.log",
        "03_build_concrete.log",
        "03_build_proof.log",
        "03_kprove_all_submitted.log",
        "03_semantics_differential.log",
        "04_constructor_compare.log",
        "04_claim_witnesses.log",
        "04_build_body_mutant.log",
        "06_vacuity_dry_run.log",
    ):
        value = text(name)
        assert "exit_status: 0" in value, name

    aggregate = text("03_kprove_all_submitted.log")
    assert re.search(r"^#Top$", aggregate, re.MULTILINE)
    print("aggregate_submitted_spec=#Top exit0")

    for index in range(1, 12):
        name = f"03_kprove_claim_{index:02d}.log"
        value = text(name)
        assert "exit_status: 0" in value
        assert re.search(r"^#Top$", value, re.MULTILINE)
        print(f"claim_{index:02d}=#Top exit0")

    body = text("04_kprove_body_mutant.log")
    assert "exit_status: 1" in body
    assert "WarnStuckClaimState" in body
    assert "append" in body and "Int ( 2 )" in body
    print("body_sensitivity=expected_stuck exit1")

    vacuity = text("06_vacuity_kprove.log")
    assert "exit_status: 1" in vacuity
    assert "WarnStuckClaimState" in vacuity
    assert "vInt ( 2 )" in vacuity
    print("false_result_mutation=expected_stuck exit1")

    entries = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_file() or path.name == "SHA256SUMS":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        entries.append(f"{digest}  {path.name}")
    (ROOT / "SHA256SUMS").write_text("\n".join(entries) + "\n")
    print(f"checksum_entries={len(entries)}")
    print("EVIDENCE_SIGNALS_OK")


if __name__ == "__main__":
    main()
