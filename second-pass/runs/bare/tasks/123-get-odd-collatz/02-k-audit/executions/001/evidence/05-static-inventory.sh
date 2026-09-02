#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/candidate-src || exit 90

echo 'COMMAND: nl -ba semantic.k'
nl -ba semantic.k
semantic_source_rc=$?
echo "EXIT: $semantic_source_rc"

echo 'COMMAND: nl -ba verification.k'
nl -ba verification.k
verification_source_rc=$?
echo "EXIT: $verification_source_rc"

echo 'COMMAND: nl -ba spec.k'
nl -ba spec.k
spec_source_rc=$?
echo "EXIT: $spec_source_rc"

echo 'COMMAND: rg -n local declarations and attributes'
rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\[[^]]*(function|total|functional|simplification|priority|priorities|opaque)[^]]*\]' \
  semantic.k verification.k spec.k
inventory_rc=$?
echo "EXIT: $inventory_rc"

echo 'COMMAND: declaration counts'
for file in semantic.k verification.k spec.k; do
  syntax_count=$(rg -c '^[[:space:]]*syntax ' "$file" || true)
  rule_count=$(rg -c '^[[:space:]]*rule ' "$file" || true)
  claim_count=$(rg -c '^[[:space:]]*claim([[:space:]]|$)' "$file" || true)
  function_decl_count=$(rg -c '\[function(?:,|\])' "$file" || true)
  total_decl_count=$(rg -c '\[function,[[:space:]]*total\]' "$file" || true)
  simplification_count=$(rg -c '\[[^]]*simplification[^]]*\]' "$file" || true)
  priority_count=$(rg -c '\[[^]]*(priority|priorities)[^]]*\]' "$file" || true)
  opaque_count=$(rg -c '\[[^]]*opaque[^]]*\]' "$file" || true)
  echo "$file syntax_lines=${syntax_count:-0} rules=${rule_count:-0} claims=${claim_count:-0} function_decls=${function_decl_count:-0} total_decls=${total_decl_count:-0} simplification_attrs=${simplification_count:-0} priority_attrs=${priority_count:-0} opaque_attrs=${opaque_count:-0}"
done

if (( semantic_source_rc != 0 || verification_source_rc != 0 || spec_source_rc != 0 || inventory_rc != 0 )); then
  exit 1
fi
