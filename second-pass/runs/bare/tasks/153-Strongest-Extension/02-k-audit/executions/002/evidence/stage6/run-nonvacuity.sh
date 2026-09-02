#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/153-strongest-extension
spec="$scratch/spec-vacuity-audit.k"
definition="$scratch/verification-kompiled"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run'
kprove "$spec" --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
build_status=$?
echo "exit_status=$build_status"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT'
kprove "$spec" --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT
proof_status=$?
echo "exit_status=$proof_status (expected nonzero for false returned value)"

if [[ $build_status -ne 0 ]]; then
  exit 2
fi
if [[ $proof_status -eq 0 ]]; then
  exit 3
fi
exit 0
