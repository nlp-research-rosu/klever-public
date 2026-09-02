#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0
run kast \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --module MPY-SYNTAX \
  --sort Program \
  --input program \
  --output kore \
  --output-file /tmp/audit-work/submitted-solution.kore \
  /tmp/audit-work/candidate-src/solution.mpy || overall=1

run kast \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --module MPY-SYNTAX \
  --sort Program \
  --input program \
  --output kore \
  --output-file /tmp/audit-work/solutionProgram-expanded.kore \
  /audit-output/evidence/solutionProgram-expanded.mpy || overall=1

run cmp -s \
  /tmp/audit-work/submitted-solution.kore \
  /tmp/audit-work/solutionProgram-expanded.kore || overall=1

run sha256sum \
  /tmp/audit-work/submitted-solution.kore \
  /tmp/audit-work/solutionProgram-expanded.kore

run python3 /audit-output/evidence/ground_witnesses.py || overall=1

printf '\n[script exit %d]\n' "$overall"
exit "$overall"
