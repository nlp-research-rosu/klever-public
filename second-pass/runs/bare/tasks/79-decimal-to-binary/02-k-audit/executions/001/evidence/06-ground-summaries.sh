#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then overall=1; fi
}

run cp \
  /audit-output/evidence/spec-ground-summaries.k \
  /tmp/audit-work/build-proof/spec-ground-summaries.k
run kprove \
  /tmp/audit-work/build-proof/spec-ground-summaries.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module AUDIT-SPEC-GROUND-SUMMARIES \
  --dry-run
run kprove \
  /tmp/audit-work/build-proof/spec-ground-summaries.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module AUDIT-SPEC-GROUND-SUMMARIES
run python3 -c \
  'import sys; sys.path.insert(0, "/tmp/audit-work"); import canonical, solution; values=[0,-1,15,32,-5]; print([(v, canonical.decimal_to_binary(v), solution.decimal_to_binary(v)) for v in values]); assert all(canonical.decimal_to_binary(v) == solution.decimal_to_binary(v) for v in values)'

printf '[script exit %d]\n' "$overall"
exit "$overall"
