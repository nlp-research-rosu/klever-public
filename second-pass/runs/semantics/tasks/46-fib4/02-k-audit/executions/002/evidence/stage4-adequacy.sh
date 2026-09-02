#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work/46-fib4-review || exit 99

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/extract_claim_program.py
run kast --definition reviewer-verification-kompiled \
  --module MPY-SYNTAX --sort Module --output json \
  --output-file solution.kast.json solution.mpy
run kast --definition reviewer-verification-kompiled \
  --module MPY-SYNTAX --sort Module --output json \
  --output-file claim-executed.kast.json claim-executed.mpy
run cmp -s solution.kast.json claim-executed.kast.json
run sha256sum solution.kast.json claim-executed.kast.json
run python3 /audit-output/evidence/check_claim_scope.py
run rg -n -e claim -e 'Call\(Name\("fib4"\)' -e requires -e ensures spec.k
