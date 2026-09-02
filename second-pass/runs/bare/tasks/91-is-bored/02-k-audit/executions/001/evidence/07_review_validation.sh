#!/usr/bin/env bash
set -u

status=0

printf '%s\n' 'COMMAND: tail -n 2 /audit-output/REVIEW.md'
tail -n 2 /audit-output/REVIEW.md
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: verify exact final marker pair and seven numbered stages'
python3 -c '
from pathlib import Path
text = Path("/audit-output/REVIEW.md").read_text(encoding="utf-8")
assert text.splitlines()[-2:] == [
    "VERDICT: FAIL",
    "LEGITIMACY: NOT_LEGIT",
]
for number in range(1, 8):
    assert f"## {number}." in text
print("marker_pair=valid")
print("numbered_stage_count=7")
'
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: verify every relative evidence link in REVIEW.md exists'
python3 -c '
from pathlib import Path
import re
review = Path("/audit-output/REVIEW.md")
targets = re.findall(r"\]\((evidence/[^)]+)\)", review.read_text(encoding="utf-8"))
missing = [target for target in targets if not (review.parent / target).is_file()]
print(f"evidence_link_count={len(targets)}")
print(f"missing_evidence_links={missing!r}")
assert not missing
'
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: sha256sum REVIEW.md and reviewer-authored evidence sources'
sha256sum \
  /audit-output/REVIEW.md \
  /audit-output/evidence/*.py \
  /audit-output/evidence/*.sh \
  /audit-output/evidence/*.k
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

exit "$status"
