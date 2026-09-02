#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit
spec="$work/spec-labeled.k"
definition="$work/proof-kompiled"
labels=(
  int-eq
  int-gt
  int-lt
  float-eq
  float-gt
  float-lt
  example-1
  example-2
  example-3
  example-4
)

for label in "${labels[@]}"; do
  printf 'COMMAND: kprove spec-labeled.k --definition proof-kompiled --spec-module SPEC-LABELED --claims SPEC-LABELED.%s --output pretty\n' "$label"
  kprove "$spec" \
    --definition "$definition" \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.$label" \
    --output pretty
  status=$?
  printf 'CLAIM %s EXIT: %s\n' "$label" "$status"
  (( status == 0 )) || exit "$status"
done

printf '%s\n' 'STAGE3_EACH_CLAIM_OK'
