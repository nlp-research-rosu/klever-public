#!/usr/bin/env bash
set -euo pipefail

sources=(
  /reference/reference-semantics/semantics.k
  /reference/reference-semantics/semantics/*.k
  /candidate/verification.k
  /candidate/spec.k
)

printf 'file\tsyntax-heads\trule-heads\tcontexts\tconfigurations\tclaims\n'
for source in "${sources[@]}"; do
  syntax_count="$(rg -c '^[[:space:]]*syntax ' "$source" || true)"
  rule_count="$(rg -c '^[[:space:]]*rule' "$source" || true)"
  context_count="$(rg -c '^[[:space:]]*context' "$source" || true)"
  config_count="$(rg -c '^[[:space:]]*configuration' "$source" || true)"
  claim_count="$(rg -c '^[[:space:]]*claim' "$source" || true)"
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$source" \
    "${syntax_count:-0}" \
    "${rule_count:-0}" \
    "${context_count:-0}" \
    "${config_count:-0}" \
    "${claim_count:-0}"
done

printf '\nExact declaration/rule head index\n'
rg -n '^[[:space:]]*(syntax|rule|context|configuration|claim)' "${sources[@]}"

printf '\nAttributes requiring special review\n'
rg -n \
  '(\bfunction\b|\btotal\b|\bfunctional\b|\bpriority\b|\bsimplification\b|\banywhere\b|\bmacro\b|\bowise\b|\bconcrete\b|\bsymbol\b|\bno-evaluators\b)' \
  "${sources[@]}" || true
