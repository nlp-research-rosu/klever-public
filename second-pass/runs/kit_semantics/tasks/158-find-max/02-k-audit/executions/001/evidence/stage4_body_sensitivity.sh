#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruct-001
evidence=/audit-output/evidence
log=$evidence/stage4_body_sensitivity_kprove.log

cd "$scratch" || exit 2
printf '$ kprove %q --definition %q --spec-module AUDIT-BODY-SENSITIVITY\n' \
  "$evidence/audit-body-sensitivity.k" \
  "$scratch/verification-fresh-kompiled"
kprove \
  "$evidence/audit-body-sensitivity.k" \
  --definition "$scratch/verification-fresh-kompiled" \
  --spec-module AUDIT-BODY-SENSITIVITY \
  > "$log" 2>&1
rc=$?
printf 'actual_exit=%d\n' "$rc"

if (( rc == 0 )); then
  printf 'UNEXPECTED: materially mutated executed body retained theorem\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$log"; then
  printf 'UNEXPECTED: mutation did not reach a stuck result obligation\n'
  exit 1
fi
if ! rg -Fq 'str ( .IntSeq )' "$log"; then
  printf 'UNEXPECTED: residual does not expose mutated empty return\n'
  exit 1
fi
printf 'EXPECTED: changed executed program term invalidated the original result\n'
exit 0
