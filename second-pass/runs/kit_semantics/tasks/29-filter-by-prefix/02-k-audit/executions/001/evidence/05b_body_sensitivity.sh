#!/usr/bin/env bash
set -u

cd /tmp/audit-work/work || exit 1
spec=auditor-body-sensitivity.k
definition=auditor-verification-kompiled
module=AUDITOR-BODY-SENSITIVITY

echo 'COMMAND: bash /audit-output/evidence/05b_body_sensitivity.sh'
echo 'MUTATION: actual loaded function body changed from conditional append to unconditional append'
echo 'SATISFYING_INPUT: strings=["abc","bcd"], prefix="a"'
echo 'ORIGINAL_EXPECTATION: ["abc"]; MUTANT_EXECUTION: ["abc","bcd"]'

echo "COMMAND: kprove $spec --definition $definition --spec-module $module --dry-run"
kprove "$spec" --definition "$definition" --spec-module "$module" --dry-run \
  > /audit-output/evidence/05b_body_sensitivity_dry_run.out 2>&1
dry_status=$?
echo "EXIT[dry-run]=$dry_status"

echo "COMMAND: kprove $spec --definition $definition --spec-module $module"
kprove "$spec" --definition "$definition" --spec-module "$module" \
  > /audit-output/evidence/05b_body_sensitivity_proof.out 2>&1
proof_status=$?
echo "EXIT[mutant-proof]=$proof_status"
sed -n '1,260p' /audit-output/evidence/05b_body_sensitivity_proof.out

if test "$dry_status" -ne 0; then
  echo 'RESULT: invalid mutation artifact'
  exit 1
fi
if test "$proof_status" -eq 0; then
  echo 'RESULT: mutated program unexpectedly proved the original result'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/05b_body_sensitivity_proof.out; then
  echo 'RESULT: missing expected stuck-claim residual'
  exit 1
fi
if ! rg -Fq 'iCons ( 98' /audit-output/evidence/05b_body_sensitivity_proof.out; then
  echo 'RESULT: residual did not expose the unconditionally appended bcd value'
  exit 1
fi

echo 'RESULT: PASS (actual-body mutation is not captured by the original loop bridge)'
exit 0
