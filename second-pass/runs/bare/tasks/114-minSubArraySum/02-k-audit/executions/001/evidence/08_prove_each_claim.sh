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

run kprove spec-labeled.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.prefix-helper

run kprove spec-labeled.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.target-call

run timeout --signal=INT 20s kprove spec-labeled.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry
