#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/reviewer-002/scratch
LOG=/audit-output/evidence/04-adequacy-pinning.log
: > "$LOG"

run() {
  printf '$ (cd %s &&' "$SCRATCH" >> "$LOG"
  printf ' %q' "$@" >> "$LOG"
  printf ')\n' >> "$LOG"
  (
    cd "$SCRATCH" || exit 125
    "$@"
  ) >> "$LOG" 2>&1
  command_status=$?
  printf 'EXIT: %s\n\n' "$command_status" >> "$LOG"
  return 0
}

run kast solution.mpy \
  --definition reviewer-verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file submitted-module.kore
run kast module-from-proof-macro.mpy \
  --definition reviewer-verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file proof-macro-module.kore
run cmp -l submitted-module.kore proof-macro-module.kore
run sha256sum submitted-module.kore proof-macro-module.kore
run kprove spec-pinning.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-PINNING \
  --claims SPEC-PINNING.module-load-pins-closure \
  --output pretty
run python3 /audit-output/evidence/claim_substitution.py
run rg -n -F \
  -e fizzBuzzSpec \
  -e fizzBuzzAcc \
  -e countSevensAcc \
  -e 'Call(FIZZ-BUZZ-CLOSURE' \
  spec.k verification.k
