#!/usr/bin/env bash
set -u

mutation_dir=/tmp/audit-work/tests/false-postcondition
definition=/tmp/audit-work/build/proof-kompiled
status=0

printf '%s\n' '$ mkdir -p /tmp/audit-work/tests/false-postcondition'
mkdir -p "$mutation_dir"
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ cp /audit-output/evidence/stage6/spec-vacuity.k /tmp/audit-work/tests/false-postcondition/spec-vacuity.k'
cp -- /audit-output/evidence/stage6/spec-vacuity.k "$mutation_dir/spec-vacuity.k"
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ cp /tmp/audit-work/source/verification.k /tmp/audit-work/tests/false-postcondition/verification.k'
cp -- /tmp/audit-work/source/verification.k "$mutation_dir/verification.k"
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ cp /tmp/audit-work/source/semantic.k /tmp/audit-work/tests/false-postcondition/semantic.k'
cp -- /tmp/audit-work/source/semantic.k "$mutation_dir/semantic.k"
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ kprove spec-vacuity.k --definition /tmp/audit-work/build/proof-kompiled --spec-module SPEC-VACUITY --claims FALSE-PROMPT-RESULT --dry-run > dry-run.kore 2>&1'
kprove "$mutation_dir/spec-vacuity.k" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY \
  --claims FALSE-PROMPT-RESULT \
  --dry-run > "$mutation_dir/dry-run.kore" 2>&1
rc=$?
printf 'EXIT: %d\n' "$rc"
wc -c "$mutation_dir/dry-run.kore"
sha256sum "$mutation_dir/dry-run.kore"
tail -n 8 "$mutation_dir/dry-run.kore"
if [[ "$rc" -ne 0 ]]; then
  printf '%s\n' 'MUTATION_BUILD_SUCCESS: false'
  status=1
else
  printf '%s\n' 'MUTATION_BUILD_SUCCESS: true'
fi

printf '%s\n' '$ kprove spec-vacuity.k --definition /tmp/audit-work/build/proof-kompiled --spec-module SPEC-VACUITY --claims FALSE-PROMPT-RESULT'
output=$(kprove "$mutation_dir/spec-vacuity.k" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY \
  --claims FALSE-PROMPT-RESULT 2>&1)
rc=$?
printf '%s\n' "$output"
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -eq 0 ]]; then
  printf '%s\n' 'EXPECTED_PROOF_FAILURE: false'
  status=1
else
  printf '%s\n' 'EXPECTED_PROOF_FAILURE: true'
fi

if printf '%s\n' "$output" \
  | rg -q 'WarnStuckClaimState|implication check.*failed|cannot be rewritten'; then
  printf '%s\n' 'EXPECTED_UNMET_OBLIGATION_RESIDUAL: true'
else
  printf '%s\n' 'EXPECTED_UNMET_OBLIGATION_RESIDUAL: false'
  status=1
fi

exit "$status"
