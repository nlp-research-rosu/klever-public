#!/usr/bin/env bash
set -uo pipefail

audit_claims=(
  empty-name
  bad-dot-count
  bad-initial
  bad-extension
  too-many-digits-txt
  too-many-digits-exe
  too-many-digits-dll
  valid-name-txt
  valid-name-exe
  valid-name-dll
)

audit_failed=0
for audit_claim in "${audit_claims[@]}"; do
  audit_log="/audit-output/evidence/03-kprove-${audit_claim}.log"
  audit_command="export PATH=\"/home/agent/.nix-profile/bin:\$PATH\"; kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC --claims SPEC.${audit_claim}"
  script -q -e -c "${audit_command}" "${audit_log}"
  audit_status=$?
  echo "CLAIM=${audit_claim} EXIT=${audit_status}"
  if [[ ${audit_status} -ne 0 ]]; then
    audit_failed=1
  fi
done

exit "${audit_failed}"
