#!/usr/bin/env bash
set -u

cd /tmp/audit-work/work || exit 1
definition=auditor-verification-kompiled
spec=auditor-false-result.k
module=AUDITOR-FALSE-RESULT

echo 'COMMAND: bash /audit-output/evidence/06_nonvacuity.sh'
echo 'SATISFYING_INPUT: strings=["abc","bcd"], prefix="a"'
echo 'CANONICAL_AND_GENERATED_RESULT: ["abc"]'
echo 'FALSE_MUTATION: require returned heap list at ref(0) to be empty'

echo
echo "COMMAND: kprove $spec --definition $definition --spec-module $module --dry-run"
kprove "$spec" --definition "$definition" --spec-module "$module" --dry-run \
  > /audit-output/evidence/06_nonvacuity_dry_run.out 2>&1
dry_status=$?
echo "EXIT[dry-run]=$dry_status"
sed -n '1,120p' /audit-output/evidence/06_nonvacuity_dry_run.out

echo
echo "COMMAND: kprove $spec --definition $definition --spec-module $module"
kprove "$spec" --definition "$definition" --spec-module "$module" \
  > /audit-output/evidence/06_nonvacuity_proof.out 2>&1
proof_status=$?
echo "EXIT[false-proof]=$proof_status"
sed -n '1,260p' /audit-output/evidence/06_nonvacuity_proof.out

if test "$dry_status" -ne 0; then
  echo 'RESULT: invalid mutation artifact (dry run failed)'
  exit 1
fi
if test "$proof_status" -eq 0; then
  echo 'RESULT: false mutation unexpectedly proved'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/06_nonvacuity_proof.out; then
  echo 'RESULT: proof failed without expected unmet-obligation residual'
  exit 1
fi
if ! rg -q 'vCons|filterPrefixAcc|iCons' /audit-output/evidence/06_nonvacuity_proof.out; then
  echo 'RESULT: residual does not expose the non-empty computed result'
  exit 1
fi

echo 'RESULT: PASS (well-formed false result obligation rejected as stuck)'
exit 0
