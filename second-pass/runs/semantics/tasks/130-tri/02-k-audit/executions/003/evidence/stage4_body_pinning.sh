#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/130-tri-audit
definition="$scratch/verification-audit-kompiled"
body="$scratch/solution.body.mpy"
submitted="$scratch/solution.submitted.mpy"
macro_json=/audit-output/evidence/stage4_macro_body.json
source_json=/audit-output/evidence/stage4_source_body.json
overall=0

printf 'COMMAND: sed -n 3,$p %q with final two module/function delimiters removed > %q\n' "$submitted" "$body"
sed -n '3,$p' "$submitted" | sed '$s/))$//' > "$body"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi

printf '\nEXTRACTED_REGENERATED_BODY\n'
nl -ba "$body"

printf '\nCOMMAND: kast macro with --expand-macros to JSON\n'
kast --definition "$definition" \
  --module TRI-VERIFICATION \
  --sort Stmts \
  --expand-macros \
  --expression TriFunctionBody \
  --output json > "$macro_json"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi

printf '\nCOMMAND: kast mechanically extracted submitted body with --expand-macros to JSON\n'
kast --definition "$definition" \
  --module TRI-VERIFICATION \
  --sort Stmts \
  --expand-macros \
  --output json "$body" > "$source_json"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi

printf '\nCOMMAND: cmp -s %q %q\n' "$macro_json" "$source_json"
cmp -s "$macro_json" "$source_json"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then
  overall=1
  diff -u "$source_json" "$macro_json" | sed -n '1,200p'
fi

printf '\nCOMMAND: sha256sum body JSON files\n'
sha256sum "$macro_json" "$source_json"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi

printf '\nBINDING_CHECK submitted_header=%q claim_params=%q claim_defining_scope=%q\n' \
  'FuncDef("tri", Params("n"), BODY)' \
  '("n", .ParamNames)' \
  '0'
printf 'STAGE4_BODY_PINNING_EXIT_STATUS: %d\n' "$overall"
exit "$overall"
