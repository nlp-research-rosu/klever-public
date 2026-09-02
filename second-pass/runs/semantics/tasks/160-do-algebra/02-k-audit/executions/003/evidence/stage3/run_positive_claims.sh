#!/usr/bin/env bash
set -u

workdir=/tmp/audit-work/160-do-algebra
runner=/audit-output/evidence/run_logged.sh
definition=audit-verification-kompiled
labels=(
  plus
  minus
  times
  floor
  power
  minus-assoc
  floor-assoc
  power-assoc
  prompt-precedence
  mixed-precedence
)

overall=0
cd "$workdir"
for label in "${labels[@]}"; do
  log="/audit-output/evidence/stage3/claim-${label}.log"
  "$runner" "$log" \
    kprove spec.k \
      --definition "$definition" \
      --spec-module SPEC \
      --claims "$label" \
      --warnings none
  status=$?
  printf 'CLAIM_RESULT label=%s exit=%s has_top=' "$label" "$status"
  if grep -q '^#Top$' "$log"; then
    printf 'yes\n'
  else
    printf 'no\n'
    status=1
  fi
  if (( status != 0 )); then
    overall=1
  fi
done

exit "$overall"
