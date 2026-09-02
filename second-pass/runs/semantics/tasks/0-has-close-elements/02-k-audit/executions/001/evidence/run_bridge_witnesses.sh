#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/0-has-close-elements
spec=bridge-witness.k
log=/audit-output/evidence/05-bridge-witnesses.log
cp /audit-output/evidence/bridge-witness.k "$scratch/$spec"
: > "$log"

run_one() {
  definition=$1
  module=$2
  {
    printf 'WORKDIR: %s\n' "$scratch"
    printf 'COMMAND: kprove %s --definition %s --spec-module %s\n' \
      "$spec" "$definition" "$module"
  } >> "$log"
  (
    cd "$scratch" || exit 125
    kprove "$spec" --definition "$definition" --spec-module "$module"
  ) 2>&1 | sed -n '1,160p' >> "$log"
  status=${PIPESTATUS[0]}
  printf 'EXIT: %s\n\n' "$status" >> "$log"
  printf '%s exit=%s\n' "$module" "$status"
  return "$status"
}

overall=0
run_one audit-build/base-kompiled \
  WITNESS-FIXED-EMPTY-INNER-LOOP-FALSE || overall=1
run_one audit-build/inner-kompiled \
  WITNESS-BRIDGED-EMPTY-INNER-LOOP-SUMMARY || overall=1
run_one audit-build/inner-kompiled \
  WITNESS-FIXED-SHADOWED-HELPER-FALSE || overall=1
run_one audit-build/helper-kompiled \
  WITNESS-BRIDGED-SHADOWED-HELPER-SUMMARY || overall=1
run_one audit-build/helper-kompiled \
  WITNESS-FIXED-EMPTY-OUTER-LOOP-FALSE || overall=1
run_one audit-build/outer-kompiled \
  WITNESS-BRIDGED-EMPTY-OUTER-LOOP-SUMMARY || overall=1
run_one audit-build/outer-kompiled \
  WITNESS-FIXED-SHADOWED-ENTRY-FALSE || overall=1
run_one audit-build/entry-kompiled \
  WITNESS-BRIDGED-SHADOWED-ENTRY-SUMMARY || overall=1

printf 'overall_exit=%s\n' "$overall" >> "$log"
exit "$overall"
