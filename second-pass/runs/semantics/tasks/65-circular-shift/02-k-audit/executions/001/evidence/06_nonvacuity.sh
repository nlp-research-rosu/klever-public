#!/usr/bin/env bash
set -u
cd /tmp/audit-work/case || exit 125

printf '$ kprove spec-vacuity.k --definition verification-kompiled --spec-module CIRCULAR-SHIFT-SPEC-VACUITY --dry-run --warnings none\n'
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC-VACUITY \
  --dry-run \
  --warnings none
dry_rc=$?
printf '[dry-run exit %d]\n' "$dry_rc"
if test "$dry_rc" -ne 0; then
  printf 'INVALID NON-VACUITY TEST: mutated claim did not parse/build.\n'
  exit 90
fi

printf '$ kprove spec-vacuity.k --definition verification-kompiled --spec-module CIRCULAR-SHIFT-SPEC-VACUITY --depth 300 --warnings none\n'
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC-VACUITY \
  --depth 300 \
  --warnings none
proof_rc=$?
printf '[proof exit %d]\n' "$proof_rc"
if test "$proof_rc" -eq 0; then
  printf 'UNEXPECTED: false result mutation proved.\n'
  exit 91
fi

printf 'EXPECTED FAILURE: the false result obligation was not established.\n'
exit 0
