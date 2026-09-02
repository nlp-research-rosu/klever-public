#!/usr/bin/env bash
set -u
export PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return 0
}

run krun "$work/len-test.mpy" \
  --definition "$work/semantic-concrete-kompiled" \
  -cARGS='args(pyStr("😀"),pyStr(""))'
printf '%s\n' 'COMMAND: python3 -c print(len("😀"))'
python3 -c 'print(len("😀"))'
printf 'EXIT: %d\n' "$?"
