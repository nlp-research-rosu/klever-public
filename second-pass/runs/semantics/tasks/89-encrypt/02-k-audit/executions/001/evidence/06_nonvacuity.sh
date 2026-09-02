#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruct || exit 99
cp /audit-output/evidence/spec-vacuity.k spec-vacuity.k
audit_copy_status=$?
echo 'COMMAND: cp /audit-output/evidence/spec-vacuity.k /tmp/audit-work/reconstruct/spec-vacuity.k'
echo "EXIT_STATUS: ${audit_copy_status}"

echo 'SATISFYING_WITNESS: input str(.IntSeq), env 0, exact encrypt closure/builtins scopes, empty heap/stack, noRet, NoExc'
echo 'FALSE_OBLIGATION: submitted/generated Python returns ""; mutation requires "x"'

echo 'COMMAND: kprove spec-vacuity.k --definition function-verification-kompiled --spec-module SPEC-VACUITY --dry-run'
kprove \
  spec-vacuity.k \
  --definition function-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
audit_dry_status=$?
echo "EXIT_STATUS: ${audit_dry_status}"

echo 'COMMAND: kprove spec-vacuity.k --definition function-verification-kompiled --spec-module SPEC-VACUITY'
kprove \
  spec-vacuity.k \
  --definition function-verification-kompiled \
  --spec-module SPEC-VACUITY
audit_prove_status=$?
echo "EXIT_STATUS: ${audit_prove_status} (EXPECTED NONZERO)"

if (( audit_copy_status != 0 || audit_dry_status != 0 || audit_prove_status == 0 )); then
  exit 1
fi
