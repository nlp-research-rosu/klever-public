#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md
expected_tail=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual_tail="$(tail -n 2 "$review")"
[[ "$actual_tail" == "$expected_tail" ]]
echo "review_tail=PASS"

python3 - <<'PY'
import re
from pathlib import Path

review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
targets = re.findall(r"\]\((evidence/[^)]+)\)", text)
missing = [target for target in targets if not (review.parent / target).exists()]
print(f"relative_evidence_link_count={len(targets)}")
print(f"missing_relative_evidence_links={missing}")
if missing:
    raise SystemExit(1)
PY

positive_logs=(
  08-kprove-all-claims.log
  09-kprove-emitted-tree.log
  10-kprove-returns-on-one.log
  11-kprove-rejects-below-one.log
  12-kprove-rejects-small-base.log
  13-kprove-active-path.log
  14-kprove-loop-correct.log
)
for name in "${positive_logs[@]}"; do
  grep -Fxq '#Top' "/audit-output/evidence/logs/$name"
  grep -Fxq 'EXIT_STATUS: 0' "/audit-output/evidence/logs/$name"
done
echo "positive_proof_logs=PASS"

grep -Fq 'WarnStuckClaimState' \
  /audit-output/evidence/logs/16-vacuity-proof-expected-failure.log
grep -Fxq 'EXIT_STATUS: 1' \
  /audit-output/evidence/logs/16-vacuity-proof-expected-failure.log
grep -Fq '<result>' \
  /audit-output/evidence/logs/16-vacuity-proof-expected-failure.log
grep -Fq 'true' \
  /audit-output/evidence/logs/16-vacuity-proof-expected-failure.log
echo "non_vacuity_log=PASS"

python3 -m py_compile \
  /audit-output/evidence/trace_summary.py \
  /audit-output/evidence/differential_test.py \
  /audit-output/evidence/concrete_semantics_compare.py \
  /audit-output/evidence/claim_witnesses.py
echo "reviewer_python_scripts_compile=PASS"
