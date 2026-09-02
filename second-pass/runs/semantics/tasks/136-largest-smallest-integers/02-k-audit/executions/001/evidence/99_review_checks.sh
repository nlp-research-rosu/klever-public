#!/usr/bin/env bash
set -u

status=0

printf 'COMMAND: bash /audit-output/evidence/99_review_checks.sh\n'
printf 'STAGE: final review marker and evidence sanity checks\n'

expected=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual=$(tail -n 2 /audit-output/REVIEW.md)
if [[ "$actual" == "$expected" ]]; then
  printf 'OK exact terminal verdict pairing\n'
else
  printf 'FAIL terminal verdict pairing\n'
  status=1
fi

marker_count=$(rg -c '^(VERDICT|LEGITIMACY): ' /audit-output/REVIEW.md)
printf 'terminal-marker count=%s expected=2\n' "$marker_count"
if [[ "$marker_count" -ne 2 ]]; then
  status=1
fi

for stage in 01_integrity 02_fidelity 03_reconstruction 04_inventory \
             05_adequacy_extensions 06_static_checks 07_nonvacuity; do
  log="/audit-output/evidence/${stage}.log"
  if rg -q 'FINAL EXIT: 0' "$log"; then
    printf 'OK %s contains FINAL EXIT: 0\n' "$stage"
  else
    printf 'FAIL %s lacks FINAL EXIT: 0\n' "$stage"
    status=1
  fi
done

if rg -q 'WarnStuckClaimState' /audit-output/evidence/07_nonvacuity.log &&
   rg -q '^[[:space:]]*A \+Int 1$' /audit-output/evidence/07_nonvacuity.log; then
  printf 'OK final non-vacuity log contains expected stuck arithmetic residual\n'
else
  printf 'FAIL final non-vacuity residual missing\n'
  status=1
fi

printf 'STAGE: reviewer-authored artifact SHA-256 manifest (logs excluded)\n'
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '*.log' \
  ! -name '99_review_checks.sh' \
  -print0 |
  sort -z |
  xargs -0 sha256sum
sha_status=${PIPESTATUS[2]}
printf 'EXIT SHA-256 manifest: %d\n' "$sha_status"
if [[ "$sha_status" -ne 0 ]]; then
  status=1
fi

printf 'FINAL EXIT: %d\n' "$status"
exit "$status"
