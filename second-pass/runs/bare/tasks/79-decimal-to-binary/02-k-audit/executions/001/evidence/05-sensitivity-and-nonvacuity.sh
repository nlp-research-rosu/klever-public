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
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

run cp \
  /audit-output/evidence/spec-body-sensitivity.k \
  /tmp/audit-work/build-proof/spec-body-sensitivity.k
run cp \
  /audit-output/evidence/spec-false-result.k \
  /tmp/audit-work/build-proof/spec-false-result.k

run kprove \
  /tmp/audit-work/build-proof/spec-body-sensitivity.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module AUDIT-SPEC-BODY-SENSITIVITY \
  --dry-run

printf '%s\n' '$ kprove /tmp/audit-work/build-proof/spec-body-sensitivity.k --definition /tmp/audit-work/build-proof/verification-kompiled --spec-module AUDIT-SPEC-BODY-SENSITIVITY'
kprove \
  /tmp/audit-work/build-proof/spec-body-sensitivity.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module AUDIT-SPEC-BODY-SENSITIVITY
body_status=$?
printf '[exit %d; expected nonzero]\n' "$body_status"
if [ "$body_status" -eq 0 ]; then overall=1; fi

run kprove \
  /tmp/audit-work/build-proof/spec-false-result.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE-RESULT \
  --dry-run

printf '%s\n' '$ kprove /tmp/audit-work/build-proof/spec-false-result.k --definition /tmp/audit-work/build-proof/verification-kompiled --spec-module AUDIT-SPEC-FALSE-RESULT'
kprove \
  /tmp/audit-work/build-proof/spec-false-result.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE-RESULT
false_status=$?
printf '[exit %d; expected nonzero]\n' "$false_status"
if [ "$false_status" -eq 0 ]; then overall=1; fi

run python3 -c \
  'import sys; sys.path.insert(0, "/tmp/audit-work"); import canonical, solution; assert canonical.decimal_to_binary(15) == solution.decimal_to_binary(15) == "db1111db"; print("satisfying witness: input=15; actual result=db1111db; mutated result=db1110db is false")'

printf '[script exit %d]\n' "$overall"
exit "$overall"
