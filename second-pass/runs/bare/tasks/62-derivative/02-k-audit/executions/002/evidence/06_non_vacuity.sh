#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction-62 || exit 70

dry_run=(
  kprove spec-vacuity-audit.k
  --definition verification-fresh-kompiled
  --spec-module SPEC-VACUITY-AUDIT
  --dry-run
)
printf 'COMMAND:'
printf ' %q' "${dry_run[@]}"
printf '\n'
"${dry_run[@]}"
dry_status=$?
printf 'EXIT_STATUS: %d\n' "$dry_status"
if (( dry_status != 0 )); then
  echo "UNEXPECTED: mutation did not build"
  exit "$dry_status"
fi

prove=(
  timeout 120s
  kprove spec-vacuity-audit.k
  --definition verification-fresh-kompiled
  --spec-module SPEC-VACUITY-AUDIT
)
printf 'COMMAND:'
printf ' %q' "${prove[@]}"
printf '\n'
"${prove[@]}"
prove_status=$?
printf 'EXIT_STATUS: %d\n' "$prove_status"

if (( prove_status == 0 )); then
  echo "UNEXPECTED: false degree-start mutation proved"
  exit 1
fi
if (( prove_status == 124 )); then
  echo "UNEXPECTED: false degree-start mutation timed out"
  exit 2
fi
echo "EXPECTED_FAILURE: false result-constraining obligation was rejected"
exit 0
