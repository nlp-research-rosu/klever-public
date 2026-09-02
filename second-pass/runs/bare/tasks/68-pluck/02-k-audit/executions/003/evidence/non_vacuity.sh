#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit

echo '$ kprove spec-vacuity.k --definition proof-audit-kompiled --spec-module SPEC-VACUITY --dry-run'
kprove "$scratch/spec-vacuity.k" \
  --definition "$scratch/proof-audit-kompiled" \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_status=$?
echo "false mutation dry-run/build exit=$dry_status"
if (( dry_status != 0 )); then
  echo 'UNEXPECTED: false mutation did not build'
  exit 1
fi

echo '$ kprove spec-vacuity.k --definition proof-audit-kompiled --spec-module SPEC-VACUITY'
mutation_output=$(
  kprove "$scratch/spec-vacuity.k" \
    --definition "$scratch/proof-audit-kompiled" \
    --spec-module SPEC-VACUITY 2>&1
)
mutation_status=$?
printf '%s\n' "$mutation_output"
echo "false mutation kprove exit=$mutation_status"

if (( mutation_status == 0 )); then
  echo 'UNEXPECTED: false result mutation proved'
  exit 1
fi
[[ "$mutation_output" == *"WarnStuckClaimState"* ]]
stuck_check=$?
echo "WarnStuckClaimState check exit=$stuck_check"
[[ "$mutation_output" == *"specScanArray"* && "$mutation_output" == *"VList ( .Ints )"* ]]
residual_check=$?
echo "expected result-equality residual check exit=$residual_check"
overall=$((stuck_check || residual_check))
if (( overall == 0 )); then
  echo 'EXPECTED: meaningful false result obligation rejected'
fi
exit "$overall"
