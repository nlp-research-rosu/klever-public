#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/fresh

body_output="$(mktemp /tmp/audit-body-proof.XXXXXX)"
trap 'rm -f "$body_output"' EXIT

printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-fresh-body.k --definition audit-verification-kompiled --spec-module SPEC-FRESH-BODY --dry-run'
kprove /audit-output/evidence/spec-fresh-body.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FRESH-BODY \
  --dry-run >/dev/null 2>&1
dry_status=$?
printf 'EXIT: %s\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  exit "$dry_status"
fi

printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-fresh-body.k --definition audit-verification-kompiled --spec-module SPEC-FRESH-BODY'
kprove /audit-output/evidence/spec-fresh-body.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FRESH-BODY >"$body_output" 2>&1
body_status=$?
printf 'EXIT: %s (expected nonzero)\n' "$body_status"
rg -n -m 1 'WarnStuckClaimState' "$body_output"
rg -n -m 1 -F '"$result" |-> 0' "$body_output"
if [[ "$body_status" -eq 0 ]] \
   || ! rg -q 'WarnStuckClaimState' "$body_output" \
   || ! rg -q -F '"$result" |-> 0' "$body_output"; then
  tail -n 120 "$body_output"
  exit 1
fi
printf '%s\n' 'BODY_SENSITIVITY=PASS'
