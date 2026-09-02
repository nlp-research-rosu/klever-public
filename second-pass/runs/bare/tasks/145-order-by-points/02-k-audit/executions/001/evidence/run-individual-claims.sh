#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/proof145
failed=0
cd "$work" || exit 125

for number in $(seq -w 1 13); do
  label="SPEC-AUDIT.audit-${number}"
  log="/audit-output/evidence/stage3-claim-${number}.log"
  (
    printf 'WORKDIR: %s\n' "$work"
    printf 'COMMAND: kprove spec-audit-labeled.k --definition verification-audit-kompiled --spec-module SPEC-AUDIT --claims %s\n' "$label"
    kprove spec-audit-labeled.k \
      --definition verification-audit-kompiled \
      --spec-module SPEC-AUDIT \
      --claims "$label"
    status=$?
    printf '\nEXIT_STATUS: %d\n' "$status"
    exit "$status"
  ) 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  if [[ $status -ne 0 ]]; then
    failed=1
  fi
done

exit "$failed"
