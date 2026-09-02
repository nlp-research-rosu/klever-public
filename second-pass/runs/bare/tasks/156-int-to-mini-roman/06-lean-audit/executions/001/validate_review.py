#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


review = Path("/audit-output/REVIEW.md")
text = review.read_text()
evidence = Path("/audit-output/evidence")
result = {
    "review_sha256": hashlib.sha256(review.read_bytes()).hexdigest(),
    "exact_final_pair": text.endswith(
        "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
    ),
    "verdict_line_count": len(
        re.findall(r"(?m)^VERDICT: (?:PASS|CONCERNS|FAIL)$", text)
    ),
    "legitimacy_line_count": len(
        re.findall(r"(?m)^LEGITIMACY: (?:LEGIT|NOT_LEGIT)$", text)
    ),
    "candidate_present": Path("/candidate").exists(),
    "evidence_files": sorted(path.name for path in evidence.iterdir()),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(
    0
    if (
        result["exact_final_pair"]
        and result["verdict_line_count"] == 1
        and result["legitimacy_line_count"] == 1
        and not result["candidate_present"]
    )
    else 1
)
