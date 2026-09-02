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

printf 'Emit compiled claim and parsed ground constructor AST:\n'
run_in_work kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC \
  --dry-run \
  --emit-json-spec spec-compiled.json \
  --output kore
run_in_work kast solution.mpy \
  --definition fresh-verification-kompiled \
  --module MPY-SYNTAX \
  --sort Program \
  --output json \
  --output-file solution-ast.json

printf '\nConstructor-level unification:\n'
run python3 /audit-output/evidence/04_program_pinning.py

printf '\nEntry claim precondition/postcondition source:\n'
run nl -ba /tmp/audit-work/k-proof/spec.k
