#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/fresh

extended_output="$(mktemp /tmp/audit-stage5-extended.XXXXXX)"
wrong_output="$(mktemp /tmp/audit-stage5-wrong.XXXXXX)"
trap 'rm -f "$extended_output" "$wrong_output"' EXIT

printf '%s\n' \
  'COMMAND: krun audit-smoke.mpy --definition audit-verification-kompiled'
krun audit-smoke.mpy \
  --definition audit-verification-kompiled >"$extended_output" 2>&1
extended_status=$?
printf 'EXIT: %s\n' "$extended_status"
if [[ "$extended_status" -ne 0 ]]; then
  tail -n 120 "$extended_output"
  exit "$extended_status"
fi
perl -pe 's/\e\\[[0-9;]*m//g' "$extended_output" |
  rg -F \
    -e '"documented" |->' \
    -e '"empty_boundary" |->' \
    -e '"singleton" |->' \
    -e '"odd_value_at_odd_index" |->' \
    -e '"zero_at_odd_index" |->' \
    -e '"negative_even_at_odd_indices" |->' \
    -e '"mixed_branches" |->' \
    -e '<ret>' \
    -e '<exc>' \
    -e '<exit-code>'

printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-local-witnesses.k --definition audit-verification-kompiled --spec-module SPEC-LOCAL-WITNESSES'
kprove /audit-output/evidence/spec-local-witnesses.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-LOCAL-WITNESSES
positive_status=$?
printf 'EXIT: %s\n' "$positive_status"
if [[ "$positive_status" -ne 0 ]]; then
  exit "$positive_status"
fi

printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-local-wrong.k --definition audit-verification-kompiled --spec-module SPEC-LOCAL-WRONG'
kprove /audit-output/evidence/spec-local-wrong.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-LOCAL-WRONG >"$wrong_output" 2>&1
wrong_status=$?
printf 'EXIT: %s (expected nonzero)\n' "$wrong_status"
rg -n -m 1 'WarnStuckClaimState|cannot be rewritten further' "$wrong_output"
if [[ "$wrong_status" -eq 0 ]]; then
  printf '%s\n' 'ERROR: opposite projection interpretation unexpectedly proved'
  exit 1
fi

printf '%s\n' 'LOCAL_VALUE_SENSITIVITY=PASS'
