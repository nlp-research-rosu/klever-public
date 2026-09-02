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

run kprove spec-direct-program.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-DIRECT-PROGRAM \
  --dry-run

run kprove spec-direct-program.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-DIRECT-PROGRAM
