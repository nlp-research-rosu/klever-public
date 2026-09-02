#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
spec=/audit-output/evidence/06_spec_false_result.k
cd "$work" || exit 125

echo 'SATISFYING_WITNESS: N=5; precondition 5 >Int 0; actual/formal result=1; mutated demanded result=2'

echo 'COMMAND: kprove /audit-output/evidence/06_spec_false_result.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-FALSE-RESULT --claims AUDIT-SPEC-FALSE-RESULT.false-plus-one -I . --dry-run'
kprove "$spec" \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE-RESULT \
  --claims AUDIT-SPEC-FALSE-RESULT.false-plus-one \
  -I . \
  --dry-run
dry_status=$?
echo "EXIT_STATUS: $dry_status"

echo 'COMMAND: kprove /audit-output/evidence/06_spec_false_result.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-FALSE-RESULT --claims AUDIT-SPEC-FALSE-RESULT.false-plus-one -I . --output pretty'
kprove "$spec" \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE-RESULT \
  --claims AUDIT-SPEC-FALSE-RESULT.false-plus-one \
  -I . \
  --output pretty
proof_status=$?
echo "EXIT_STATUS: $proof_status"

if (( dry_status == 0 && proof_status != 0 )); then
  echo 'NONVACUITY_EXPECTATION_MET: parser/build succeeded and false result proof failed'
  exit 0
fi
echo 'NONVACUITY_EXPECTATION_NOT_MET'
exit 1
