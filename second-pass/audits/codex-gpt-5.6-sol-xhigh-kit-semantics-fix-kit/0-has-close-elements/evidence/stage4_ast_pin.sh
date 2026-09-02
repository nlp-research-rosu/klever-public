#!/usr/bin/env bash
set -u
set -x

scratch=/tmp/audit-work/reconstruction

kast "$scratch/regenerated-solution.mpy" \
  --definition "$scratch/verification-kompiled" \
  --module VERIFICATION --sort Module --expand-macros --output json \
  --output-file "$scratch/regenerated-solution.ast.json"
submitted_parse_status=$?

kast /audit-output/evidence/stage4-embedded-module.mpy \
  --definition "$scratch/verification-kompiled" \
  --module VERIFICATION --sort Module --expand-macros --output json \
  --output-file "$scratch/embedded-module.ast.json"
embedded_parse_status=$?

cmp "$scratch/regenerated-solution.ast.json" "$scratch/embedded-module.ast.json"
ast_cmp_status=$?

sha256sum "$scratch/regenerated-solution.ast.json" "$scratch/embedded-module.ast.json"

printf 'SUBMITTED_PARSE_STATUS=%d\n' "$submitted_parse_status"
printf 'EMBEDDED_PARSE_STATUS=%d\n' "$embedded_parse_status"
printf 'AST_CMP_STATUS=%d\n' "$ast_cmp_status"

if (( submitted_parse_status != 0 || embedded_parse_status != 0 || ast_cmp_status != 0 )); then
  exit 1
fi
exit 0
