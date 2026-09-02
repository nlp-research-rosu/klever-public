#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 90

printf '%s\n' '$ kprove spec-prefix-positive.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-PREFIX-POSITIVE-SPEC --claims SUM-SQUARES-PREFIX-POSITIVE-SPEC.empty-result-zero --output pretty'
baseline=$(kprove spec-prefix-positive.k \
  --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-PREFIX-POSITIVE-SPEC \
  --claims SUM-SQUARES-PREFIX-POSITIVE-SPEC.empty-result-zero \
  --output pretty 2>&1)
baseline_status=$?
printf '%s\n' "$baseline"
printf 'BASELINE EXIT: %s\n' "$baseline_status"
if (( baseline_status != 0 )) || ! grep -Fxq '#Top' <<<"$baseline"; then
  printf '%s\n' 'ERROR: reachable baseline did not close'
  exit 1
fi

run_mutation() {
  local file=$1
  local module=$2
  local claim=$3
  local witness=$4

  printf '\nMUTATION: %s\n' "$file"
  printf 'FALSE WITNESS: %s\n' "$witness"

  printf '$ kprove %s --definition audit-verification-kompiled --spec-module %s --claims %s.%s --dry-run\n' \
    "$file" "$module" "$module" "$claim"
  kprove "$file" \
    --definition audit-verification-kompiled \
    --spec-module "$module" \
    --claims "$module.$claim" \
    --dry-run > /tmp/audit-work/mutation-dry-run.out 2>&1
  local dry_status=$?
  sed -n '1,80p' /tmp/audit-work/mutation-dry-run.out
  printf 'DRY-RUN EXIT: %s\n' "$dry_status"
  if (( dry_status != 0 )); then
    printf '%s\n' 'ERROR: mutation did not build'
    return 1
  fi

  printf '$ kprove %s --definition audit-verification-kompiled --spec-module %s --claims %s.%s --output pretty\n' \
    "$file" "$module" "$module" "$claim"
  kprove "$file" \
    --definition audit-verification-kompiled \
    --spec-module "$module" \
    --claims "$module.$claim" \
    --output pretty > /tmp/audit-work/mutation-proof.out 2>&1
  local proof_status=$?
  sed -n '1,220p' /tmp/audit-work/mutation-proof.out
  printf 'PROOF EXIT: %s\n' "$proof_status"
  if (( proof_status == 0 )); then
    printf '%s\n' 'ERROR: false mutation unexpectedly closed'
    return 1
  fi
  if ! grep -q 'WarnStuckClaimState' /tmp/audit-work/mutation-proof.out; then
    printf '%s\n' 'ERROR: nonzero result was not the expected unmet reachability obligation'
    return 1
  fi
  printf '%s\n' 'EXPECTED STUCK CLAIM CONFIRMED'
}

run_mutation \
  spec-body-mutation.k \
  SUM-SQUARES-BODY-MUTATION-SPEC \
  body-sensitive \
  'input []: mutated initializer returns 1, claimed result is 0' || exit $?

run_mutation \
  spec-vacuity-audit.k \
  SUM-SQUARES-VACUITY-AUDIT-SPEC \
  off-by-one \
  'input []: original result is 0, mutated postcondition requires 1' || exit $?
