#!/usr/bin/env bash
set -euo pipefail

run_case() {
  local case_label=$1
  shift
  printf 'CASE: %s\n' "$case_label"
  printf 'INPUT:'
  printf ' %s' "$@"
  printf '\n'
  printf '%s\n' 'K_RESULT:'
  krun <(python3 make_case.py "$@") \
    --definition audit-semantic-kompiled \
    --output pretty
  printf '%s\n' 'PYTHON_RESULTS:'
  python3 -c '
import sys
from canonical import rolling_max as canonical
from solution import rolling_max as generated
values = [int(value) for value in sys.argv[1:]]
oracle = [max(values[:index + 1]) for index in range(len(values))]
print("canonical=", canonical(values))
print("generated=", generated(values))
print("oracle=", oracle)
assert canonical(values) == generated(values) == oracle
' "$@"
}

run_case empty
run_case singleton-negative -7
run_case first-then-less 2 1
run_case first-then-greater 1 2
run_case equal-boundary 2 2
run_case prompt 1 2 3 2 3 4 2
run_case all-negative -5 -9 -3 -4
run_case large-integers 100000000000000000000 -100000000000000000000 100000000000000000001
