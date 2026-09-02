#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/fresh

dry_output="$(mktemp /tmp/audit-stage6-dry.XXXXXX)"
proof_output="$(mktemp /tmp/audit-stage6-proof.XXXXXX)"
trap 'rm -f "$dry_output" "$proof_output"' EXIT

printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-fresh-false.k --definition audit-verification-kompiled --spec-module SPEC-FRESH-FALSE --dry-run'
kprove /audit-output/evidence/spec-fresh-false.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FRESH-FALSE \
  --dry-run >"$dry_output" 2>&1
dry_status=$?
printf 'EXIT: %s\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  tail -n 120 "$dry_output"
  exit "$dry_status"
fi
printf '%s\n' 'MUTATION_BUILD=PASS'

printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-fresh-false.k --definition audit-verification-kompiled --spec-module SPEC-FRESH-FALSE'
kprove /audit-output/evidence/spec-fresh-false.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FRESH-FALSE >"$proof_output" 2>&1
proof_status=$?
printf 'EXIT: %s (expected nonzero)\n' "$proof_status"
rg -n -m 1 'WarnStuckClaimState' "$proof_output"
rg -n -m 1 -F '"$result" |-> -6' "$proof_output"
if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'ERROR: fresh false result unexpectedly proved'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$proof_output"; then
  printf '%s\n' 'ERROR: failure was not the expected unmet reachability obligation'
  tail -n 120 "$proof_output"
  exit 1
fi
if ! rg -q -F '"$result" |-> -6' "$proof_output"; then
  printf '%s\n' 'ERROR: residual did not expose the expected correct result -6'
  tail -n 120 "$proof_output"
  exit 1
fi
printf '%s\n' 'FRESH_NON_VACUITY=PASS'
