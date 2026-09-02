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
source_dir="$scratch/source"
build_dir="$scratch/build-final"
mkdir -p "$build_dir"

run test ! -e "$source_dir/semantic-kompiled" || exit $?
run test ! -e "$source_dir/verification-kompiled" || exit $?
run find -P "$source_dir" -maxdepth 1 -printf '%y\t%s\t%f\t%l\n' || exit $?
run rg -n '^[[:space:]]*claim\b' "$source_dir" -g '*.k' || exit $?

run kompile "$source_dir/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$build_dir/semantic-llvm-kompiled" \
  || exit $?

run kompile "$source_dir/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$build_dir/verification-haskell-kompiled" \
  || exit $?

concrete_status=0
run python3 /audit-output/evidence/concrete_semantics_compare.py \
  --definition "$build_dir/semantic-llvm-kompiled" \
  --program "$source_dir/solution.mpy" \
  --canonical "$scratch/trusted/canonical.py" \
  --solution "$source_dir/solution.py" \
  || concrete_status=$?

proof_status=0
run kprove "$source_dir/spec.k" \
  --definition "$build_dir/verification-haskell-kompiled" \
  --spec-module SPEC \
  || proof_status=$?

printf 'concrete_status=%d\n' "$concrete_status"
printf 'proof_status=%d\n' "$proof_status"
test "$concrete_status" -eq 0 && test "$proof_status" -eq 0
