#!/usr/bin/env bash
set -uo pipefail

SOURCE=/tmp/audit-work/90-next-smallest/source
DEFINITION=/tmp/audit-work/90-next-smallest/rebuild/verification-kompiled
MUTATION="$SOURCE/spec-vacuity-audit.k"

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run cp -p /audit-output/evidence/spec-vacuity-audit.k "$MUTATION" || exit $?
run cmp /audit-output/evidence/spec-vacuity-audit.k "$MUTATION" || exit $?

run env "PYTHONPATH=$SOURCE" python3 -c \
  'from canonical import next_smallest; assert next_smallest([1,2]) == 2; print("canonical([1,2]) = 2, so mutated expected none is false")'
python_status=$?
if [[ "$python_status" -ne 0 ]]; then
  exit "$python_status"
fi

run kprove "$MUTATION" \
  --definition "$DEFINITION" \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims false-always-none-on-one-two \
  --dry-run \
  --output pretty
dry_status=$?
if [[ "$dry_status" -ne 0 ]]; then
  printf 'ERROR: mutation did not build/parse successfully\n'
  exit "$dry_status"
fi

printf '$'
printf ' %q' kprove "$MUTATION" \
  --definition "$DEFINITION" \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims false-always-none-on-one-two \
  --output pretty
printf '\n'
kprove "$MUTATION" \
  --definition "$DEFINITION" \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims false-always-none-on-one-two \
  --output pretty
proof_status=$?
printf '[exit %d]\n' "$proof_status"

if [[ "$proof_status" -eq 0 ]]; then
  printf 'ERROR: false mutation unexpectedly proved\n'
  exit 1
fi
printf 'EXPECTED: false result mutation was rejected after a successful dry run\n'
exit 0
