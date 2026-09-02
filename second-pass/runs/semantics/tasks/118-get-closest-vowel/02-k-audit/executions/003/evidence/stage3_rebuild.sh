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
  if (( status != 0 )); then
    overall=1
  fi
}

printf '%s\n' 'COMMAND: python3 /reference/py2mpy.py audit-concrete.py > audit-concrete.mpy'
python3 /reference/py2mpy.py audit-concrete.py > audit-concrete.mpy
status=$?
printf 'EXIT: %s\n' "$status"
if (( status != 0 )); then overall=1; fi

run_and_record \
  'kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled' \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled

run_and_record \
  'krun audit-concrete.mpy --definition audit-runtime-kompiled' \
  krun audit-concrete.mpy --definition audit-runtime-kompiled

run_and_record \
  'kompile verification.k --backend haskell --main-module HUMAN-EVAL-118-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-proof-kompiled' \
  kompile verification.k \
    --backend haskell \
    --main-module HUMAN-EVAL-118-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-proof-kompiled

run_and_record \
  'kprove spec.k --definition audit-proof-kompiled --spec-module HUMAN-EVAL-118-SPEC' \
  kprove spec.k \
    --definition audit-proof-kompiled \
    --spec-module HUMAN-EVAL-118-SPEC

run_and_record \
  'kprove spec-empty.k --definition audit-proof-kompiled --spec-module AUDIT-SPEC-EMPTY' \
  kprove spec-empty.k \
    --definition audit-proof-kompiled \
    --spec-module AUDIT-SPEC-EMPTY

run_and_record \
  'kprove spec-one.k --definition audit-proof-kompiled --spec-module AUDIT-SPEC-ONE' \
  kprove spec-one.k \
    --definition audit-proof-kompiled \
    --spec-module AUDIT-SPEC-ONE

run_and_record \
  'kprove spec-two.k --definition audit-proof-kompiled --spec-module AUDIT-SPEC-TWO' \
  kprove spec-two.k \
    --definition audit-proof-kompiled \
    --spec-module AUDIT-SPEC-TWO

run_and_record \
  'kprove spec-long.k --definition audit-proof-kompiled --spec-module AUDIT-SPEC-LONG' \
  kprove spec-long.k \
    --definition audit-proof-kompiled \
    --spec-module AUDIT-SPEC-LONG

exit "$overall"
