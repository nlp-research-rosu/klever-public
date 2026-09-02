#!/usr/bin/env bash
set -u

sources=(
  /reference/reference-semantics/semantics.k
  /reference/reference-semantics/semantics/*.k
  /candidate/verification.k
  /candidate/spec.k
)

printf 'COMMAND: rg -n declarations/rules/claims/contexts/configuration over all supplied K sources and candidate proof sources\n'
rg -n '^[[:space:]]*(syntax|rule|claim|context|configuration|module|endmodule|imports|requires|alias)\b' "${sources[@]}"
printf '[exit %d]\n' "$?"

printf 'COMMAND: rg -n all semantic attributes over the same source set\n'
rg -n '\[(function|total|functional|simplification|simplifier|priority|owise|macro|macro-rec|symbol|no-evaluators|concrete|strict|seqstrict)' "${sources[@]}"
printf '[exit %d]\n' "$?"

printf 'COMMAND: count inventory categories\n'
for category in syntax rule claim context configuration; do
  count=$(rg -n "^[[:space:]]*${category}\b" "${sources[@]}" | wc -l)
  printf '%s=%s\n' "$category" "$count"
done
printf 'function_declaration_lines=%s\n' "$(rg -n '^[[:space:]]*syntax.*\[.*function' "${sources[@]}" | wc -l)"
printf 'total_declaration_lines=%s\n' "$(rg -n '^[[:space:]]*syntax.*\[.*total' "${sources[@]}" | wc -l)"
printf 'functional_declaration_lines=%s\n' "$(rg -n '\[functional' "${sources[@]}" | wc -l)"
printf 'opaque_no_evaluators_lines=%s\n' "$(rg -n 'no-evaluators' "${sources[@]}" | wc -l)"
printf 'priority_attribute_lines=%s\n' "$(rg -n '\[priority' "${sources[@]}" | wc -l)"
printf 'simplification_attribute_lines=%s\n' "$(rg -n '\[(simplification|simplifier)' "${sources[@]}" | wc -l)"
printf '[exit 0]\n'
