#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/maximum-120-audit
status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then status=1; fi
}

printf 'Concrete satisfying witness and false destination:\n'
run python3 /audit-output/evidence/mutation_witness.py

printf '\nMutation parse/spec-build check:\n'
run kprove "$WORK/spec-vacuity.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module SPEC-VACUITY \
  --dry-run

printf '\nExpected failure on the reachable off-by-one result obligation:\n'
printf '$ kprove %q --definition %q --spec-module SPEC-VACUITY\n' \
  "$WORK/spec-vacuity.k" "$WORK/verification-kompiled"
kprove "$WORK/spec-vacuity.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module SPEC-VACUITY
rc=$?
printf '[exit %d; expected nonzero]\n' "$rc"
if (( rc == 0 )); then
  printf 'ERROR: false mutation unexpectedly proved\n'
  status=1
fi

exit "$status"
