#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit_status] %d\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/71-triangle-area
concrete="$scratch/build/concrete-haskell-kompiled"
proof="$scratch/build/proof-kompiled"
overall=0

printf 'Generated-semantics Haskell reconstruction and false-conclusion witness\n'

run kompile \
  --backend haskell \
  "$scratch/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$concrete" || overall=1

run krun "$scratch/solution.mpy" \
  -cARGS='Args(VInt(3), VInt(4), VInt(5))' \
  --definition "$concrete" \
  --output pretty || overall=1

run krun "$scratch/solution.mpy" \
  -cARGS='Args(VInt(1), VInt(2), VInt(3))' \
  --definition "$concrete" \
  --output pretty || overall=1

run python3 /audit-output/evidence/python_semantics_oracle.py || overall=1

# A concrete false-conclusion witness for the exact-rational replacement of
# CPython floating arithmetic.  Both the prompt and formal valid-triangle
# precondition include this unbounded positive integer input.
run krun "$scratch/solution.mpy" \
  -cARGS='Args(VInt(10000000000000000), VInt(10000000000000000), VInt(1))' \
  --definition "$concrete" \
  --output pretty || overall=1

run kprove "$scratch/precision-witness-spec.k" \
  --definition "$proof" \
  --spec-module PRECISION-WITNESS-SPEC \
  --claims PRECISION-WITNESS-SPEC.precision-loss-valid \
  --smt-timeout 10000 || overall=1

printf '\n[script_exit_status] %d\n' "$overall"
exit "$overall"
