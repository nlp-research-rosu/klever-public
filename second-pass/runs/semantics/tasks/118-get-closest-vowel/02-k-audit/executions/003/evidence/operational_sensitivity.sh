#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/body-mutation || exit 90
overall=0

run_and_record() {
  local description=$1
  shift
  printf 'COMMAND: %s\n' "$description"
  "$@"
  local status=$?
  printf 'EXIT: %s\n' "$status"
  if (( status != 0 )); then overall=1; fi
}

printf '%s\n' 'MUTATION: getClosestBody base case Return(Str("")) -> Return(Str("X"))'
printf '%s\n' 'WITNESS: intended-domain English-letter input "bab"; actual mutant result "X"; claimed result "a"'

printf '%s\n' 'COMMAND: python3 py2mpy.py mutant-concrete.py > mutant-concrete.mpy'
python3 py2mpy.py mutant-concrete.py > mutant-concrete.mpy
status=$?
printf 'EXIT: %s\n' "$status"
if (( status != 0 )); then overall=1; fi

run_and_record \
  'python3 mutant-concrete.py' \
  python3 mutant-concrete.py

run_and_record \
  'krun mutant-concrete.mpy --definition /tmp/audit-work/reconstruction/audit-runtime-kompiled' \
  krun mutant-concrete.mpy \
    --definition /tmp/audit-work/reconstruction/audit-runtime-kompiled

run_and_record \
  'kompile verification.k --backend haskell --main-module HUMAN-EVAL-118-VERIFICATION --syntax-module MPY-SYNTAX --output-definition mutant-proof-kompiled' \
  kompile verification.k \
    --backend haskell \
    --main-module HUMAN-EVAL-118-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition mutant-proof-kompiled

run_and_record \
  'kprove spec-mutant-false.k --definition mutant-proof-kompiled --spec-module AUDIT-MUTANT-FALSE' \
  kprove spec-mutant-false.k \
    --definition mutant-proof-kompiled \
    --spec-module AUDIT-MUTANT-FALSE

run_and_record \
  'kprove spec-long.k --definition mutant-proof-kompiled --spec-module AUDIT-SPEC-LONG' \
  kprove spec-long.k \
    --definition mutant-proof-kompiled \
    --spec-module AUDIT-SPEC-LONG

exit "$overall"
