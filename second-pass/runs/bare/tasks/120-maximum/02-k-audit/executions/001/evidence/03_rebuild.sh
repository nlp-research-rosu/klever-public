#!/usr/bin/env bash
set -u

work=/tmp/audit-work/120-maximum-audit/src
overall_status=0

run_command() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n\n' "$command_status"
  if (( command_status != 0 )); then
    overall_status=1
  fi
}

cd "$work" || exit 1

printf 'K TOOLCHAIN\n'
run_command kompile --version
run_command kprove --version
run_command krun --version

printf 'SCRATCH SOURCE TREE BEFORE BUILD\n'
find "$work" -maxdepth 2 -printf '%y %p -> %l\n' | sort
printf 'FIND_EXIT_STATUS: %d\n\n' "${PIPESTATUS[0]}"

printf 'FRESH CONCRETE DEFINITION (LLVM)\n'
run_command \
  kompile semantic.k \
    --backend llvm \
    --main-module MAXIMUM \
    --syntax-module MAXIMUM-SYNTAX \
    --output-definition concrete-kompiled

printf 'FRESH PROOF DEFINITION (HASKELL)\n'
run_command \
  kompile verification.k \
    --backend haskell \
    --main-module MAXIMUM-VERIFICATION \
    --syntax-module MAXIMUM-SYNTAX \
    --output-definition proof-kompiled

printf 'ALL POSITIVE TARGET CLAIMS\n'
run_command \
  kprove spec.k \
    --definition proof-kompiled \
    --spec-module MAXIMUM-SPEC

printf 'OVERALL_EXIT_STATUS: %d\n' "$overall_status"
exit "$overall_status"
