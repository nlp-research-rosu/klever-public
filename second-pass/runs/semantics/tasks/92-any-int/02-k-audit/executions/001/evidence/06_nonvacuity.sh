#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
spec=spec-vacuity-audit.k
module=SPEC-VACUITY-AUDIT

cp "$work/$spec" "$evidence/$spec"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run'
(
  cd "$work" &&
  kprove "$spec" \
    --definition verification-kompiled \
    --spec-module "$module" \
    --dry-run
) > /tmp/audit-work/nonvacuity-dry-run.out 2>&1
dry_status=$?
echo "exit=$dry_status"
echo '$ bounded dry-run output'
wc -l -c /tmp/audit-work/nonvacuity-dry-run.out
sed -n '1,40p' /tmp/audit-work/nonvacuity-dry-run.out
cp /tmp/audit-work/nonvacuity-dry-run.out "$evidence/06_nonvacuity_dry_run.log"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT'
(
  cd "$work" &&
  kprove "$spec" \
    --definition verification-kompiled \
    --spec-module "$module"
) 2>&1 | tee /tmp/audit-work/nonvacuity-proof.out
prove_status=${PIPESTATUS[0]}
echo "exit=$prove_status"
cp /tmp/audit-work/nonvacuity-proof.out "$evidence/06_nonvacuity_proof.log"

grep -q 'WarnStuckClaimState' /tmp/audit-work/nonvacuity-proof.out
stuck_status=$?
grep -Eq 'notBool|#Equals|doesn.t unify|implication' /tmp/audit-work/nonvacuity-proof.out
obligation_status=$?
printf 'EXPECTED_CHECK dry_run_zero=%s proof_nonzero=%s stuck_warning=%s unmet_obligation_text=%s witness=(5,2,7) original=true mutated=false\n' \
  "$([ "$dry_status" -eq 0 ] && echo yes || echo no)" \
  "$([ "$prove_status" -ne 0 ] && echo yes || echo no)" \
  "$([ "$stuck_status" -eq 0 ] && echo yes || echo no)" \
  "$([ "$obligation_status" -eq 0 ] && echo yes || echo no)"

if test "$dry_status" -eq 0 &&
   test "$prove_status" -ne 0 &&
   test "$stuck_status" -eq 0 &&
   test "$obligation_status" -eq 0
then
  exit 0
fi
exit 1
