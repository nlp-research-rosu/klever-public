#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/rebuild
LOG=/audit-output/evidence/03_rebuild.log
: > "$LOG"

run() {
  printf 'COMMAND: ' >> "$LOG"
  printf '%q ' "$@" >> "$LOG"
  printf '\n' >> "$LOG"
  "$@" >> "$LOG" 2>&1
  status=$?
  printf 'EXIT: %d\n\n' "$status" >> "$LOG"
  if [ "$status" -ne 0 ]; then
    exit "$status"
  fi
}

cd "$WORK" || exit 1

run find . -maxdepth 2 -type d -name '*-kompiled' -print
run python3 /audit-output/evidence/03_make_concrete_tests.py \
  solution.mpy concrete-tests.mpy
run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
run krun concrete-tests.mpy \
  --definition runtime-audit-kompiled \
  --output none
run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled

printf '%s\n' \
  'COMMAND: kast --definition verification-audit-kompiled --module VERIFICATION --sort Module --expand-macros --output kore solution.mpy > parsed-solution.kore' \
  >> "$LOG"
kast --definition verification-audit-kompiled --module VERIFICATION \
  --sort Module --expand-macros --output kore solution.mpy \
  > parsed-solution.kore 2>> "$LOG"
status=$?
printf 'EXIT: %d\n\n' "$status" >> "$LOG"
[ "$status" -eq 0 ] || exit "$status"

printf '%s\n' \
  'COMMAND: kast --definition verification-audit-kompiled --module VERIFICATION --sort Module --expand-macros --output kore --expression solutionProgram > macro-solution.kore' \
  >> "$LOG"
kast --definition verification-audit-kompiled --module VERIFICATION \
  --sort Module --expand-macros --output kore --expression solutionProgram \
  > macro-solution.kore 2>> "$LOG"
status=$?
printf 'EXIT: %d\n\n' "$status" >> "$LOG"
[ "$status" -eq 0 ] || exit "$status"

run cmp -s parsed-solution.kore macro-solution.kore
run sha256sum parsed-solution.kore macro-solution.kore
