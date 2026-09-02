#!/usr/bin/env bash
set -euo pipefail

cd /audit-output

echo '$ sha256sum REVIEW.md'
sha256sum REVIEW.md

echo '$ tail -n 8 REVIEW.md'
tail -n 8 REVIEW.md

echo '$ python3 - <<PY  # validate the exact terminal verdict pair and evidence references'
python3 - <<'PY'
from pathlib import Path
import re

review_path = Path("/audit-output/REVIEW.md")
review = review_path.read_text()
required_end = "VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n"
assert review.endswith(required_end)
assert review.count("VERDICT:") == 1
assert review.count("LEGITIMACY:") == 1

references = sorted(set(re.findall(r"`(evidence/[^`]+)`", review)))
missing = [path for path in references if not (Path("/audit-output") / path).exists()]
print("terminal_pair_exact =", True)
print("referenced_evidence_count =", len(references))
print("missing_evidence =", missing)
assert not missing
print("REVIEW_VALIDATION = PASS")
PY
