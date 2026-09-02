#!/usr/bin/env bash
set -u

log=/audit-output/evidence/06_adequacy_and_pinning.log
exec > >(tee "$log") 2>&1
scratch=/tmp/audit-work/133-sum-squares
capture="$scratch/.audit-command-output.log"

run_bounded() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$capture" 2>&1
  status=$?
  lines=$(wc -l <"$capture")
  bytes=$(wc -c <"$capture")
  printf 'OUTPUT_LINES: %d OUTPUT_BYTES: %d\n' "$lines" "$bytes"
  sed -n '1,240p' "$capture"
  if (( lines > 240 )); then
    printf '[... bounded log omitted %d trailing lines ...]\n' "$((lines - 240))"
  fi
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'COMMAND: cd %q\n' "$scratch"
cd "$scratch"
printf 'EXIT_STATUS: %d\n' "$?"

printf '\nCOMMAND: kast solution.mpy --definition audit-semantic-kompiled > solution.kast\n'
kast solution.mpy --definition audit-semantic-kompiled > solution.kast
printf 'EXIT_STATUS: %d\n' "$?"
printf '\nCOMMAND: kast spec-program.mpy --definition audit-semantic-kompiled > spec-program.kast\n'
kast spec-program.mpy --definition audit-semantic-kompiled > spec-program.kast
printf 'EXIT_STATUS: %d\n' "$?"
run_bounded cmp -s solution.kast spec-program.kast
run_bounded sha256sum solution.kast spec-program.kast
run_bounded kprove spec-loop-ground.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-LOOP-GROUND
run_bounded python3 /audit-output/evidence/06_adequacy_witnesses.py
