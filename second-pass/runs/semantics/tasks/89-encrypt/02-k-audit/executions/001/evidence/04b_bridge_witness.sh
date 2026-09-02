#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruct || exit 99
cp /audit-output/evidence/bridge-witness.k bridge-witness.k
audit_copy_status=$?
echo 'COMMAND: cp /audit-output/evidence/bridge-witness.k /tmp/audit-work/reconstruct/bridge-witness.k'
echo "EXIT_STATUS: ${audit_copy_status}"

echo 'COMMAND: kprove --definition verification-kompiled bridge-witness.k --spec-module BRIDGE-WITNESS-BASE --dry-run'
kprove \
  --definition verification-kompiled \
  bridge-witness.k \
  --spec-module BRIDGE-WITNESS-BASE \
  --dry-run
audit_base_dry_status=$?
echo "EXIT_STATUS: ${audit_base_dry_status}"

echo 'COMMAND: kprove --definition verification-kompiled bridge-witness.k --spec-module BRIDGE-WITNESS-BASE'
kprove \
  --definition verification-kompiled \
  bridge-witness.k \
  --spec-module BRIDGE-WITNESS-BASE
audit_base_prove_status=$?
echo "EXIT_STATUS: ${audit_base_prove_status} (EXPECTED NONZERO)"

echo 'COMMAND: kprove --definition function-verification-kompiled bridge-witness.k --spec-module BRIDGE-WITNESS-EXTENDED --dry-run'
kprove \
  --definition function-verification-kompiled \
  bridge-witness.k \
  --spec-module BRIDGE-WITNESS-EXTENDED \
  --dry-run
audit_extended_dry_status=$?
echo "EXIT_STATUS: ${audit_extended_dry_status}"

echo 'COMMAND: kprove --definition function-verification-kompiled bridge-witness.k --spec-module BRIDGE-WITNESS-EXTENDED'
kprove \
  --definition function-verification-kompiled \
  bridge-witness.k \
  --spec-module BRIDGE-WITNESS-EXTENDED
audit_extended_prove_status=$?
echo "EXIT_STATUS: ${audit_extended_prove_status}"

if (( audit_copy_status != 0 || audit_base_dry_status != 0 || audit_base_prove_status == 0 || audit_extended_dry_status != 0 || audit_extended_prove_status != 0 )); then
  exit 1
fi
