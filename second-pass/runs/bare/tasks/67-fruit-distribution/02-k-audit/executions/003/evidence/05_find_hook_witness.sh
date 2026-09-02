#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/fruit67 || exit 99

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

run kompile find-test.k \
  --main-module FIND-TEST \
  --syntax-module FIND-TEST \
  --backend llvm \
  --output-definition find-test-llvm-kompiled || exit $?

run kompile find-test.k \
  --main-module FIND-TEST \
  --syntax-module FIND-TEST \
  --backend haskell \
  --output-definition find-test-haskell-kompiled || exit $?

run krun find-input.k --definition find-test-llvm-kompiled --output pretty
llvm_status=$?
run krun find-input.k --definition find-test-haskell-kompiled --output pretty
haskell_status=$?

echo 'WITNESS: in "5 apples and 6 oranges", searching for " " from index 2'
echo 'The absolute next-space index is 8.'
echo 'Candidate rule nextSpace(S,START) => START + findString(S," ",START)'
echo 'therefore produces 2+8=10 under the documented/LLVM absolute-index hook.'

[[ "$llvm_status" -eq 0 && "$haskell_status" -eq 0 ]]
