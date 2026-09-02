#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0
run python3 /audit-output/evidence/vacuity_witness.py || overall=1

# Successful dry run distinguishes a well-formed mutation from a parser,
# import, or compilation failure.
run kprove /audit-output/evidence/spec-vacuity.k \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --spec-module SPEC-VACUITY \
  --dry-run \
  --output none || overall=1

printf '\n$ kprove /audit-output/evidence/spec-vacuity.k --definition /tmp/audit-work/build/verification-haskell-r2 --spec-module SPEC-VACUITY --output pretty\n'
kprove /audit-output/evidence/spec-vacuity.k \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --spec-module SPEC-VACUITY \
  --output pretty
status=$?
printf '[exit %d; expected nonzero for the reachable false result obligation]\n' "$status"
if (( status == 0 )); then
  overall=1
fi

printf '\n[script exit %d]\n' "$overall"
exit "$overall"
