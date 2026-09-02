#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/87-get-row
definition="$scratch/verification-audit-kompiled"
status=0

printf '%s\n' '$ kast regenerated solution.mpy to KORE with the fresh proof definition'
kast "$scratch/regenerated_solution.mpy" \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Program \
  --output kore > "$scratch/translated-program.kore"
rc=$?
printf 'translated_kast_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ kast and expand the verification solutionProgram macro to KORE'
kast --expression solutionProgram \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Program \
  --expand-macros \
  --output kore > "$scratch/proof-program.kore"
rc=$?
printf 'proof_macro_kast_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ cmp translated-program.kore proof-program.kore'
cmp "$scratch/translated-program.kore" "$scratch/proof-program.kore"
rc=$?
printf 'program_kore_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ sha256sum both KORE program terms'
sha256sum "$scratch/translated-program.kore" "$scratch/proof-program.kore"
rc=$?
printf 'program_kore_sha_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ python3 claim_witnesses.py'
python3 /audit-output/evidence/claim_witnesses.py
rc=$?
printf 'claim_witnesses_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf 'overall_exit=%d\n' "$status"
exit "$status"
