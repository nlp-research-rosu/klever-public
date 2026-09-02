#!/usr/bin/env bash
set -u

expected='VERDICT: CONCERNS
LEGITIMACY: LEGIT'
actual=$(tail -n 2 /audit-output/REVIEW.md)
if [ "$actual" != "$expected" ]; then
  printf '%s\n' 'final marker check failed' >&2
  exit 1
fi
printf '%s\n' 'final_markers=ok'

python3 - <<'PY'
import re
from pathlib import Path

review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
missing = []
for link in links:
    if "://" in link or link.startswith("#"):
        continue
    target = (review.parent / link).resolve()
    if not target.exists():
        missing.append((link, str(target)))
print(f"relative_links={len(links)} missing={len(missing)}")
for item in missing:
    print(item)
raise SystemExit(1 if missing else 0)
PY
status=$?
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

for log in \
  prove_loop_spec.log \
  prove_entry_spec.log \
  prove_for_spec.log
do
  rg -q '^\[exit 0;' "/audit-output/evidence/logs/$log" || exit 1
  rg -q '^#Top$' "/audit-output/evidence/logs/$log" || exit 1
done
printf '%s\n' 'positive_claim_logs=three_exit_0_with_top'

rg -q '^\[exit 0;' /audit-output/evidence/logs/vacuity_dry_run.log || exit 1
rg -q '^\[exit 1;' /audit-output/evidence/logs/vacuity_proof.log || exit 1
rg -q 'WarnStuckClaimState' /audit-output/evidence/logs/vacuity_proof.log || exit 1
printf '%s\n' 'fresh_vacuity_logs=dry_run_0_proof_1_stuck'
