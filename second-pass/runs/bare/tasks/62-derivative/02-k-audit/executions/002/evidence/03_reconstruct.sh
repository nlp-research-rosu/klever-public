#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/reconstruction-62

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run kompile --version
run kprove --version
run krun --version

run kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  -o semantic-fresh-kompiled

run python3 /audit-output/evidence/03_semantics_differential.py

run kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  -o verification-fresh-kompiled

printf '%s\n' \
  'COMMAND: cmp <(kast solution.mpy --definition verification-fresh-kompiled --module VERIFICATION --sort Pgm --expand-macros --output kore) <(kast --expression solutionProgram --definition verification-fresh-kompiled --module VERIFICATION --sort Pgm --expand-macros --output kore)'
cmp \
  <(kast solution.mpy --definition verification-fresh-kompiled \
      --module VERIFICATION --sort Pgm --expand-macros --output kore) \
  <(kast --expression solutionProgram \
      --definition verification-fresh-kompiled \
      --module VERIFICATION --sort Pgm --expand-macros --output kore)
printf 'EXIT_STATUS: %d\n' "$?"

run kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC

run kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  --claims helper-correct

run kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  --claims derivative-empty

run kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  --claims derivative-nonempty
