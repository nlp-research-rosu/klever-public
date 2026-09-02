#!/usr/bin/env bash
set -uo pipefail

for file in \
  /tmp/audit-work/candidate-fresh/list-domain.k \
  /tmp/audit-work/candidate-fresh/semantic.k \
  /tmp/audit-work/candidate-fresh/verification.k
do
  echo "FILE=$file"
  echo "COMMAND: rg numbered local declarations and special attributes $file"
  rg -n \
    '^[[:space:]]*(syntax|rule|configuration|claim|context|alias)([[:space:]]|$)|\[(function|total|functional|simplification|concrete|priority|owise|anywhere|macro|macro-rec|symbol|hook)' \
    "$file"
  scan_status=$?
  echo "SCAN_EXIT_STATUS=$scan_status"
  if [[ "$scan_status" -gt 1 ]]; then
    exit "$scan_status"
  fi
  rules=$(rg -c '^[[:space:]]*rule([[:space:]]|$)' "$file" || true)
  syntax=$(rg -c '^[[:space:]]*syntax([[:space:]]|$)' "$file" || true)
  claims=$(rg -c '^[[:space:]]*claim([[:space:]]|$)' "$file" || true)
  functions=$(rg -c '\[function\]' "$file" || true)
  special=$(rg -c '\[(total|functional|simplification|concrete|owise|anywhere|macro|macro-rec)(,|\])' "$file" || true)
  claims=${claims:-0}
  functions=${functions:-0}
  special=${special:-0}
  echo "RULE_COUNT=$rules"
  echo "SYNTAX_DECLARATION_COUNT=$syntax"
  echo "CLAIM_COUNT=$claims"
  echo "FUNCTION_DECLARATION_COUNT=$functions"
  echo "SPECIAL_RULE_ATTRIBUTE_COUNT=$special"
done

total_rules=$(rg -c '^[[:space:]]*rule([[:space:]]|$)' \
  /tmp/audit-work/candidate-fresh/{list-domain,semantic,verification}.k \
  | awk -F: '{sum += $2} END {print sum}')
total_syntax=$(rg -c '^[[:space:]]*syntax([[:space:]]|$)' \
  /tmp/audit-work/candidate-fresh/{list-domain,semantic,verification}.k \
  | awk -F: '{sum += $2} END {print sum}')
total_functions=$(rg -c '\[function\]' \
  /tmp/audit-work/candidate-fresh/{list-domain,semantic,verification}.k \
  | awk -F: '{sum += $2} END {print sum}')
echo "TOTAL_RULE_COUNT=$total_rules"
echo "TOTAL_SYNTAX_DECLARATION_COUNT=$total_syntax"
echo "TOTAL_FUNCTION_DECLARATION_COUNT=$total_functions"

if [[
  "$total_rules" -ne 32
  || "$total_syntax" -ne 24
  || "$total_functions" -ne 13
 ]]; then
  exit 2
fi
exit 0
