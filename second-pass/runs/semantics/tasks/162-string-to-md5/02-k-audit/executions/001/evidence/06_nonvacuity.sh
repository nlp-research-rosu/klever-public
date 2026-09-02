#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/proof-162

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd "$scratch" || exit 2

run python3 -c \
  'from solution import string_to_md5; value=string_to_md5("a"); print(repr(value)); assert value != None'

run kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run

run kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
