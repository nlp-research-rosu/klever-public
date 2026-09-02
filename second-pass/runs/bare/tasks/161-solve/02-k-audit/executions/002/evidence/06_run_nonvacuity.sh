#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/k-proof

run_in_work() {
  printf '+ (cd %q &&' "$WORK"
  printf ' %q' "$@"
  printf ')\n'
  (
    cd "$WORK" || exit 125
    "$@"
  )
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Install reviewer-authored mutation only in scratch:\n'
run cp /audit-output/evidence/spec-vacuity-audit.k "$WORK/spec-vacuity-audit.k"
run_in_work sha256sum spec-vacuity-audit.k

printf '\nMutation parses/builds to KORE (successful dry run required):\n'
run_in_work kprove spec-vacuity-audit.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run

printf '\nConcrete satisfiable witness for the original execution:\n'
run_in_work krun solution.mpy \
  --definition fresh-semantic-kompiled \
  -cINPUT='97 :: 98 :: .PString'

printf '\nFalse mutation proof (expected meaningful non-zero stuck claim):\n'
run_in_work kprove spec-vacuity-audit.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
mutation_status=$?
printf 'expected_nonzero_observed=%s\n' "$(
  if [ "$mutation_status" -ne 0 ]; then printf true; else printf false; fi
)"
exit 0
