#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction
python3 /audit-output/evidence/06_vacuity_witness.py

kprove spec-audit-vacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module AUDIT-VACUITY \
  --dry-run \
  > /audit-output/evidence/06-vacuity-dry-run.log 2>&1
dry_run_status=$?
printf 'vacuity_dry_run_exit=%s\n' "${dry_run_status}"

set +e
kprove spec-audit-vacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module AUDIT-VACUITY \
  > /audit-output/evidence/06-vacuity-kprove.log 2>&1
mutation_status=$?
set -e
printf 'vacuity_kprove_exit=%s\n' "${mutation_status}"
test "${mutation_status}" -ne 0
rg -q 'WarnStuckClaimState' /audit-output/evidence/06-vacuity-kprove.log
rg -n 'WarnStuckClaimState|14 ~> \\.K|15|\\[Error\\]' \
  /audit-output/evidence/06-vacuity-kprove.log | head -n 100
