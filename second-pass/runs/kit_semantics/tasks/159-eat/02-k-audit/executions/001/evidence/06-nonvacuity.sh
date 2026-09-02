#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/159-eat
cp /audit-output/evidence/06-nonvacuity.k audit-nonvacuity.k
copy_status=$?
echo "mutation_copy_exit=${copy_status}"

kprove audit-nonvacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-NONVACUITY \
  --dry-run \
  --output none
dry_run_status=$?
echo "mutation_dry_run_exit=${dry_run_status}"

kprove audit-nonvacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-NONVACUITY \
  > audit-nonvacuity-raw.log 2>&1
proof_status=$?
echo "mutation_kprove_exit=${proof_status}"

sed -n '1,240p' audit-nonvacuity-raw.log
bounded_output_status=$?
echo "mutation_bounded_output_exit=${bounded_output_status}"

rg -q 'WarnStuckClaimState' audit-nonvacuity-raw.log
stuck_status=$?
echo "mutation_warn_stuck_present_exit=${stuck_status}"

rg -q 'implication check between the conditions has failed' \
  audit-nonvacuity-raw.log
residual_status=$?
echo "mutation_expected_residual_present_exit=${residual_status}"

cp audit-nonvacuity-raw.log \
  /audit-output/evidence/06-nonvacuity-raw.log
raw_copy_status=$?
echo "mutation_raw_log_copy_exit=${raw_copy_status}"

if (( copy_status != 0 || dry_run_status != 0 || proof_status == 0 ||
      bounded_output_status != 0 || stuck_status != 0 ||
      residual_status != 0 || raw_copy_status != 0 )); then
  exit 1
fi

exit 0
