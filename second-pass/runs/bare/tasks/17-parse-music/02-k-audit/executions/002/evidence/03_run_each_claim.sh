#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction

labels=(
  entry-o
  entry-example
  entry-half
  entry-quarter
  loop-o
  loop-half
  loop-quarter
  loop-base
  bridge-o
  bridge-half
  bridge-quarter
)

overall_rc=0
for label in "${labels[@]}"; do
  full_label="SPEC-LABELED.label(${label})"
  echo "COMMAND: kprove spec-labeled.k --definition audit-verification-kompiled --spec-module SPEC-LABELED --claims '$full_label'"
  output="$(
    kprove spec-labeled.k \
      --definition audit-verification-kompiled \
      --spec-module SPEC-LABELED \
      --claims "$full_label" 2>&1
  )"
  claim_rc=$?
  printf '%s\n' "$output"
  echo "CLAIM=$label EXIT_STATUS=$claim_rc"
  if [[ "$claim_rc" -ne 0 || "$output" != *"#Top"* ]]; then
    overall_rc=1
  fi
done

echo "ALL_INDIVIDUAL_CLAIMS_EXIT_STATUS=$overall_rc"
exit "$overall_rc"
