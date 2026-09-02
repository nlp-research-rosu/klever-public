#!/usr/bin/env bash
set -u

log=/audit-output/evidence/05_operational_sensitivity.log
exec > >(tee "$log") 2>&1

run_success() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

run_expected_failure() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d; expected nonzero]\n' "$status"
  if test "$status" -eq 0; then
    printf 'UNEXPECTED SUCCESS\n'
    exit 1
  fi
}

work=/tmp/audit-work/rebuild/candidate
cd "$work" || exit 1

run_success kprove spec-body-sensitivity.k \
  --definition verification-base-kompiled \
  --spec-module BODY-SENSITIVITY \
  --dry-run

run_expected_failure kprove spec-body-sensitivity.k \
  --definition verification-base-kompiled \
  --spec-module BODY-SENSITIVITY

run_success kprove spec-context-sensitivity.k \
  --definition verification-base-kompiled \
  --spec-module CONTEXT-SENSITIVITY-BASE

run_success kprove spec-context-sensitivity-lemma.k \
  --definition verification-lemma-kompiled \
  --spec-module CONTEXT-SENSITIVITY-LEMMA
