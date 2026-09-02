#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/22-filter-integers
definition="$work/reviewer-verification-kompiled"
spec="$work/spec.k"
overall=0

run_claim() {
  label="$1"
  printf 'COMMAND: kprove %q --definition %q --spec-module FILTER-SPEC --claims FILTER-SPEC.%s\n' \
    "$spec" "$definition" "$label"
  kprove "$spec" \
    --definition "$definition" \
    --spec-module FILTER-SPEC \
    --claims "FILTER-SPEC.$label"
  status=$?
  printf 'CLAIM %s EXIT %s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
}

run_claim empty
run_claim prompt-example-one
run_claim prompt-example-two
run_claim order-and-scalars

printf 'COMMAND: kprove %q --definition %q --spec-module FILTER-SPEC\n' \
  "$spec" "$definition"
kprove "$spec" --definition "$definition" --spec-module FILTER-SPEC
combined_status=$?
printf 'COMBINED EXIT %s\n' "$combined_status"
if [[ "$combined_status" -ne 0 ]]; then
  overall=1
fi

printf 'STAGE3_PROOFS EXIT %s\n' "$overall"
exit "$overall"
