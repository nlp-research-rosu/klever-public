#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work
cp /audit-output/evidence/06_spec_vacuity.k spec-vacuity.k

(
  echo 'COMMAND: kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module PILE-LOOP-SPEC-VACUITY --dry-run'
  kprove spec-vacuity.k \
    --definition audit-verification-kompiled \
    --spec-module PILE-LOOP-SPEC-VACUITY \
    --dry-run
  status=$?
  echo "EXIT_STATUS: ${status}"
  exit "${status}"
) > /audit-output/evidence/06a_vacuity_dry_run.log 2>&1
dry_status=$?

(
  echo 'COMMAND: kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module PILE-LOOP-SPEC-VACUITY'
  kprove spec-vacuity.k \
    --definition audit-verification-kompiled \
    --spec-module PILE-LOOP-SPEC-VACUITY
  status=$?
  echo "EXIT_STATUS: ${status}"
  exit "${status}"
) > /audit-output/evidence/06b_vacuity_kprove.log 2>&1
prove_status=$?

echo "dry_run_status=${dry_status}"
echo "proof_status=${prove_status}"

if (( dry_status != 0 )); then
  exit 1
fi
if (( prove_status == 0 )); then
  exit 2
fi
exit 0
