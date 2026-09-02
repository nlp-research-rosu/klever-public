#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/48-is-palindrome
definition="$scratch/build-final/verification-haskell-kompiled"
mutation="$scratch/mutations/spec-vacuity-audit.k"
proof_output="$scratch/mutations/spec-vacuity-audit.out"

run cmp -s "$mutation" /audit-output/evidence/spec-vacuity-audit.k || exit $?

run kprove "$mutation" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run \
  || exit $?

printf '$ kprove %q --definition %q --spec-module %q\n' \
  "$mutation" \
  "$definition" \
  SPEC-VACUITY-AUDIT
set -o pipefail
kprove "$mutation" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  2>&1 | tee "$proof_output"
mutation_status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$mutation_status"

if test "$mutation_status" -eq 0
then
  printf 'unexpected_mutation_success=true\n'
  exit 1
fi

run rg -n \
  'WarnStuckClaimState|implication check|doesn.t unify|cannot be rewritten further|PyBool' \
  "$proof_output" \
  || exit $?

run krun "$scratch/source/solution.mpy" \
  --definition "$scratch/build-final/semantic-llvm-kompiled" \
  '-cFUNCTION="is_palindrome"' \
  '-cARG=""' \
  --output-file "$scratch/mutations/empty-witness.out" \
  || exit $?
run rg -n 'PyBool[[:space:]]*\([[:space:]]*true' \
  "$scratch/mutations/empty-witness.out" \
  || exit $?
run python3 -c \
  'import importlib.util; p="/tmp/audit-work/48-is-palindrome/source/solution.py"; s=importlib.util.spec_from_file_location("vacuity_solution",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print({"input":"", "result":m.is_palindrome("")})' \
  || exit $?

printf 'mutation_build_success=true\n'
printf 'mutation_expected_failure=true\n'
printf 'satisfying_false-witness_input=""\n'
