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

run kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  -o semantic-audit-kompiled

run python3 /audit-output/evidence/03_semantics_differential.py \
  /tmp/audit-work/reconstruction-62/semantic-audit-kompiled

run kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  -o verification-audit-kompiled

printf '%s\n' \
  'COMMAND: cmp <(kast solution.mpy --definition verification-audit-kompiled --module VERIFICATION --sort Pgm --expand-macros --output kore) <(kast --expression solutionProgram --definition verification-audit-kompiled --module VERIFICATION --sort Pgm --expand-macros --output kore)'
cmp \
  <(kast solution.mpy --definition verification-audit-kompiled \
      --module VERIFICATION --sort Pgm --expand-macros --output kore) \
  <(kast --expression solutionProgram \
      --definition verification-audit-kompiled \
      --module VERIFICATION --sort Pgm --expand-macros --output kore)
printf 'EXIT_STATUS: %d\n' "$?"

# All three target claims.
run kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC

# Independently selected helper target.
run kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims helper-correct

# Independently selected empty entry target.
run kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims derivative-empty

# Independently selected nonempty entry target with its explicit helper
# dependency retained in the selected claim set.
run kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims helper-correct,derivative-nonempty
