#!/usr/bin/env bash
set -uo pipefail

SOURCE=/tmp/audit-work/90-next-smallest/source
DEFINITION=/tmp/audit-work/90-next-smallest/rebuild/verification-kompiled
MUTATION="$SOURCE/spec-body-mutation-audit.k"

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run cp -p /audit-output/evidence/spec-body-mutation-audit.k "$MUTATION" || exit $?
run kprove "$MUTATION" \
  --definition "$DEFINITION" \
  --spec-module SPEC-BODY-MUTATION-AUDIT \
  --claims index-body-sensitivity \
  --dry-run \
  --output pretty || exit $?

printf '$'
printf ' %q' kprove "$MUTATION" \
  --definition "$DEFINITION" \
  --spec-module SPEC-BODY-MUTATION-AUDIT \
  --claims index-body-sensitivity \
  --output pretty
printf '\n'
kprove "$MUTATION" \
  --definition "$DEFINITION" \
  --spec-module SPEC-BODY-MUTATION-AUDIT \
  --claims index-body-sensitivity \
  --output pretty
proof_status=$?
printf '[exit %d]\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf 'ERROR: changed program body retained the original theorem\n'
  exit 1
fi
printf 'EXPECTED: index-0 body mutation invalidated the original result claim\n'
exit 0
