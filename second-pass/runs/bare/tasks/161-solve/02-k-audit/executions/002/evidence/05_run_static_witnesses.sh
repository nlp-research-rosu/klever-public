#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/k-proof

run_in_work() {
  printf '+ (cd %q &&' "$WORK"
  printf ' %q' "$@"
  printf ')\n'
  (
    cd "$WORK" || exit 125
    "$@"
  )
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Full source inventory with line numbers:\n'
run nl -ba /tmp/audit-work/k-proof/semantic.k
run nl -ba /tmp/audit-work/k-proof/verification.k
run nl -ba /tmp/audit-work/k-proof/spec.k

printf '\nAll local declaration/rule/claim headers:\n'
run rg -n \
  '^[[:space:]]*(module|endmodule|imports|syntax|configuration|rule|claim)' \
  /tmp/audit-work/k-proof/semantic.k \
  /tmp/audit-work/k-proof/verification.k \
  /tmp/audit-work/k-proof/spec.k

printf '\nCopy reviewer witness terms and body mutation into scratch:\n'
run cp \
  /audit-output/evidence/05_witness-filter-false.mpy \
  /audit-output/evidence/05_witness-swapcase-arg.mpy \
  /audit-output/evidence/spec-body-mutation.k \
  "$WORK/"

printf '\nIndependent Python source-language outcomes:\n'
run python3 /audit-output/evidence/05_semantics_witnesses.py

printf '\nFalse semantic conclusion witness 1: ignored generator filter.\n'
printf 'The K rule returns swapCase(\"a\") = \"A\"; Python returns \"a\".\n'
run_in_work krun 05_witness-filter-false.mpy \
  --definition fresh-semantic-kompiled \
  -cINPUT='pstr("a")'

printf '\nFalse semantic conclusion witness 2: ignored swapcase argument.\n'
printf 'The K rule returns \"A\"; Python raises TypeError.\n'
run_in_work krun 05_witness-swapcase-arg.mpy \
  --definition fresh-semantic-kompiled \
  -cINPUT='pstr("a")'

printf '\nMaterial body-sensitivity mutation parses successfully:\n'
run_in_work kprove spec-body-mutation.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --dry-run

printf '\nMaterial false source theorem under candidate semantics:\n'
run_in_work kprove spec-body-mutation.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
