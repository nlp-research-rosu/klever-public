#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit

echo '$ kprove spec-body-mutation.k --definition proof-audit-kompiled --spec-module SPEC-BODY-MUTATION'
kprove "$scratch/spec-body-mutation.k" \
  --definition "$scratch/proof-audit-kompiled" \
  --spec-module SPEC-BODY-MUTATION
status=$?
echo "body-mutation kprove exit=$status"
if (( status == 0 )); then
  echo 'UNEXPECTED: false mutated body proved'
  exit 1
fi
echo 'EXPECTED: body mutation rejected'
exit 0
