#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/reconstruction
RAW=$WORK/spec-body-mutation.fresh.raw.log
DRY=$WORK/spec-body-mutation.fresh.dry.kore

cd "$WORK" || exit 1

printf '%s\n' \
  'MUTATION: the closure body executed by the claim changes the final append argument from Int(8) to Int(7); the postcondition is unchanged'
printf '%s\n' \
  'SATISFYING WITNESS: A=8, B=8; mutated body returns [7], required result is [8]'
printf '%s\n' \
  'COMMAND: diff -u spec.k spec-body-mutation.k'
diff -u spec.k spec-body-mutation.k || true

printf '%s\n' \
  'COMMAND: kprove spec-body-mutation.k --definition fresh-verification-kompiled --spec-module SPEC-BODY-MUTATION --dry-run > spec-body-mutation.fresh.dry.kore'
kprove spec-body-mutation.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --dry-run > "$DRY" 2>&1
dry_status=$?
printf 'STATUS [body-mutation dry-run/build]: %s\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  sed -n '1,160p' "$DRY"
  exit "$dry_status"
fi
wc -c "$DRY"

printf '%s\n' \
  'COMMAND: kprove spec-body-mutation.k --definition fresh-verification-kompiled --spec-module SPEC-BODY-MUTATION'
kprove spec-body-mutation.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > "$RAW" 2>&1
proof_status=$?
printf 'STATUS [body sensitivity proof]: %s (expected nonzero)\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  sed -n '1,160p' "$RAW"
  printf '%s\n' 'RESULT: FAIL body mutation unexpectedly proved'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$RAW"; then
  sed -n '1,160p' "$RAW"
  printf '%s\n' 'RESULT: FAIL body mutation did not reach expected stuck obligation'
  exit 1
fi
printf '%s\n' 'BOUNDED BODY-SENSITIVITY OUTPUT (first 70 lines):'
sed -n '1,70p' "$RAW"
printf '%s\n' 'BOUNDED BODY-SENSITIVITY OUTPUT (last 80 lines):'
tail -n 80 "$RAW"
printf '%s\n' \
  'RESULT: executed claim body is sensitivity-checked; material body change failed at the unchanged result obligation'
