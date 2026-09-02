#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
cd "$scratch" || exit 90

echo "MUTATION executed body changes values[middle + 1] to values[middle]; postconditions unchanged"
echo "COMMAND python3 /audit-output/evidence/05_make_body_mutation.py > spec-body-mutation.k"
python3 /audit-output/evidence/05_make_body_mutation.py > spec-body-mutation.k
mutation_status=$?
echo "MUTATION_CREATE_EXIT=$mutation_status"

echo "COMMAND rg -n 'MEDIAN-SPEC-BODY-MUTATION|BinOp\\(\"\\+\", Name\\(\"middle\"\\), Int\\(1\\)\\)|Name\\(\"middle\"\\)\\)\\)' spec-body-mutation.k"
rg -n 'MEDIAN-SPEC-BODY-MUTATION|BinOp\("\+", Name\("middle"\), Int\(1\)\)|Name\("middle"\)\)\)' spec-body-mutation.k
inspect_status=$?
echo "MUTATION_INSPECT_EXIT=$inspect_status"

output=/tmp/audit-work/reconstruction/body-mutation-kprove.out
echo "COMMAND kprove spec-body-mutation.k --definition verification-kompiled --spec-module MEDIAN-SPEC-BODY-MUTATION --claims MEDIAN-SPEC-BODY-MUTATION.median-even"
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module MEDIAN-SPEC-BODY-MUTATION \
  --claims MEDIAN-SPEC-BODY-MUTATION.median-even > "$output" 2>&1
prove_status=$?
echo "BODY_MUTATION_KPROVE_EXIT=$prove_status"

echo "COMMAND sed -n '1,220p' $output"
sed -n '1,220p' "$output"
read_status=$?
echo "OUTPUT_READ_EXIT=$read_status"

rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check' "$output"
stuck_status=$?
echo "EXPECTED_STUCK_MARKER_EXIT=$stuck_status"

rg -q '^#Top$' "$output"
top_present=$?
echo "TOP_SEARCH_EXIT=$top_present (1 means #Top absent)"

if [[ $mutation_status -eq 0 &&
      $inspect_status -eq 0 &&
      $prove_status -ne 0 &&
      $read_status -eq 0 &&
      $stuck_status -eq 0 &&
      $top_present -eq 1 ]]; then
  echo "RESULT PASS: proof is sensitive to the executed program body"
  exit 0
fi
echo "RESULT FAIL: body-sensitivity probe did not fail in the expected way"
exit 1
