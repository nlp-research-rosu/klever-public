#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/source || exit 99

echo "Concrete satisfying witness for the mutated entry precondition:"
run python3 -c 'from solution import encrypt; print(repr(encrypt("")))'
witness_status=$?

echo "Dry run: parsing/claim construction must succeed:"
run kprove spec-vacuity.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_status=$?

echo "False result mutation: a non-zero stuck proof is expected:"
run kprove spec-vacuity.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module SPEC-VACUITY
proof_status=$?

printf 'summary witness=%d dry_run=%d mutated_proof=%d\n' \
  "$witness_status" "$dry_status" "$proof_status"

if (( witness_status == 0 && dry_status == 0 && proof_status != 0 )); then
  exit 0
fi
exit 1
