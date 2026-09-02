#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/58-common

echo 'NOTE: common-loop depends on member-fold; common-program depends on both auxiliary claims.'

echo 'COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.member-fold'
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims SPEC.member-fold
member_status=$?
echo "TARGET member-fold EXIT: ${member_status}"

echo 'COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --exclude SPEC.common-program'
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --exclude SPEC.common-program
loop_closure_status=$?
echo "TARGET common-loop WITH member-fold DEPENDENCY EXIT: ${loop_closure_status}"

echo 'COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module SPEC'
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC
program_closure_status=$?
echo "TARGET common-program WITH BOTH DEPENDENCIES EXIT: ${program_closure_status}"

echo "SUMMARY member=${member_status} loop_dependency_closure=${loop_closure_status} program_dependency_closure=${program_closure_status}"
if [[ ${member_status} -ne 0 || ${loop_closure_status} -ne 0 || ${program_closure_status} -ne 0 ]]; then
  exit 1
fi
