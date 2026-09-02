#!/usr/bin/env bash
set -u

log=/audit-output/evidence/04_adequacy.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

work=/tmp/audit-work/rebuild/candidate
definition="$work/verification-lemma-kompiled"

run kast "$work/solution.mpy" \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file "$work/submitted-solution.kore"

run kast \
  --expression solutionProgram \
  --definition "$definition" \
  --module BELOW-ZERO-COMMON \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file "$work/solutionProgram-macro.kore"

run cmp --silent "$work/submitted-solution.kore" "$work/solutionProgram-macro.kore"
run sha256sum "$work/submitted-solution.kore" "$work/solutionProgram-macro.kore"
run python3 /audit-output/evidence/compare_aux_bridge.py
run python3 /audit-output/evidence/adequacy_witness.py
