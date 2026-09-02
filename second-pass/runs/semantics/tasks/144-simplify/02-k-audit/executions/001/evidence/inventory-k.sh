#!/usr/bin/env bash
set -u

sources=(
  /reference/reference-semantics/semantics.k
  /reference/reference-semantics/semantics/*.k
  /candidate/verification.k
  /candidate/spec.k
)

printf '%s\n' '=== COUNTS BY FILE ==='
for source_path in "${sources[@]}"; do
  rules=$(rg -c '^\s*rule\b' "$source_path" 2>/dev/null || true)
  syntax=$(rg -c '^\s*syntax\b|^\s*\|' "$source_path" 2>/dev/null || true)
  contexts=$(rg -c '^\s*context\b' "$source_path" 2>/dev/null || true)
  claims=$(rg -c '^\s*claim\b' "$source_path" 2>/dev/null || true)
  configurations=$(rg -c '^\s*configuration\b' "$source_path" 2>/dev/null || true)
  printf '%s\trules=%s\tsyntax_productions=%s\tcontexts=%s\tclaims=%s\tconfigurations=%s\n' \
    "$source_path" "${rules:-0}" "${syntax:-0}" "${contexts:-0}" \
    "${claims:-0}" "${configurations:-0}"
done

printf '%s\n' '=== EVERY DECLARATION/RULE/CONTEXT/CLAIM START ==='
rg -n --no-heading \
  '^\s*(configuration|syntax|rule|context|claim)\b|^\s*\|' \
  "${sources[@]}" | LC_ALL=C sort

printf '%s\n' '=== EVERY RELEVANT ATTRIBUTE OCCURRENCE ==='
rg -n --no-heading \
  '\[(function|total|functional|symbol|no-evaluators|priority|owise|simplification|concrete|macro|strict|seqstrict|heat|cool)' \
  "${sources[@]}" | LC_ALL=C sort
