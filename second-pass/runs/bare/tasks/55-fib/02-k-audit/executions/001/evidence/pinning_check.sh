#!/usr/bin/env bash
set -uo pipefail

definition=/tmp/audit-work/build/semantic-llvm-kompiled
submitted=/tmp/audit-work/src/solution.mpy
claim_program=/tmp/audit-work/src/claim-program.mpy
submitted_kast=/tmp/audit-work/build/solution.kast.json
claim_kast=/tmp/audit-work/build/claim-program.kast.json

printf '%s\n' \
  'NORMALIZATION: claim .Stmts list unit is rendered as the concrete empty Stmts field'

printf 'COMMAND: kast %q --definition %q --output json > %q\n' \
  "$submitted" "$definition" "$submitted_kast"
kast "$submitted" --definition "$definition" --output json > "$submitted_kast"
submitted_status=$?
printf 'SUBMITTED_KAST_EXIT_STATUS: %d\n' "$submitted_status"
if (( submitted_status != 0 )); then
  exit "$submitted_status"
fi

printf 'COMMAND: kast %q --definition %q --output json > %q\n' \
  "$claim_program" "$definition" "$claim_kast"
kast "$claim_program" --definition "$definition" --output json > "$claim_kast"
claim_status=$?
printf 'CLAIM_KAST_EXIT_STATUS: %d\n' "$claim_status"
if (( claim_status != 0 )); then
  exit "$claim_status"
fi

sha256sum "$submitted_kast" "$claim_kast"
printf 'COMMAND: cmp -s %q %q\n' "$submitted_kast" "$claim_kast"
cmp -s "$submitted_kast" "$claim_kast"
compare_status=$?
printf 'PARSED_TERM_COMPARE_EXIT_STATUS: %d\n' "$compare_status"
if (( compare_status != 0 )); then
  diff -u "$submitted_kast" "$claim_kast" || true
fi
exit "$compare_status"
