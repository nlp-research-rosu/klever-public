#!/usr/bin/env bash
set -uo pipefail

scratch="/tmp/audit-work/audit19"
logger="/audit-output/evidence/run_logged.sh"
claims=(
  number-value-zero
  number-value-one
  number-value-two
  number-value-three
  number-value-four
  number-value-five
  number-value-six
  number-value-seven
  number-value-eight
  number-value-nine
  sort-numbers-symbolic
)

cd "$scratch" || exit 70
failures=0
for claim in "${claims[@]}"; do
  log="/audit-output/evidence/stage3-kprove-${claim}.log"
  "$logger" "$log" timeout 300 kprove spec.k \
    --definition verification-kompiled \
    --spec-module SORT-NUMBERS-SPEC \
    --claims "SORT-NUMBERS-SPEC.${claim}"
  status=$?
  printf 'CLAIM %s STATUS %d\n' "$claim" "$status"
  if [[ "$status" -ne 0 ]]; then
    failures=$((failures + 1))
  fi
done

printf 'POSITIVE_CLAIM_COUNT: %d\n' "${#claims[@]}"
printf 'POSITIVE_CLAIM_FAILURES: %d\n' "$failures"
exit "$failures"
