#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work/46-fib4-review || exit 99

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run test ! -e /candidate/spec-vacuity.k
run python3 /audit-output/evidence/make_vacuity_mutation.py
run python3 -c 'from solution import fib4; print("candidate_fib4_12=", fib4(12))'
run python3 -c 'from canonical import fib4; print("canonical_fib4_12=", fib4(12))'

run timeout 300 kprove spec-vacuity-review.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC-VACUITY \
  --claims FIB4-SPEC-VACUITY.operational-cases \
  --dry-run \
  --output pretty

run timeout 900 kprove spec-vacuity-review.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC-VACUITY \
  --claims FIB4-SPEC-VACUITY.operational-cases \
  --output pretty
