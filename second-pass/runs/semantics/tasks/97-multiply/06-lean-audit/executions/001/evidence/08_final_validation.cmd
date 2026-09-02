#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' 'COMMAND: enumerate audit artifacts'
find /audit-output -maxdepth 2 -type f -printf '%P\n' | sort
printf '%s\n' 'COMMAND: verify required evidence success markers'
rg -n \
  'ALL_RECORDED_INPUT_HASHES_AND_PRODUCER_BINDINGS_MATCH' \
  /audit-output/evidence/01_hash_reconstruction.log
rg -n \
  'BIJECTION_AND_INDEPENDENT_CLASSIFICATION_PASS' \
  /audit-output/evidence/03_inventory_reconstruction.log
rg -n \
  'RERUN_PREFLIGHT_PASS' \
  /audit-output/evidence/06_rerun_preflight_with_compat.log
rg -n \
  'OBLIGATION_BIJECTION_EMPTY_AND_TARGET_ABSENT' \
  /audit-output/evidence/07_stage4_structure.log
printf '%s\n' 'COMMAND: verify REVIEW.md has one exact terminal verdict pair'
test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1
test "$(tail -n 2 /audit-output/REVIEW.md)" = \
  $'VERDICT: PASS\nLEGITIMACY: LEGIT'
tail -n 8 /audit-output/REVIEW.md
printf '%s\n' 'COMMAND: hash final artifacts (excluding this actively written log)'
find /audit-output -maxdepth 2 -type f \
  ! -path '/audit-output/evidence/08_final_validation.log' \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum
printf '%s\n' 'FINAL_ARTIFACT_VALIDATION_PASS'
