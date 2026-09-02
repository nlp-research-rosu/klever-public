#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$work" || exit 1

run_kast() {
  local input=$1
  local output=$2
  local log=$3
  printf 'COMMAND: kast %s --definition verification-base-kompiled --module BELOW-ZERO-COMMON --sort Module --expand-macros --output kore > %s\n' \
    "$input" "$output" | tee "$log"
  kast "$input" \
    --definition verification-base-kompiled \
    --module BELOW-ZERO-COMMON \
    --sort Module \
    --expand-macros \
    --output kore > "$output" 2>> "$log"
  local status=$?
  printf 'EXIT_STATUS: %s\n' "$status" | tee -a "$log"
  return "$status"
}

run_kast solution.mpy parsed-submitted-program.kore \
  "$evidence/04a-kast-submitted.log" || exit $?
run_kast claimed-program.mpy parsed-claimed-program.kore \
  "$evidence/04b-kast-claimed.log" || exit $?

printf 'COMMAND: cmp parsed-submitted-program.kore parsed-claimed-program.kore\n' |
  tee "$evidence/04c-program-term-cmp.log"
cmp parsed-submitted-program.kore parsed-claimed-program.kore \
  2>&1 | tee -a "$evidence/04c-program-term-cmp.log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$status" |
  tee -a "$evidence/04c-program-term-cmp.log"
sha256sum parsed-submitted-program.kore parsed-claimed-program.kore |
  tee -a "$evidence/04c-program-term-cmp.log"
exit "$status"
