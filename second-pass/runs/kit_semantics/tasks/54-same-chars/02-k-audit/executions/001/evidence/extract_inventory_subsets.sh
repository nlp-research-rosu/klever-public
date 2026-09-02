#!/usr/bin/env bash
set -euo pipefail
set -o xtrace
inventory=/audit-output/evidence/rule_inventory.tsv
awk -F '\t' 'NR == 1 || $5 ~ /no-evaluators/' "$inventory" > /audit-output/evidence/opaque_inventory.tsv
awk -F '\t' 'NR == 1 || $5 ~ /priority/' "$inventory" > /audit-output/evidence/priority_inventory.tsv
awk -F '\t' 'NR == 1 || $2 == "verification.k" || $2 == "spec.k"' "$inventory" > /audit-output/evidence/proof_local_inventory.tsv
awk -F '\t' 'NR == 1 || $7 == "MANUAL_REVIEW"' "$inventory" > /audit-output/evidence/dependency_candidate_inventory.tsv
printf 'opaque_rows='
awk -F '\t' 'NR > 1 { count += 1 } END { print count + 0 }' /audit-output/evidence/opaque_inventory.tsv
printf 'priority_rows='
awk -F '\t' 'NR > 1 { count += 1 } END { print count + 0 }' /audit-output/evidence/priority_inventory.tsv
printf 'proof_local_rows='
awk -F '\t' 'NR > 1 { count += 1 } END { print count + 0 }' /audit-output/evidence/proof_local_inventory.tsv
printf 'dependency_candidate_rows='
awk -F '\t' 'NR > 1 { count += 1 } END { print count + 0 }' /audit-output/evidence/dependency_candidate_inventory.tsv
printf 'haskell_compiled_rule_records='
wc -l < /tmp/audit-work/54-same-chars/audit-verification-kompiled/allRules.txt
printf 'haskell_concrete_module_rule_records='
count=$(rg -c 'semantics/concrete\.k' /tmp/audit-work/54-same-chars/audit-verification-kompiled/allRules.txt || true)
printf '%s\n' "${count:-0}"
printf 'haskell_set_module_rule_records='
rg -c 'semantics/set\.k' /tmp/audit-work/54-same-chars/audit-verification-kompiled/allRules.txt
printf 'proof_local_semantic_declarations='
count=$(rg -c '^\s*(syntax|rule|context|configuration|alias)\b' /tmp/audit-work/54-same-chars/verification.k || true)
printf '%s\n' "${count:-0}"
printf 'spec_claims='
rg -c '^\s*claim\b' /tmp/audit-work/54-same-chars/spec.k
printf 'EXIT_STATUS=0\n'
