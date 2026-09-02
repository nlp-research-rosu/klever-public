#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

cp "$evidence/spec-vacuity.k" "$work/spec-vacuity.k"

printf '%s\n' \
  'COMMAND: kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY --dry-run' \
  'CWD: /tmp/audit-work/reconstruction' \
  'EXPECTED: exit 0 (mutation parses and builds)'
(
  cd "$work" || exit 99
  kprove spec-vacuity.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC-VACUITY \
    --dry-run
)
dry_status=$?
printf 'EXIT_STATUS: %s\n' "$dry_status"

printf '%s\n' \
  'COMMAND: kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY' \
  'CWD: /tmp/audit-work/reconstruction' \
  'EXPECTED: nonzero stuck claim; satisfying witness N=8 returns true, not false'
(
  cd "$work" || exit 99
  kprove spec-vacuity.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC-VACUITY
)
proof_status=$?
printf 'EXIT_STATUS: %s\n' "$proof_status"

if (( dry_status != 0 )); then
  exit 1
fi
if (( proof_status == 0 )); then
  exit 1
fi
exit 0
