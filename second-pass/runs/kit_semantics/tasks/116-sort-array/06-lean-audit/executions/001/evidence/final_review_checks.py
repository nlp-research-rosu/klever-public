#!/usr/bin/env python3
"""Final consistency checks for the audit deliverable."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
review = review_path.read_text()
required_end = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
overall_logs = [
    "06_inventory_reconstruction.log",
    "28_bijection_and_target.log",
    "29_recorded_hashes_complete.log",
    "30_preflight_evidence_comparison.log",
    "31_definition_witnesses.log",
]
checks = {
    "review_has_exact_required_end": review.endswith(required_end),
    "one_verdict_line": review.count("VERDICT:") == 1,
    "one_legitimacy_line": review.count("LEGITIMACY:") == 1,
    "candidate_absent": not Path("/candidate").exists(),
}
for name in overall_logs:
    text = (Path("/audit-output/evidence") / name).read_text()
    checks[f"{name}_overall_true"] = '"overall": true' in text

preflight_log = Path("/audit-output/evidence/26_check_generation_rerun.log").read_text()
checks["fresh_preflight_no_obligations"] = '"status": "KLEAN_NO_OBLIGATIONS"' in preflight_log
checks["fresh_preflight_target_null"] = '"target": null' in preflight_log

print(
    json.dumps(
        {
            "review_sha256": hashlib.sha256(review_path.read_bytes()).hexdigest(),
            "checks": checks,
            "overall": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
