#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/131-digits
failures=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then failures=1; fi
  return 0
}

run_eval() {
  label=$1
  term=$2
  file="$scratch/inputs/static_${label}.mpy"
  printf '\n$ printf %q > %q\n' "$term" "$file"
  printf '%s\n' "$term" > "$file"
  printf '[exit 0]\n'
  run krun "$file" \
    --definition "$scratch/verification-fresh-kompiled" --output pretty
}

printf 'AUDIT STAGE 5: STATIC INVENTORY SUPPORTING EVIDENCE\n'
run nl -ba "$scratch/semantic.k"
run nl -ba "$scratch/verification.k"
run nl -ba "$scratch/spec.k"
run rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise)' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
run python3 /reference/py2mpy.py "$scratch/solution.py" --ast

printf '\nIntended-domain arithmetic witnesses:\n'
run_eval positive_division 'eval(BinOp("//", Int(235), Int(10)))'
run_eval positive_remainder 'eval(BinOp("%", Int(235), Int(10)))'

printf '\nDocumented out-of-domain Python-model limitation:\n'
run_eval negative_division 'eval(BinOp("//", Int(-3), Int(2)))'
run_eval negative_remainder 'eval(BinOp("%", Int(-3), Int(2)))'
run python3 -c 'print(-3 // 2); print(-3 % 2)'

printf '\nstage5_failures=%d\n' "$failures"
exit "$failures"
