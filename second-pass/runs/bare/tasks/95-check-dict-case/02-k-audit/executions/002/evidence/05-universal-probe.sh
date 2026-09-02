#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/95-check-dict-case-audit
cp /audit-output/evidence/spec-universal-probe.k "$scratch/"
printf '%s\n' \
  'COMMAND: kprove spec-universal-probe.k --definition verification-fresh-kompiled --spec-module SPEC-UNIVERSAL-PROBE'
(
  cd "$scratch" || exit 1
  kprove spec-universal-probe.k \
    --definition verification-fresh-kompiled \
    --spec-module SPEC-UNIVERSAL-PROBE
)
proof_status=$?
printf 'UNIVERSAL_PROBE_EXIT=%s\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'UNIVERSAL_PROBE=UNEXPECTEDLY_PROVED'
  exit 1
fi
printf '%s\n' 'UNIVERSAL_PROBE=EXPECTED_NOT_ESTABLISHED'
exit 0
