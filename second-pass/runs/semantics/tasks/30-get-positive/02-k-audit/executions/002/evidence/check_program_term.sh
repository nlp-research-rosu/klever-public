#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/30-get-positive
definition="$scratch/verification-kompiled"
submitted="$scratch/solution.mpy"
submitted_kore=/audit-output/evidence/submitted-program-expanded.kore
claim_kore=/audit-output/evidence/claim-program-expanded.kore

kast "$submitted" \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > "$submitted_kore"
submitted_status=$?

kast \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Module \
  --expression \
    'Module(FuncDef("get_positive", Params("l"), getPositiveBody))' \
  --expand-macros \
  --output kore > "$claim_kore"
claim_status=$?

cmp "$submitted_kore" "$claim_kore"
compare_status=$?

printf '%s\n' \
  "COMMAND: kast $submitted --definition $definition --module VERIFICATION --sort Module --expand-macros --output kore > $submitted_kore" \
  "SUBMITTED_PARSE_EXIT_STATUS: $submitted_status" \
  "COMMAND: kast --definition $definition --module VERIFICATION --sort Module --expression 'Module(FuncDef(\"get_positive\", Params(\"l\"), getPositiveBody))' --expand-macros --output kore > $claim_kore" \
  "CLAIM_TERM_PARSE_EXIT_STATUS: $claim_status" \
  "COMMAND: cmp $submitted_kore $claim_kore" \
  "CONSTRUCTOR_IDENTITY_EXIT_STATUS: $compare_status"
sha256sum "$submitted_kore" "$claim_kore"

test "$submitted_status" -eq 0 \
  -a "$claim_status" -eq 0 \
  -a "$compare_status" -eq 0
