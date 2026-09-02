#!/usr/bin/env bash
set -euo pipefail

inputs=(
  /reference/reference-semantics/semantics.k
  /reference/reference-semantics/semantics/*.k
  /candidate/verification.k
  /candidate/spec.k
)

printf '%s\n' '# Exhaustive declaration/rule/claim inventory (source order)'
printf '%s\n' '# Generated with ripgrep 14-compatible syntax.'
rg -n --no-heading '^[[:space:]]*(configuration|syntax|context|rule|claim|alias)[[:space:]]' "${inputs[@]}"

printf '\n%s\n' '# Attribute-bearing and explicitly opaque/no-evaluator declarations'
rg -n --no-heading '\[(function|functional|total|macro|priority|simplification|concrete|owise)|no-evaluators|opaque|trusted' "${inputs[@]}"
