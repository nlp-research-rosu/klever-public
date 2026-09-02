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
witness_dir="$scratch/witnesses"

run nl -ba "$scratch/source/semantic.k" || exit $?
run nl -ba "$scratch/source/verification.k" || exit $?
run nl -ba "$scratch/source/spec.k" || exit $?
run sed -n 1681,1765p /usr/include/kframework/builtin/domains.md || exit $?
run rg -n \
  '^[[:space:]]*(syntax|rule|claim|configuration)\b|\[(function|total|functional|simplification|priority|anywhere|macro)' \
  "$scratch/source/semantic.k" \
  "$scratch/source/verification.k" \
  "$scratch/source/spec.k" \
  || exit $?

run cmp -s \
  "$witness_dir/spec-unicode-formal-expected.k" \
  /audit-output/evidence/spec-unicode-formal-expected.k \
  || exit $?

run kprove "$witness_dir/spec-unicode-formal-expected.k" \
  --definition "$definition" \
  --spec-module SPEC-UNICODE-FORMAL-EXPECTED \
  --dry-run \
  || exit $?
run kprove "$witness_dir/spec-unicode-formal-expected.k" \
  --definition "$definition" \
  --spec-module SPEC-UNICODE-FORMAL-EXPECTED \
  || exit $?

run krun "$scratch/source/solution.mpy" \
  --definition "$scratch/build-final/semantic-llvm-kompiled" \
  '-cFUNCTION="is_palindrome"' \
  '-cARG="🙂a🙂"' \
  --output-file "$witness_dir/unicode-verbatim-config.out" \
  || exit $?
run rg -n 'PyBool[[:space:]]*\([[:space:]]*false' \
  "$witness_dir/unicode-verbatim-config.out" \
  || exit $?
run python3 -c \
  's="🙂a🙂"; print({"input": s, "canonical_result": s == s[::-1]})' \
  || exit $?
printf 'classification=runtime-input-encoding bridge limitation; no local rule marked unsound\n'
