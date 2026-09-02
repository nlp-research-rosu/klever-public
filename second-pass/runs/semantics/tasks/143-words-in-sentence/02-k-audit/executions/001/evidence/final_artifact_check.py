#!/usr/bin/env python3
from pathlib import Path


review = Path("/audit-output/REVIEW.md").read_text(encoding="utf-8")
assert review.endswith("VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n")
assert review.count("VERDICT:") == 1
assert review.count("LEGITIMACY:") == 1

required = [
    "01-integrity.log",
    "02-translation-identity.log",
    "03-differential.log",
    "07-kprove-loop.log",
    "08-kprove-entry.log",
    "11b-static-inventory.log",
    "13-vacuity-proof.log",
    "17-len-shadow-extended-krun.log",
    "21-kprove-loop-no-len.log",
    "24-bridge-free-proof.log",
]
evidence = Path("/audit-output/evidence")
for item in required:
    assert (evidence / item).is_file(), item
for log in evidence.glob("*.log"):
    assert log.stat().st_size <= 200_000, log

print(f"review_bytes={len(review.encode())}")
print(f"log_count={len(list(evidence.glob('*.log')))}")
print("final_markers_ok=true")
print("required_evidence_ok=true")
print("bounded_logs_ok=true")
