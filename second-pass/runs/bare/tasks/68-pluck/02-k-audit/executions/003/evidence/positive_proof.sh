#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit

echo '$ kprove spec.k --definition proof-audit-kompiled --spec-module SPEC'
output=$(
  kprove "$scratch/spec.k" \
    --definition "$scratch/proof-audit-kompiled" \
    --spec-module SPEC 2>&1
)
status=$?
printf '%s\n' "$output"
echo "kprove exit=$status"
if (( status != 0 )); then
  exit "$status"
fi
if [[ "$output" == *"#Top"* ]]; then
  echo '#Top check exit=0'
  exit 0
fi
echo '#Top check exit=1'
exit 1
