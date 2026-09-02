#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

python3 - <<'PY'
from solution import triples_sum_to_zero

tests = [
    ([1, 3, 5, 0], False),
    ([1, 3, -2, 1], True),
    ([1, 2, 3, 7], False),
    ([2, 4, -5, 3, 9, 7], True),
    ([1], False),
    ([], False),
    ([0, 0, 0], True),
    ([0, 0], False),
]
for values, expected in tests:
    actual = triples_sum_to_zero(values)
    assert actual is expected, (values, expected, actual)
print("CPython examples and edge cases passed")
PY

kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition .kbuild

run_case() {
  local ints="$1"
  local expected="$2"
  local state
  local result_line
  state="$(krun solution.mpy \
    --definition .kbuild \
    -cINPUT="VList(${ints})" \
    --output pretty)"
  result_line="$(printf '%s\n' "$state" | rg 'result \( VBool')"
  if [[ "$result_line" != *"VBool ( ${expected} )"* ]]; then
    printf 'Unexpected K result for [%s]: %s\n' "$ints" "$result_line" >&2
    return 1
  fi
  printf 'K execution [%s] -> %s\n' "$ints" "$expected"
}

run_case '1 ; 3 ; 5 ; 0 ; .Ints' false
run_case '1 ; 3 ; -2 ; 1 ; .Ints' true
run_case '1 ; 2 ; 3 ; 7 ; .Ints' false
run_case '2 ; 4 ; -5 ; 3 ; 9 ; 7 ; .Ints' true
run_case '1 ; .Ints' false
run_case '.Ints' false
run_case '0 ; 0 ; 0 ; .Ints' true
run_case '0 ; 0 ; .Ints' false

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition .kprove

kprove spec.k \
  --definition .kprove \
  --spec-module SPEC \
  --output pretty
