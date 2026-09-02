#!/usr/bin/env bash
set -uo pipefail

overall=0
run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
  return 0
}

scratch=/tmp/audit-work/46-fib4
cd "$scratch" || exit 2

printf 'AUDIT STAGE 3: clean definitions, concrete execution, individual claims\n'
run find "$scratch" -maxdepth 2 -printf '%y %p -> %l\n'
run kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition semantic-llvm-kompiled
run kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition semantic-haskell-kompiled
run python3 /audit-output/evidence/semantic_crosscheck.py

claims=(
  SPEC.fib4-spec-link
  SPEC.loop-correct
  SPEC.fib4-inductive-init
  SPEC.fib4-base-0
  SPEC.fib4-base-1
  SPEC.fib4-base-2
  SPEC.fib4-base-3
  SPEC.fib4-seven
)

for claim in "${claims[@]}"; do
  run kprove spec.k \
    --definition semantic-haskell-kompiled \
    --spec-module SPEC \
    --claims "$claim"
done

exit "$overall"
