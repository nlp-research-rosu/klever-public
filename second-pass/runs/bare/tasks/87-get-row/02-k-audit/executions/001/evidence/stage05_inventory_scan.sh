#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/87-get-row/source
status=0

printf '%s\n' '$ rg all local module/import/syntax/configuration/rule/claim declarations'
rg -n '^\s*(module|imports|syntax|configuration|rule|claim|requires|ensures)' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
rc=$?
printf 'declaration_scan_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ rg all soundness-sensitive local attributes/tokens'
rg -n '\[(function|total|functional|simplification|concrete|macro|priority|owise|anywhere|trusted|opaque)|priority|simplification|opaque|\[owise\]' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
rc=$?
printf 'attribute_scan_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ count semantic rules, verification rules, and spec claims'
printf 'semantic_rules='
rg -c '^\s*rule\b' "$scratch/semantic.k"
rc=$?
printf 'semantic_rule_count_exit=%d\n' "$rc"
(( rc == 0 )) || status=1
printf 'verification_rules='
rg -c '^\s*rule\b' "$scratch/verification.k"
rc=$?
printf 'verification_rule_count_exit=%d\n' "$rc"
(( rc == 0 )) || status=1
printf 'spec_claims='
rg -c '^\s*claim\b' "$scratch/spec.k"
rc=$?
printf 'spec_claim_count_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf 'overall_exit=%d\n' "$status"
exit "$status"
