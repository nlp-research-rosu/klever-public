#!/usr/bin/env bash
set -u

cd /tmp/audit-work/work || exit 1
spec=auditor-wrong-iterator.k
definition=auditor-verification-kompiled
module=AUDITOR-WRONG-ITERATOR

echo 'COMMAND: bash /audit-output/evidence/05c_iterator_opposite.sh'
echo 'FALSE_INTERPRETATION: fixed list iteration over string "a" yields empty string'
echo "COMMAND: kprove $spec --definition $definition --spec-module $module --dry-run"
kprove "$spec" --definition "$definition" --spec-module "$module" --dry-run \
  > /audit-output/evidence/05c_iterator_opposite_dry_run.out 2>&1
dry_status=$?
echo "EXIT[dry-run]=$dry_status"

echo "COMMAND: kprove $spec --definition $definition --spec-module $module"
kprove "$spec" --definition "$definition" --spec-module "$module" \
  > /audit-output/evidence/05c_iterator_opposite_proof.out 2>&1
proof_status=$?
echo "EXIT[opposite-proof]=$proof_status"
sed -n '1,220p' /audit-output/evidence/05c_iterator_opposite_proof.out

if test "$dry_status" -eq 0 &&
   test "$proof_status" -ne 0 &&
   rg -q 'WarnStuckClaimState' /audit-output/evidence/05c_iterator_opposite_proof.out &&
   rg -Fq 'iCons ( 97' /audit-output/evidence/05c_iterator_opposite_proof.out
then
  echo 'RESULT: PASS (opposite iterator interpretation rejected; actual code 97 remains)'
  exit 0
fi
echo 'RESULT: FAIL (probe did not fail with the expected value residual)'
exit 1
