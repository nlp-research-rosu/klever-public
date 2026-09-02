#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/reconstruction
RAW=$WORK/audit-false-result.raw.log
DRY=$WORK/audit-false-result.dry.kore

cd "$WORK" || exit 1

printf '%s\n' \
  'MUTATION: final heap list changed from list(expectedDigits(A,B)) to list(vCons(10,expectedDigits(A,B)))'
printf '%s\n' \
  'SATISFYING WITNESS: A=10, B=14; precondition true; Python/correct formal result []; mutated result [10]'
printf '%s\n' \
  'COMMAND: diff -u spec.k audit-false-result.k'
diff -u spec.k audit-false-result.k || true

printf '%s\n' \
  'COMMAND: kprove audit-false-result.k --definition fresh-verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run > audit-false-result.dry.kore'
kprove audit-false-result.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run > "$DRY" 2>&1
dry_status=$?
printf 'STATUS [mutation dry-run/build]: %s\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  sed -n '1,160p' "$DRY"
  exit "$dry_status"
fi
wc -c "$DRY"

printf '%s\n' \
  'COMMAND: kprove audit-false-result.k --definition fresh-verification-kompiled --spec-module AUDIT-FALSE-RESULT'
kprove audit-false-result.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT > "$RAW" 2>&1
proof_status=$?
printf 'STATUS [false mutation proof]: %s (expected nonzero)\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  sed -n '1,160p' "$RAW"
  printf '%s\n' 'RESULT: FAIL mutation unexpectedly proved'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$RAW"; then
  sed -n '1,160p' "$RAW"
  printf '%s\n' 'RESULT: FAIL mutation did not reach expected stuck obligation'
  exit 1
fi

printf '%s\n' 'BOUNDED MUTATION OUTPUT (first 60 lines):'
sed -n '1,60p' "$RAW"
printf '%s\n' 'BOUNDED MUTATION OUTPUT (last 100 lines):'
tail -n 100 "$RAW"
printf '%s\n' \
  'RESULT: mutation built successfully and failed at the reachable false result obligation as expected'
