#!/usr/bin/env python3
"""Final self-check of review structure, terminal markers, and evidence signals."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"
REVIEW = ROOT / "REVIEW.md"


def require_text(path: Path, needles: list[str]) -> None:
    assert path.is_file() and not path.is_symlink(), path
    text = path.read_text(errors="replace")
    for needle in needles:
        assert needle in text, (path, needle)


review = REVIEW.read_text()
headings = [review.index(f"## {number}.") for number in range(1, 8)]
assert headings == sorted(headings)
assert review.splitlines()[-2:] == [
    "VERDICT: FAIL",
    "LEGITIMACY: NOT_LEGIT",
]

required = {
    "01_integrity.log": ["INTEGRITY_STATUS=PASS", "EXIT_STATUS=0"],
    "03_program_fidelity.log": [
        "mismatch_count=0",
        "DIFFERENTIAL_STATUS=PASS",
        "EXIT_STATUS=0",
    ],
    "05_kompile_llvm.log": ["EXIT_STATUS=0"],
    "05_krun_concrete.log": ["NoExc", "EXIT_STATUS=0"],
    "05_kompile_haskell.log": ["EXIT_STATUS=0"],
    "05_kprove_batch.log": ["#Top", "EXIT_STATUS=0"],
    "06_constructor_pinning.log": ["constructor_level_match=True", "EXIT_STATUS=0"],
    "07_rule_inventory.md": ["INVENTORY_STATUS=COMPLETE"],
    "08_body_mutation_build.log": ["EXIT_STATUS=0"],
    "08_body_mutation_proof.log": ["WarnStuckClaimState", "EXIT_STATUS=1"],
    "09_vacuity_dry_run.log": ["EXIT_STATUS=0"],
    "09_vacuity_proof.log": [
        "WarnStuckClaimState",
        "0",
        "A +Int B +Int C",
        "EXIT_STATUS=1",
    ],
}
for name, needles in required.items():
    require_text(EVIDENCE / name, needles)

for label in [
    "empty",
    "length-one",
    "length-two",
    "length-three",
    "length-four",
    "length-five",
    "length-six",
]:
    require_text(EVIDENCE / f"05_kprove_{label}.log", ["#Top", "EXIT_STATUS=0"])

print("REVIEW_STAGE_ORDER=PASS")
print("REVIEW_TERMINAL_MARKERS=PASS")
print("REQUIRED_EVIDENCE_SIGNALS=PASS")
print("EVIDENCE_SHA256:")
for path in sorted(EVIDENCE.iterdir()):
    if (
        path.is_file()
        and not path.is_symlink()
        and path.name != "99_verify_evidence.log"
    ):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{digest}  {path.name}")
print("FINAL_SELF_CHECK=PASS")
