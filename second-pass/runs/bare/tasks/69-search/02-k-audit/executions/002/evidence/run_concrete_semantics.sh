#!/usr/bin/env bash
set -euo pipefail
set -x

audit_case_root=/tmp/audit-work/69-search
cd "$audit_case_root"

run_case() {
  local label=$1
  local python_literal=$2
  local k_input=$3
  echo "CASE $label"
  python3 -c "from solution import search; print('PYTHON_RESULT', search($python_literal))"
  krun solution.mpy \
    --definition reviewer-semantic-kompiled \
    -cINPUT="$k_input" |
    sed -n '/<result>/,/<\/result>/p'
}

run_case empty '[]' 'VList(.Ints)'
run_case singleton_qualifies '[1]' 'VList(cons(1, .Ints))'
run_case singleton_rejected '[2]' 'VList(cons(2, .Ints))'
run_case equal_frequency '[2, 2]' 'VList(cons(2, cons(2, .Ints)))'
run_case greater_frequency '[2, 2, 2]' 'VList(cons(2, cons(2, cons(2, .Ints))))'
run_case two_qualifiers '[1, 2, 2, 3, 3, 3]' \
  'VList(cons(1, cons(2, cons(2, cons(3, cons(3, cons(3, .Ints)))))))'
run_case prompt_one '[4, 1, 2, 2, 3, 1]' \
  'VList(cons(4, cons(1, cons(2, cons(2, cons(3, cons(1, .Ints)))))))'
run_case prompt_three '[5, 5, 4, 4, 4]' \
  'VList(cons(5, cons(5, cons(4, cons(4, cons(4, .Ints))))))'
