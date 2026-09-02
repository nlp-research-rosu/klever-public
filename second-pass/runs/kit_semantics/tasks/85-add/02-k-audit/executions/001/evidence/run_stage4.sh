#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/stage4_pinning.py'
python3 /audit-output/evidence/stage4_pinning.py
pinning_status=$?
printf 'EXIT: %s\n' "$pinning_status"
if [[ "$pinning_status" -ne 0 ]]; then
  exit "$pinning_status"
fi

cd /tmp/audit-work/fresh
printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-summary-witnesses.k --definition audit-verification-kompiled --spec-module SPEC-SUMMARY-WITNESSES'
kprove /audit-output/evidence/spec-summary-witnesses.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-SUMMARY-WITNESSES
witness_status=$?
printf 'EXIT: %s\n' "$witness_status"
exit "$witness_status"
