#!/usr/bin/env bash
set -u -o pipefail

SCRATCH=/tmp/audit-work/141-file-name-check
cd "$SCRATCH" || exit 1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run nl -ba fresh-vacuity-spec.k
run python3 -c '
from solution import file_name_check
value = "a123.txt"
print(repr(value), file_name_check(value))
assert file_name_check(value) == "Yes"
'

run kprove \
  fresh-vacuity-spec.k \
  --definition audit-verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC \
  --dry-run \
  --warnings none
dry_status=$?
if [ "$dry_status" -ne 0 ]; then
  printf 'MUTATION DID NOT BUILD\n'
  exit "$dry_status"
fi

run kprove \
  fresh-vacuity-spec.k \
  --definition audit-verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC \
  --warnings all
proof_status=$?
if [ "$proof_status" -eq 0 ]; then
  printf 'FALSE MUTATION UNEXPECTEDLY PROVED\n'
  exit 1
fi
printf 'FALSE MUTATION REJECTED AS EXPECTED\n'
exit 0
