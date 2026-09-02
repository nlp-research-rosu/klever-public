#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/review-31
candidate="$scratch/candidate"
definition="$scratch/verification-proof-kompiled"
claimed="$scratch/claimed-program.mpy"
submitted_kore="$scratch/submitted-program.kore"
claimed_kore="$scratch/claimed-program.kore"
mutant_kore="$scratch/mutant-program.kore"
overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return "$rc"
}

run python3 \
  /audit-output/evidence/extract_solution_program.py \
  "$candidate/verification.k" \
  "$claimed" || overall=1

run kast \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --output kore \
  --output-file "$submitted_kore" \
  "$candidate/solution.mpy" || overall=1

run kast \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --output kore \
  --output-file "$claimed_kore" \
  "$claimed" || overall=1

run cmp -s "$submitted_kore" "$claimed_kore"
same_rc=$?
if [[ "$same_rc" -ne 0 ]]; then
  overall=1
fi
sha256sum "$submitted_kore" "$claimed_kore"

run kast \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --output kore \
  --output-file "$mutant_kore" \
  "$scratch/solution-body-mutant.mpy" || overall=1

printf 'COMMAND (expected non-equality): cmp -s %q %q\n' \
  "$mutant_kore" "$claimed_kore"
cmp -s "$mutant_kore" "$claimed_kore"
mutant_cmp_rc=$?
printf 'EXIT: %d\n' "$mutant_cmp_rc"
if [[ "$mutant_cmp_rc" -eq 0 ]]; then
  overall=1
fi
sha256sum "$mutant_kore" "$claimed_kore"

printf 'STAGE4_OVERALL=%d\n' "$overall"
exit "$overall"
