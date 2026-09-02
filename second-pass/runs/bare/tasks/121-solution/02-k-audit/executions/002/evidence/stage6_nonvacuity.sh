#!/usr/bin/env bash
set -u

work=/tmp/audit-work/121-solution-audit/candidate
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

run cp /audit-output/evidence/spec-vacuity-audit.k \
  "$work/spec-vacuity-audit.k"
run kprove "$work/spec-vacuity-audit.k" \
  --definition "$work/verification-audit-kompiled" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run

printf '$ kprove %q --definition %q --spec-module SPEC-VACUITY-AUDIT --smt-timeout 1000\n' \
  "$work/spec-vacuity-audit.k" "$work/verification-audit-kompiled"
kprove "$work/spec-vacuity-audit.k" \
  --definition "$work/verification-audit-kompiled" \
  --spec-module SPEC-VACUITY-AUDIT \
  --smt-timeout 1000
rc=$?
printf '[exit %d; expected nonzero for the false off-by-one result]\n' "$rc"
if [ "$rc" -eq 0 ]; then
  status=1
fi

exit "$status"
