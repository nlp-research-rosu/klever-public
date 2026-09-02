#!/usr/bin/env bash
set -uo pipefail

echo '$ tail -n 2 /audit-output/REVIEW.md'
tail -n 2 /audit-output/REVIEW.md

echo '$ test "$(tail -n 2 /audit-output/REVIEW.md)" = $'"'"'VERDICT: PASS\nLEGITIMACY: LEGIT'"'"''
test "$(tail -n 2 /audit-output/REVIEW.md)" = $'VERDICT: PASS\nLEGITIMACY: LEGIT'
ending_rc=$?
echo "exit_code=$ending_rc"

echo '$ for status in expected-success exit files; do cat "$status"; done'
status_rc=0
for status in \
  /audit-output/evidence/01_inspect_inputs.exit \
  /audit-output/evidence/02_provenance_and_inventory.exit \
  /audit-output/evidence/03_hash_and_lemma_identity.exit \
  /audit-output/evidence/04_stage1_derived_lemma_recheck.exit \
  /audit-output/evidence/05_preflight_environment_fix.exit \
  /audit-output/evidence/05_stage4_preflight.exit \
  /audit-output/evidence/06_semantic_classification.exit \
  /audit-output/evidence/07_stage4_independent_gate.exit
do
  printf '%s: ' "$(basename "$status")"
  cat "$status"
  if ! grep -qx 'exit_code=0' "$status"; then
    status_rc=1
  fi
done
echo "aggregate_exit_code=$status_rc"

echo '$ cat /audit-output/evidence/05_stage4_preflight_initial_failure.exit'
cat /audit-output/evidence/05_stage4_preflight_initial_failure.exit

echo '$ test ! -e /candidate'
test ! -e /candidate
candidate_rc=$?
echo "exit_code=$candidate_rc"

if [ "$ending_rc" -ne 0 ]; then
  exit "$ending_rc"
fi
if [ "$status_rc" -ne 0 ]; then
  exit "$status_rc"
fi
exit "$candidate_rc"
