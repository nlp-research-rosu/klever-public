#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruct || exit 99
cp /audit-output/evidence/bridge-connection.k bridge-connection.k
audit_copy_status=$?
echo 'COMMAND: cp /audit-output/evidence/bridge-connection.k /tmp/audit-work/reconstruct/bridge-connection.k'
echo "EXIT_STATUS: ${audit_copy_status}"

echo 'COMMAND: kprove --definition verification-kompiled bridge-connection.k --spec-module BRIDGE-CONNECTION-SPEC --dry-run'
kprove \
  --definition verification-kompiled \
  bridge-connection.k \
  --spec-module BRIDGE-CONNECTION-SPEC \
  --dry-run
audit_dry_status=$?
echo "EXIT_STATUS: ${audit_dry_status}"

echo 'COMMAND: kprove --definition verification-kompiled bridge-connection.k --spec-module BRIDGE-CONNECTION-SPEC'
kprove \
  --definition verification-kompiled \
  bridge-connection.k \
  --spec-module BRIDGE-CONNECTION-SPEC
audit_prove_status=$?
echo "EXIT_STATUS: ${audit_prove_status}"

if (( audit_copy_status != 0 || audit_dry_status != 0 || audit_prove_status != 0 )); then
  exit 1
fi
