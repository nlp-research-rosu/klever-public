#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/fresh

printf '%s\n' \
  'COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.add-loop'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.add-loop
loop_status=$?
printf 'EXIT: %s\n' "$loop_status"
if [[ "$loop_status" -ne 0 ]]; then
  exit "$loop_status"
fi

printf '%s\n' \
  'COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
full_status=$?
printf 'EXIT: %s\n' "$full_status"
exit "$full_status"
