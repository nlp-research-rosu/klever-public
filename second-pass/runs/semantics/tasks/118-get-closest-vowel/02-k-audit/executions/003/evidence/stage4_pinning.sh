#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 90
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

run_and_record \
  'kast body-from-solution.mpy --definition audit-proof-kompiled --module MPY-SYNTAX --sort Stmts --output kore --output-file body-from-solution.kore' \
  kast body-from-solution.mpy \
    --definition audit-proof-kompiled \
    --module MPY-SYNTAX \
    --sort Stmts \
    --output kore \
    --output-file body-from-solution.kore

run_and_record \
  'kast body-from-verification.mpy --definition audit-proof-kompiled --module MPY-SYNTAX --sort Stmts --output kore --output-file body-from-verification.kore' \
  kast body-from-verification.mpy \
    --definition audit-proof-kompiled \
    --module MPY-SYNTAX \
    --sort Stmts \
    --output kore \
    --output-file body-from-verification.kore

run_and_record \
  'cmp body-from-solution.kore body-from-verification.kore' \
  cmp body-from-solution.kore body-from-verification.kore

run_and_record \
  'sha256sum body-from-solution.kore body-from-verification.kore' \
  sha256sum body-from-solution.kore body-from-verification.kore

run_and_record \
  'kprove spec-ground.k --definition audit-proof-kompiled --spec-module AUDIT-SPEC-GROUND' \
  kprove spec-ground.k \
    --definition audit-proof-kompiled \
    --spec-module AUDIT-SPEC-GROUND

run_and_record \
  'python3 /audit-output/evidence/ground_compare.py' \
  python3 /audit-output/evidence/ground_compare.py

exit "$overall"
