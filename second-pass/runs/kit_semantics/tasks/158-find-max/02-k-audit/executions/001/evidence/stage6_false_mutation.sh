#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruct-001
evidence=/audit-output/evidence
log=$evidence/stage6_false_mutation_kprove.log

cd "$scratch" || exit 2
printf '$ kprove %q --definition %q --spec-module AUDIT-FALSE-MUTATION\n' \
  "$evidence/audit-false-mutation.k" \
  "$scratch/verification-fresh-kompiled"
kprove \
  "$evidence/audit-false-mutation.k" \
  --definition "$scratch/verification-fresh-kompiled" \
  --spec-module AUDIT-FALSE-MUTATION \
  > "$log" 2>&1
rc=$?
printf 'actual_exit=%d\n' "$rc"

if (( rc == 0 )); then
  printf 'UNEXPECTED: false result proved\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$log"; then
  printf 'UNEXPECTED: failure was not a stuck claim\n'
  exit 1
fi
if ! rg -Fq 'str ( iCons ( 97' "$log"; then
  printf 'UNEXPECTED: residual does not expose correct "ab" return\n'
  exit 1
fi
printf 'EXPECTED: build/parse succeeded and false tie result was rejected\n'
exit 0
