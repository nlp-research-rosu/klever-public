#!/usr/bin/env bash
set -euo pipefail

echo '$ rerun independent hash verification'
PYTHONPATH=/reference python3 /audit-output/evidence/01_verify_hashes.py >/dev/null
echo 'PASS'
echo '$ rerun canonical inventory verification'
PYTHONPATH=/reference python3 /audit-output/evidence/02_verify_inventory.py >/dev/null
echo 'PASS'
echo '$ rerun Stage 4 no-obligation and target verification'
PYTHONPATH=/reference python3 /audit-output/evidence/05_verify_stage4.py >/dev/null
echo 'PASS'
echo '$ compare saved returned preflight evidence to immutable recorded preflight'
python3 - <<'PY'
import json
from pathlib import Path
returned = json.loads(Path("/audit-output/evidence/04_preflight_return.json").read_text())
recorded = json.loads(Path("/reference/klean-generation/preflight.json").read_text())
assert returned == recorded
print("PASS: documents are exactly equal as JSON")
PY
echo '$ verify REVIEW.md has exactly one allowed final pair and ends there'
python3 - <<'PY'
from pathlib import Path
text = Path("/audit-output/REVIEW.md").read_text()
pair = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
assert text.endswith(pair)
assert text.count("VERDICT:") == 1
assert text.count("LEGITIMACY:") == 1
print("PASS")
PY
echo '$ list final evidence files'
find /audit-output/evidence -maxdepth 1 -type f -printf '%f\n' | sort
