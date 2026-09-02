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
concrete="$scratch/build/concrete-kompiled"
proof="$scratch/build/proof-kompiled"
overall=0

printf 'Audit stage 3: clean semantics and proof reconstruction\n'
run kompile --version || overall=1
run krun --version || overall=1
run kprove --version || overall=1
run mkdir -p "$scratch/build" || overall=1

run kompile \
  --backend llvm \
  "$scratch/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$concrete" || overall=1

run kompile \
  --backend haskell \
  "$scratch/verification.k" \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition "$proof" || overall=1

run python3 /audit-output/evidence/python_semantics_oracle.py || overall=1

for case_name in \
  valid-example \
  valid-rounding \
  valid-near-boundary \
  invalid-first-equality \
  invalid-second-equality \
  invalid-third-equality \
  zero
do
  case "$case_name" in
    valid-example) args='Args(VInt(3), VInt(4), VInt(5))' ;;
    valid-rounding) args='Args(VInt(2), VInt(2), VInt(2))' ;;
    valid-near-boundary) args='Args(VInt(2), VInt(2), VInt(3))' ;;
    invalid-first-equality) args='Args(VInt(1), VInt(2), VInt(3))' ;;
    invalid-second-equality) args='Args(VInt(1), VInt(3), VInt(2))' ;;
    invalid-third-equality) args='Args(VInt(3), VInt(2), VInt(1))' ;;
    zero) args='Args(VInt(0), VInt(0), VInt(0))' ;;
  esac
  printf '\nConcrete case: %s\n' "$case_name"
  run krun "$scratch/solution.mpy" \
    -cARGS="$args" \
    --definition "$concrete" \
    --output pretty || overall=1
done

# The source contract does not state an integer bound.  This valid integer
# witness exercises the generated semantics where CPython raises on / 2.
huge=1$(printf '%0400d' 0)
run krun "$scratch/solution.mpy" \
  -cARGS="Args(VInt($huge), VInt($huge), VInt($huge))" \
  --definition "$concrete" \
  --output pretty || overall=1

# The natural-language contract says "lengths" without an integer-only
# restriction.  Record how the submitted semantics handles a valid float case.
run krun "$scratch/solution.mpy" \
  -cARGS='Args(VFloat(0.5), VFloat(0.5), VFloat(0.75))' \
  --definition "$concrete" \
  --output pretty

printf '\nOriginal all-claims target\n'
run kprove "$scratch/spec.k" \
  --definition "$proof" \
  --spec-module SPEC \
  --smt-timeout 10000 || overall=1

for label in \
  example-3-4-5 \
  example-5-12-13 \
  example-2-2-2 \
  valid-universal \
  invalid-first \
  invalid-second \
  invalid-third
do
  printf '\nIndividually selected positive claim: %s\n' "$label"
  run kprove "$scratch/spec-labeled.k" \
    --definition "$proof" \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.$label" \
    --smt-timeout 10000 || overall=1
done

printf '\n[script_exit_status] %d\n' "$overall"
exit "$overall"
