#!/usr/bin/env bash
set +e

record() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return 0
}

src=/tmp/audit-work/47-median/candidate-src
definition=/tmp/audit-work/47-median/build/proof-kompiled

record python3 /audit-output/evidence/stage4-witnesses.py
record kprove "$src/spec-body-sensitivity.k" \
  --definition "$definition" \
  --spec-module SPEC-BODY-SENSITIVITY
