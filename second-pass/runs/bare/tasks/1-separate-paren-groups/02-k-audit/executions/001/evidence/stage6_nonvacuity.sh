#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

run cp \
  /audit-output/evidence/spec-vacuity-audit.k \
  /tmp/audit-work/candidate/spec-vacuity-audit.k

cd /tmp/audit-work/candidate || exit 99

run kprove spec-vacuity-audit.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
run kprove spec-vacuity-audit.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --output pretty
