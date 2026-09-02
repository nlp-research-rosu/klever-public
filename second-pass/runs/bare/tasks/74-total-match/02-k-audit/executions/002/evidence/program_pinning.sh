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

run kast "$work/solution.mpy" \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --expand-macros \
  --output json \
  --output-file "$work/solution.kast.json" || exit $?
run kast "$work/solution-macro.mpy" \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --expand-macros \
  --output json \
  --output-file "$work/solution-macro.kast.json" || exit $?
run cmp -s "$work/solution.kast.json" "$work/solution-macro.kast.json" || exit $?
run sha256sum "$work/solution.kast.json" "$work/solution-macro.kast.json"
run sed -n 1,80p "$work/solution.kast.json"
printf '%s\n' 'PROGRAM_CONSTRUCTOR_IDENTITY_PASS'
