#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate-src
evidence=/audit-output/evidence
runner="$evidence/run-and-log.sh"
claims=(
  int-int
  int-float
  int-str
  float-int
  float-float
  float-str
  str-int
  str-float
  str-str
)

failures=0
for claim in "${claims[@]}"; do
  "$runner" "$evidence/stage3-claim-$claim.log" "$scratch" \
    kprove spec.k --definition verification-kompiled --spec-module SPEC --claims "$claim"
  status=$?
  printf 'CLAIM %s EXIT_STATUS %d\n' "$claim" "$status"
  if [[ "$status" -ne 0 ]]; then
    failures=$((failures + 1))
  fi
done
printf 'CLAIM_COUNT=%d FAILURE_COUNT=%d\n' "${#claims[@]}" "$failures"
exit "$failures"
