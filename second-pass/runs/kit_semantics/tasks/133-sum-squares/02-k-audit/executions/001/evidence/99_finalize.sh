#!/usr/bin/env bash
set -euxo pipefail

bash -n \
  /audit-output/evidence/02_program_fidelity.sh \
  /audit-output/evidence/03_clean_rebuild.sh \
  /audit-output/evidence/04_pinning_ground.sh \
  /audit-output/evidence/04_body_sensitivity.sh \
  /audit-output/evidence/05_ceil_bridge.sh \
  /audit-output/evidence/06_nonvacuity.sh

python3 - <<'PY'
import ast
from pathlib import Path

for path in sorted(Path("/audit-output/evidence").glob("*.py")):
    ast.parse(path.read_text(), filename=str(path))
print("reviewer_python_parse=ok")

review = Path("/audit-output/REVIEW.md").read_text()
assert review.endswith("VERDICT: PASS\nLEGITIMACY: LEGIT\n")
assert review.count("VERDICT:") == 1
assert review.count("LEGITIMACY:") == 1
print("review_terminal_markers=exact")
PY

test "$(wc -l < /audit-output/evidence/05-rule-inventory.tsv)" -eq 936
test "$(cat /audit-output/evidence/03-kprove-loop.log | head -n 1)" = "#Top"
test "$(cat /audit-output/evidence/03-kprove-all-claims.log | head -n 1)" = "#Top"
rg -Fq 'sumCeilSquares ( VS ) +Int 1' \
  /audit-output/evidence/04-body-sensitivity-kprove.log
rg -q 'WarnStuckClaimState' /audit-output/evidence/06-vacuity-kprove.log
rg -Fq '14 ~> .K' /audit-output/evidence/06-vacuity-kprove.log
test -z "$(find /audit-output -type l -print -quit)"

find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '99-evidence-sha256.txt' \
  ! -name '99-final-check.log' \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > /audit-output/evidence/99-evidence-sha256.txt

tail -n 2 /audit-output/REVIEW.md
printf 'FINAL_AUDIT_CHECKS_OK\n'
