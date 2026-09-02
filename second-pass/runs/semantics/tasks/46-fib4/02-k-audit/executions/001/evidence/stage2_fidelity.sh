#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/46-fib4-audit

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

run bash -c \
  'python3 /tmp/audit-work/46-fib4-audit/reference/py2mpy.py /tmp/audit-work/46-fib4-audit/candidate-src/solution.py > /tmp/audit-work/46-fib4-audit/candidate-src/regenerated-solution.mpy'
run cmp -s "$scratch/candidate-src/regenerated-solution.mpy" \
  "$scratch/candidate-src/solution.mpy"
run sha256sum "$scratch/candidate-src/regenerated-solution.mpy" \
  "$scratch/candidate-src/solution.mpy"

run python3 /audit-output/evidence/stage2_differential.py
