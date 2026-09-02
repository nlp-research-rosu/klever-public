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

run kprove spec-prefix-only.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-PREFIX-ONLY

run kprove spec-target-suite.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-TARGET-SUITE

run kprove spec-labeled.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-LABELED
