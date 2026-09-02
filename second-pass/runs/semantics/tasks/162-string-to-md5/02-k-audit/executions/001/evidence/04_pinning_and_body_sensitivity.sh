#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/proof-162

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd "$scratch" || exit 2

run kast solution.submitted.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kast \
  --output-file /audit-output/evidence/04_submitted_program.kast

run kast solution-macro.term \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kast \
  --output-file /audit-output/evidence/04_claim_program.kast

run cmp -s \
  /audit-output/evidence/04_submitted_program.kast \
  /audit-output/evidence/04_claim_program.kast
run sha256sum \
  /audit-output/evidence/04_submitted_program.kast \
  /audit-output/evidence/04_claim_program.kast

run kprove spec-ground.k \
  --definition verification-kompiled \
  --spec-module SPEC-GROUND

run kompile verification-body-mutant.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutant-kompiled

run kprove spec-body-mutant.k \
  --definition verification-body-mutant-kompiled \
  --spec-module SPEC-BODY-MUTANT
