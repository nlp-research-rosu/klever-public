#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf '[exit %d]\n' "$status"
  return "$status"
}

set -e
source_dir=/tmp/audit-work/review-138/candidate-src
definition=/tmp/audit-work/review-138/build/verification-kompiled

run cmp -s \
  "$source_dir/spec-modulo-false.k" \
  /audit-output/evidence/spec-modulo-false.k
run python3 -c 'print(-3 % 2)'
run kprove "$source_dir/spec-modulo-false.k" \
  --definition "$definition" \
  --spec-module SPEC-MODULO-FALSE
