#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
cd "$scratch" || exit 90

output=/tmp/audit-work/reconstruction/nonvacuity-kprove.out
echo "WITNESS VS = vCons(3, .ValSeq); allInts=true; vsLen=1; pyMod(1,2)=1; actual result=3; mutated result=4"
echo "COMMAND kprove spec-vacuity.k --definition verification-kompiled --spec-module MEDIAN-SPEC-VACUITY"
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module MEDIAN-SPEC-VACUITY > "$output" 2>&1
prove_status=$?
echo "VACUITY_KPROVE_EXIT=$prove_status"

echo "COMMAND sed -n '1,240p' $output"
sed -n '1,240p' "$output"
read_status=$?
echo "OUTPUT_READ_EXIT=$read_status"

rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check' "$output"
stuck_status=$?
echo "EXPECTED_STUCK_MARKER_EXIT=$stuck_status"

rg -q '^#Top$' "$output"
top_present=$?
echo "TOP_SEARCH_EXIT=$top_present (1 means #Top absent)"

if [[ $prove_status -ne 0 &&
      $read_status -eq 0 &&
      $stuck_status -eq 0 &&
      $top_present -eq 1 ]]; then
  echo "RESULT PASS: meaningful false result mutation was rejected"
  exit 0
fi
echo "RESULT FAIL: mutation did not fail in the expected way"
exit 1
