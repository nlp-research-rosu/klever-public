#!/usr/bin/env bash
set +e

audit_source=/tmp/audit-work/32-find-zero/source

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run cp /audit-output/evidence/spec-vacuity-fresh.k "$audit_source/spec-vacuity-fresh.k"

cd "$audit_source" || exit 98
printf 'WORKDIR: %s\n' "$PWD"

run kprove spec-vacuity-fresh.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY-FRESH \
  --dry-run

run kprove spec-vacuity-fresh.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY-FRESH
