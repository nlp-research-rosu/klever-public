#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/reconstruction
cd "$WORK" || exit 99

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

run cp /audit-output/evidence/spec-vacuity.k "$WORK/spec-vacuity.k"
printf '\nMUTATION_PARSE_AND_BUILD_CHECK\n'
run kprove spec-vacuity.k \
  --definition verification-lemma-kompiled \
  --spec-module SUM-PRODUCT-FRESH-FALSE-SPEC \
  --dry-run

printf '\nMUTATION_PROOF_EXPECTED_FAILURE\n'
run kprove spec-vacuity.k \
  --definition verification-lemma-kompiled \
  --spec-module SUM-PRODUCT-FRESH-FALSE-SPEC \
  --output pretty
