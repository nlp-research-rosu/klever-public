#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run kompile \
  --backend haskell \
  semantic-no-fused.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-no-fused-kompiled

compare_case() {
  local label="$1"
  local args="$2"
  local with_bridge="/tmp/audit-work/114-minSubArraySum-audit/${label}-with-bridge.out"
  local without_bridge="/tmp/audit-work/114-minSubArraySum-audit/${label}-without-bridge.out"

  run krun solution.mpy \
    --definition semantic-audit-kompiled \
    '-cENTRY="minSubArraySum"' \
    "-cARGS=$args" \
    --output pretty
  krun solution.mpy \
    --definition semantic-audit-kompiled \
    '-cENTRY="minSubArraySum"' \
    "-cARGS=$args" \
    --output pretty > "$with_bridge"
  printf '[capture-with-bridge exit %d]\n' "$?"

  run krun solution.mpy \
    --definition semantic-no-fused-kompiled \
    '-cENTRY="minSubArraySum"' \
    "-cARGS=$args" \
    --output pretty
  krun solution.mpy \
    --definition semantic-no-fused-kompiled \
    '-cENTRY="minSubArraySum"' \
    "-cARGS=$args" \
    --output pretty > "$without_bridge"
  printf '[capture-without-bridge exit %d]\n' "$?"

  run cmp -s "$with_bridge" "$without_bridge"
}

compare_case \
  singleton \
  'pyList(cons(7, nil))'

compare_case \
  nonsingleton \
  'pyList(cons(4, cons(-6, cons(2, cons(-5, cons(7, nil))))))'
