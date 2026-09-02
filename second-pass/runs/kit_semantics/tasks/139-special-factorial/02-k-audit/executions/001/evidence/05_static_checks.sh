#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/05_rule_inventory.py'
python3 /audit-output/evidence/05_rule_inventory.py
inventory_status=$?
printf 'EXIT: %s\n' "$inventory_status"

printf '%s\n' '--- source declaration counts ---'
printf 'syntax_heads='
rg '^\s*syntax\b' reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k | wc -l
printf 'rules='
rg '^\s*rule\b' reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k | wc -l
printf 'contexts='
rg '^\s*context\b' reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k | wc -l
printf 'configurations='
rg '^\s*configuration\b' reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k | wc -l
printf 'claims='
rg '^\s*claim\b' spec.k | wc -l

printf '%s\n' '--- proof-local potentially dangerous attributes/rules ---'
rg -n 'priority|simplification|concrete|no-evaluators|opaque|Call|While|Return|#while|#pop' verification.k
danger_scan_status=$?
printf 'proof_local_danger_scan_exit=%s (1 means no matches)\n' "$danger_scan_status"

printf '%s\n' '--- opaque or no-evaluator symbols in the fixed supplied semantics ---'
rg -n 'no-evaluators|OPAQUE|opaque' reference-semantics/semantics.k reference-semantics/semantics/*.k
opaque_scan_status=$?
printf 'fixed_opaque_scan_exit=%s\n' "$opaque_scan_status"

printf '%s\n' '--- all priority rules in the fixed supplied semantics ---'
rg -n -B 4 -A 1 'priority\(' reference-semantics/semantics.k reference-semantics/semantics/*.k
priority_scan_status=$?
printf 'fixed_priority_scan_exit=%s\n' "$priority_scan_status"

exit "$inventory_status"
