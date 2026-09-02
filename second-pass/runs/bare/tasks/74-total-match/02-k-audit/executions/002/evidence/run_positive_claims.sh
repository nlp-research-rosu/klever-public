#!/usr/bin/env bash
set -u
export PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate
definition="$work/verification-audit-kompiled"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return "$rc"
}

run kprove "$work/spec.k" \
  --definition "$definition" \
  --spec-module SPEC || exit $?

for label in total-empty total-step first-le second-lt tie-first; do
  run kprove "$work/spec-labeled.k" \
    --definition "$definition" \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.$label" || exit $?
done

printf '%s\n' 'ALL_POSITIVE_CLAIMS_TOP'
