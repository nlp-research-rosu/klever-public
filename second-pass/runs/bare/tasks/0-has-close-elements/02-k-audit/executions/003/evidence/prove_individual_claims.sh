#!/usr/bin/env bash
set -uo pipefail

definition="/tmp/audit-work/build/verification-haskell-kompiled"
spec="/audit-output/evidence/spec-labelled.k"
failures=0

for number in 01 02 03 04 05 06 07 08 09; do
  label="SPEC-LABELLED.audit-claim-${number}"
  log="/audit-output/evidence/proof-claim-${number}.log"
  if /audit-output/evidence/run-logged.sh "$log" \
      timeout 180s kprove "$spec" \
      --definition "$definition" \
      --spec-module SPEC-LABELLED \
      --claims "$label"; then
    if ! rg -q '^#Top$' "$log"; then
      printf 'MISSING_TOP: %s\n' "$label"
      failures=$((failures + 1))
    fi
  else
    failures=$((failures + 1))
  fi
done

printf 'INDIVIDUAL_CLAIMS: 9\n'
printf 'FAILURES: %d\n' "$failures"
exit "$failures"
