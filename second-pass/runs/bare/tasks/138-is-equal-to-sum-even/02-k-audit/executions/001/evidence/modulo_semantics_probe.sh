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
definition=/tmp/audit-work/review-138/build/semantic-kompiled

run krun "$source_dir/probe-modulo.mpy" \
  --definition "$definition" \
  -cN=-3
run python3 -c 'print(-3 % 2)'

run krun "$source_dir/probe-modulo-negative-divisor.mpy" \
  --definition "$definition" \
  -cN=3
run python3 -c 'print(3 % -2)'
