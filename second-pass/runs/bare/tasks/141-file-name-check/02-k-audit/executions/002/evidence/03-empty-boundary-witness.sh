#!/usr/bin/env bash
set -u -o pipefail

SCRATCH=/tmp/audit-work/141-file-name-check
cd "$SCRATCH" || exit 1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 -c '
from solution import file_name_check as generated
from canonical import file_name_check as canonical
print("generated:", generated(""))
print("canonical:", canonical(""))
assert generated("") == canonical("") == "No"
'

run krun \
  solution.mpy \
  --definition audit-verification-kompiled \
  '-cINPUT=""'
haskell_status=$?

run krun \
  solution.mpy \
  --definition audit-semantics-kompiled \
  '-cINPUT=""'
llvm_status=$?

printf 'haskell_status=%d llvm_status=%d\n' "$haskell_status" "$llvm_status"
if [ "$haskell_status" -eq 0 ] && [ "$llvm_status" -ne 0 ]; then
  printf 'BACKEND DIVERGENCE REPRODUCED\n'
  exit 0
fi
printf 'EXPECTED DIVERGENCE NOT REPRODUCED\n'
exit 1
