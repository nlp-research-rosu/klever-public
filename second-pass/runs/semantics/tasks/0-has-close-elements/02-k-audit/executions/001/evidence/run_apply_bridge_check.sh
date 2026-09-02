#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/0-has-close-elements
log=/audit-output/evidence/05b-apply-bridge-check.log
cp /audit-output/evidence/bridge-witness.k "$scratch/bridge-witness.k"
: > "$log"

run_one() {
  definition=$1
  module=$2
  {
    printf 'WORKDIR: %s\n' "$scratch"
    printf 'COMMAND: kprove bridge-witness.k --definition %s --spec-module %s\n' \
      "$definition" "$module"
  } >> "$log"
  (
    cd "$scratch" || exit 125
    kprove bridge-witness.k --definition "$definition" --spec-module "$module"
  ) 2>&1 | sed -n '1,180p' >> "$log"
  status=${PIPESTATUS[0]}
  printf 'EXIT: %s\n\n' "$status" >> "$log"
  printf '%s exit=%s\n' "$module" "$status"
  return "$status"
}

run_one audit-build/inner-kompiled WITNESS-FIXED-CLOSURE-FALSE
fixed_status=$?
run_one audit-build/helper-kompiled WITNESS-BRIDGED-CLOSURE-SUMMARY
bridged_summary_status=$?

{
  printf 'EXPECTED: fixed_status=0 and bridged_summary_status=1\n'
  printf 'fixed_status=%s\n' "$fixed_status"
  printf 'bridged_summary_status=%s\n' "$bridged_summary_status"
} >> "$log"

if [[ $fixed_status -eq 0 && $bridged_summary_status -ne 0 ]]; then
  exit 0
fi
exit 1
