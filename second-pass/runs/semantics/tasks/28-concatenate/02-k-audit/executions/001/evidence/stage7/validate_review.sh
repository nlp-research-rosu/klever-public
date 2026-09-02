#!/usr/bin/env bash
set -uo pipefail

review=/audit-output/REVIEW.md

echo 'COMMAND: test -d /reference/reference-semantics'
test -d /reference/reference-semantics
echo "EXIT: $?"

echo 'COMMAND: tail -n 2 /audit-output/REVIEW.md'
tail -n 2 "$review"
status=$?
echo "EXIT: $status"

echo 'COMMAND: verify exact terminal verdict markers'
python3 - "$review" <<'PY'
from pathlib import Path
import sys

text = Path(sys.argv[1]).read_text()
expected = "VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n"
if not text.endswith(expected):
    raise SystemExit("review does not end with the exact verdict pair")
print("exact_terminal_markers=true")
PY
echo "EXIT: $?"

echo 'COMMAND: verify every absolute local Markdown evidence link exists'
python3 - "$review" <<'PY'
from pathlib import Path
import re
import sys

text = Path(sys.argv[1]).read_text()
targets = sorted(set(re.findall(r"\]\((/audit-output/[^)]+)\)", text)))
missing = [target for target in targets if not Path(target).exists()]
print(f"local_links={len(targets)}")
print(f"missing_links={len(missing)}")
for target in missing:
    print(target)
raise SystemExit(bool(missing))
PY
echo "EXIT: $?"

echo 'COMMAND: bash -n reviewer shell scripts'
bash -n \
  /audit-output/evidence/stage1/check_integrity.sh \
  /audit-output/evidence/stage2/check_fidelity.sh \
  /audit-output/evidence/stage7/validate_review.sh
echo "EXIT: $?"

echo 'COMMAND: syntax-check reviewer Python scripts without writing beside sources'
PYTHONPYCACHEPREFIX=/tmp/audit-work/reviewer-pycache python3 -m py_compile \
  /audit-output/evidence/stage2/differential_test.py \
  /audit-output/evidence/stage4/concrete_substitutions.py \
  /audit-output/evidence/stage5/inventory_k.py \
  /audit-output/evidence/stage5/assess_inventory.py
echo "EXIT: $?"

echo 'COMMAND: summarize exhaustive assessment dispositions'
python3 - <<'PY'
import collections
import csv

path = "/audit-output/evidence/stage5/construct_assessment.csv"
with open(path, newline="") as source:
    counts = collections.Counter(row["decision"] for row in csv.DictReader(source))
for name, count in sorted(counts.items()):
    print(f"{name}={count}")
print(f"TOTAL={sum(counts.values())}")
PY
echo "EXIT: $?"
