#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/proof-audit || exit 97

printf '[exact AST pinning]\n'
run python3 /audit-output/evidence/ast_pin_check.py

printf '[copy body-sensitivity artifacts into scratch]\n'
run cp /audit-output/evidence/verification-body-mutant.k ./verification-body-mutant.k
run cp /audit-output/evidence/spec-body-sensitivity.k ./spec-body-sensitivity.k
run cmp -s /audit-output/evidence/verification-body-mutant.k ./verification-body-mutant.k
run cmp -s /audit-output/evidence/spec-body-sensitivity.k ./spec-body-sensitivity.k

printf '[fresh mutant definition]\n'
run kompile verification-body-mutant.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutant-kompiled

printf '[changed body must fail the real result obligation]\n'
run kprove spec-body-sensitivity.k \
  --definition verification-body-mutant-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY
