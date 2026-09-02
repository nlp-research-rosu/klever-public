#!/usr/bin/env bash
set -u

work=/tmp/audit-work/59-largest-prime-factor
source_dir="$work/source"
definition="$work/build-stage3-fresh/verification-kompiled"
all_status=0

run_and_record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf 'EXIT: %d\n' "$command_status"
  return "$command_status"
}

# The universal entry theorem uses loop-refines-lpf as its circularity.  K's
# --claims option removes unselected helper claims, so retain that dependency
# when selecting the entry target.
run_and_record kprove "$source_dir/spec.k" \
  --definition "$definition" \
  --spec-module SPEC \
  --claims \
  SPEC.loop-refines-lpf,SPEC.largest-prime-factor-correct \
  --output pretty \
  || all_status=1

for claim_label in SPEC.prompt-example-13195 SPEC.prompt-example-2048; do
  run_and_record kprove "$source_dir/spec.k" \
    --definition "$definition" \
    --spec-module SPEC \
    --claims "$claim_label" \
    --output pretty \
    || all_status=1
done

# Reproduce the candidate's aggregate positive target command as a final check.
run_and_record kprove "$source_dir/spec.k" \
  --definition "$definition" \
  --spec-module SPEC \
  --output pretty \
  || all_status=1

exit "$all_status"
