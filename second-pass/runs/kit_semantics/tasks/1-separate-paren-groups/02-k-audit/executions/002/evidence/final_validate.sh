#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md
evidence=/audit-output/evidence

test -s "$review"
test "$(tail -n 2 "$review" | sed -n '1p')" = "VERDICT: PASS"
test "$(tail -n 1 "$review")" = "LEGITIMACY: LEGIT"
test "$(rg -c '^VERDICT:' "$review")" -eq 1
test "$(rg -c '^LEGITIMACY:' "$review")" -eq 1

for required in \
  stage1_integrity.log \
  stage2_fidelity.log \
  stage3_explicit_claims.log \
  stage4_pinning.log \
  rule_inventory.md \
  static_assessment.md \
  stage6_false_dry_run.log \
  stage6_false_proof.log
do
  test -s "$evidence/$required"
done

rg -q '^#Top$' "$evidence/stage3_explicit_claims.log"
rg -q '^\[exit 0\]$' "$evidence/stage3_explicit_claims.log"
rg -q 'WarnStuckClaimState' "$evidence/stage6_false_proof.log"
rg -q '^\[exit 1\]$' "$evidence/stage6_false_proof.log"

for script in "$evidence"/*.sh; do
  bash -n "$script"
done

python3 - <<'PY'
import ast
from pathlib import Path

for path in sorted(Path("/audit-output/evidence").glob("*.py")):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"PYTHON_SYNTAX_OK {path}")
PY

printf 'FINAL_REVIEW_VALID=True\n'
