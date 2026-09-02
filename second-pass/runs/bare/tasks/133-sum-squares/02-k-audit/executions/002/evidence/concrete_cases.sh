#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/candidate
definition="$work/semantic-fresh-kompiled"
program="$work/regenerated-solution.mpy"

run_case() {
  local label="$1"
  local expected="$2"
  local python_input="$3"
  local k_input="$4"
  local python_result
  local output
  local k_cell

  python_result="$(
    python3 - "$python_input" <<'PY'
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "trusted_canonical", "/tmp/audit-work/reference/canonical.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.sum_squares(eval(sys.argv[1], {"__builtins__": {}}, {})))
PY
  )"
  test "$python_result" = "$expected"

  output="$(krun "$program" --definition "$definition" -cARGS="$k_input")"
  k_cell="$(printf '%s\n' "$output" | sed -n '/<k>/,/<\/k>/p' | tr -d '[:space:]')"
  test "$k_cell" = "<k>intVal($expected)~>.K</k>"

  printf 'case=%s expected=%s python=%s k_cell=%s\n' \
    "$label" "$expected" "$python_result" "$k_cell"
}

run_case \
  empty \
  0 \
  '[]' \
  'listVal(nil)'

run_case \
  documented-integers \
  14 \
  '[1, 2, 3]' \
  'listVal(cons(intVal(1), cons(intVal(2), cons(intVal(3), nil))))'

run_case \
  documented-positive-fractions \
  29 \
  '[1.4, 4.2, 0]' \
  'listVal(cons(ratVal(14, ten), cons(ratVal(42, ten), cons(intVal(0), nil))))'

run_case \
  documented-negative-fraction \
  6 \
  '[-2.4, 1, 1]' \
  'listVal(cons(ratVal(-24, ten), cons(intVal(1), cons(intVal(1), nil))))'

run_case \
  around-zero-and-integers \
  3 \
  '[-0.1, 0.1, -1, 1]' \
  'listVal(cons(ratVal(-1, ten), cons(ratVal(1, ten), cons(intVal(-1), cons(intVal(1), nil)))))'

run_case \
  negative-ceiling-boundaries \
  2 \
  '[-1.1, -1.0, -0.9]' \
  'listVal(cons(ratVal(-11, ten), cons(ratVal(-10, ten), cons(ratVal(-9, ten), nil))))'

run_case \
  arbitrary-positive-denominator \
  1 \
  '[1 / 3, -1 / 3]' \
  'listVal(cons(ratVal(1, next(next(one))), cons(ratVal(-1, next(next(one))), nil)))'
