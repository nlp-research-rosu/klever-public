#!/usr/bin/env python3
"""Validate the published audit review and its final evidence bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
review = review_path.read_text()
fresh_path = Path("/audit-output/evidence/02_preflight_return.json")
fresh = json.loads(fresh_path.read_text())
recorded = json.loads(Path("/audit-input.json").read_text())["resolution"][
    "stage4_preflight"
]
assert review.endswith("VERDICT: PASS\nLEGITIMACY: LEGIT\n")
assert review.count("VERDICT:") == 1
assert review.count("LEGITIMACY:") == 1
assert fresh == recorded
assert not Path("/candidate").exists()
print("review_final_pair=PASS/LEGIT")
print("fresh_preflight_matches_recorded=true")
print("candidate_present=false")
print(f"review_bytes={len(review.encode())}")
print(
    "review_sha256="
    + hashlib.sha256(review_path.read_bytes()).hexdigest()
)
print(
    "preflight_return_sha256="
    + hashlib.sha256(fresh_path.read_bytes()).hexdigest()
)
