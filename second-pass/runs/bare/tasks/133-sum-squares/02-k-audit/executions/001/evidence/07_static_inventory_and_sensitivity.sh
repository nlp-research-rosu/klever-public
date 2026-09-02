#!/usr/bin/env bash
set -u

log=/audit-output/evidence/07_static_inventory_and_sensitivity.log
exec > >(tee "$log") 2>&1
scratch=/tmp/audit-work/133-sum-squares
capture="$scratch/.audit-command-output.log"

run_bounded() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$capture" 2>&1
  status=$?
  lines=$(wc -l <"$capture")
  bytes=$(wc -c <"$capture")
  printf 'OUTPUT_LINES: %d OUTPUT_BYTES: %d\n' "$lines" "$bytes"
  if (( lines <= 260 )); then
    sed -n '1,260p' "$capture"
  else
    sed -n '1,200p' "$capture"
    printf '[... bounded log omitted %d middle lines ...]\n' "$((lines - 260))"
    tail -60 "$capture"
  fi
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'COMMAND: cd %q\n' "$scratch"
cd "$scratch"
printf 'EXIT_STATUS: %d\n' "$?"

run_bounded find . -maxdepth 1 -type f -name '*.k' -printf '%f\n'
run_bounded nl -ba semantic.k
run_bounded nl -ba verification.k
run_bounded nl -ba spec.k
run_bounded rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim|imports|requires)|\\[(function|total|functional|simplification|concrete|priority|owise)' \
  semantic.k verification.k spec.k
run_bounded rg -n \
  '\\[(functional|simplification|concrete|priority|owise)|\\[priority|opaque' \
  semantic.k verification.k spec.k
run_bounded krun solution-mutated-body.mpy \
  --definition audit-semantic-kompiled \
  '-cARGS=listVal(cons(intVal(1), cons(intVal(2), cons(intVal(3), nil))))'
run_bounded krun unsupported-operator.mpy \
  --definition audit-semantic-kompiled \
  '-cARGS=listVal(nil)'
