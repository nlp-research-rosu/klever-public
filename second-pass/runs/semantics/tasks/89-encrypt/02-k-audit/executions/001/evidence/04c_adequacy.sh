#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruct || exit 99
audit_overall_status=0

echo 'COMMAND: rg -n "solution\\.mpy|#loadAll|Module\\(|FuncDef\\(" /candidate/spec.k /candidate/verification.k /candidate/prove.sh'
rg -n 'solution\.mpy|#loadAll|Module\(|FuncDef\(' \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/prove.sh
audit_pinning_search_status=$?
echo "EXIT_STATUS: ${audit_pinning_search_status}"

echo 'COMMAND: cp /audit-output/evidence/ground-spec.k /tmp/audit-work/reconstruct/ground-spec.k'
cp /audit-output/evidence/ground-spec.k ground-spec.k
audit_copy_status=$?
echo "EXIT_STATUS: ${audit_copy_status}"

echo 'COMMAND: kprove --definition function-verification-kompiled ground-spec.k --spec-module GROUND-SPEC --dry-run'
kprove \
  --definition function-verification-kompiled \
  ground-spec.k \
  --spec-module GROUND-SPEC \
  --dry-run
audit_dry_status=$?
echo "EXIT_STATUS: ${audit_dry_status}"

echo 'COMMAND: kprove --definition function-verification-kompiled ground-spec.k --spec-module GROUND-SPEC'
kprove \
  --definition function-verification-kompiled \
  ground-spec.k \
  --spec-module GROUND-SPEC
audit_prove_status=$?
echo "EXIT_STATUS: ${audit_prove_status}"

echo 'COMMAND: python3 /audit-output/evidence/ground_compare.py'
python3 /audit-output/evidence/ground_compare.py
audit_compare_status=$?
echo "EXIT_STATUS: ${audit_compare_status}"

if (( audit_copy_status != 0 || audit_dry_status != 0 || audit_prove_status != 0 || audit_compare_status != 0 )); then
  audit_overall_status=1
fi
exit "${audit_overall_status}"
