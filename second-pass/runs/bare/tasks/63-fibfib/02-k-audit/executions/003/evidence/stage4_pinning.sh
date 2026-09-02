#!/usr/bin/env bash
set -u

candidate_src=/tmp/audit-work/63-fibfib/candidate-src
evidence=/audit-output/evidence
overall=0
cd "$candidate_src" || exit 125

printf '%s\n' \
  'COMMAND: kast --definition concrete-kompiled --module FIBFIB-VERIFICATION --sort Pgm --expand-macros --output kore solution.mpy'
kast --definition concrete-kompiled \
  --module FIBFIB-VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output kore solution.mpy >"$evidence/kast_solution_expanded.kore"
solution_status=$?
printf 'EXIT: %s\n' "$solution_status"
if (( solution_status != 0 )); then overall=1; fi

printf '%s\n' \
  'COMMAND: kast --definition concrete-kompiled --module FIBFIB-VERIFICATION --sort Pgm --expand-macros --output kore /audit-output/evidence/fibfibProgram.term'
kast --definition concrete-kompiled \
  --module FIBFIB-VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output kore "$evidence/fibfibProgram.term" \
  >"$evidence/kast_fibfibProgram_expanded.kore"
macro_status=$?
printf 'EXIT: %s\n' "$macro_status"
if (( macro_status != 0 )); then overall=1; fi

printf '%s\n' \
  'COMMAND: cmp --silent kast_solution_expanded.kore kast_fibfibProgram_expanded.kore'
cmp --silent \
  "$evidence/kast_solution_expanded.kore" \
  "$evidence/kast_fibfibProgram_expanded.kore"
cmp_status=$?
printf 'EXIT: %s\n' "$cmp_status"
if (( cmp_status != 0 )); then
  overall=1
  diff -u \
    "$evidence/kast_solution_expanded.kore" \
    "$evidence/kast_fibfibProgram_expanded.kore"
fi
sha256sum \
  "$evidence/kast_solution_expanded.kore" \
  "$evidence/kast_fibfibProgram_expanded.kore"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/claim_witnesses.py'
python3 "$evidence/claim_witnesses.py"
witness_status=$?
printf 'EXIT: %s\n' "$witness_status"
if (( witness_status != 0 )); then overall=1; fi

printf 'STAGE4_PINNING_EXIT: %s\n' "$overall"
exit "$overall"
