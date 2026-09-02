#!/usr/bin/env bash
set -u
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT
set -x

cd /tmp/audit-work/108-count-nums
failures=0

run_group() {
  description=$1
  labels=$2
  printf "BEGIN_GROUP %s LABELS=%s\n" "$description" "$labels"
  timeout --signal=TERM --kill-after=10 120 \
    kprove spec-labeled.k \
      --definition verification-kompiled \
      --spec-module SPEC-LABELED \
      --claims "$labels"
  status=$?
  printf "END_GROUP %s EXIT_STATUS=%s\n" "$description" "$status"
  if [[ "$status" -ne 0 ]]; then
    failures=$((failures + 1))
  fi
}

AUX='SPEC-LABELED.digit-helper,SPEC-LABELED.count-empty,SPEC-LABELED.count-positive-head,SPEC-LABELED.count-nonpositive-head'
run_group auxiliary_mutual_induction "$AUX"
run_group entry_empty_with_dependencies "$AUX,SPEC-LABELED.entry-empty"
run_group entry_positive_with_dependencies "$AUX,SPEC-LABELED.entry-positive-head"
run_group entry_nonpositive_with_dependencies "$AUX,SPEC-LABELED.entry-nonpositive-head"

printf "TOTAL_GROUP_FAILURES=%s\n" "$failures"
exit "$failures"
