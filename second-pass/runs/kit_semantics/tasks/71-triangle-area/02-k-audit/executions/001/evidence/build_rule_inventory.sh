#!/usr/bin/env bash
set -euo pipefail

root=/tmp/audit-work/proof
sources=(
  "$root/reference-semantics/semantics.k"
  "$root/reference-semantics/semantics/"*.k
  "$root/verification.k"
  "$root/spec.k"
)
pattern='^[[:space:]]*(requires|module|imports|configuration|syntax|context|rule|claim|endmodule)\b|\[(function|total|functional|simplification|concrete|symbol|no-evaluators|priority|owise|macro)'

for source in "${sources[@]}"; do
  relative=${source#"$root/"}
  printf 'FILE %s\n' "$relative"
  sha256sum "$source"
  printf 'COUNTS '
  printf 'syntax=%s ' "$(rg -c '^[[:space:]]*syntax\b' "$source" || true)"
  printf 'rules=%s ' "$(rg -c '^[[:space:]]*rule\b' "$source" || true)"
  printf 'contexts=%s ' "$(rg -c '^[[:space:]]*context\b' "$source" || true)"
  printf 'claims=%s ' "$(rg -c '^[[:space:]]*claim\b' "$source" || true)"
  printf 'function_attrs=%s ' "$(rg -c '\[([^]]*,[[:space:]]*)?function([,]])' "$source" || true)"
  printf 'total_attrs=%s ' "$(rg -c '\[[^]]*total' "$source" || true)"
  printf 'functional_attrs=%s ' "$(rg -c '\[[^]]*functional' "$source" || true)"
  printf 'opaque_no_evaluators=%s ' "$(rg -c 'no-evaluators' "$source" || true)"
  printf 'priority_attrs=%s ' "$(rg -c '\[priority\(' "$source" || true)"
  printf 'simplification_attrs=%s ' "$(rg -c '\[simplification' "$source" || true)"
  printf 'concrete_attrs=%s\n' "$(rg -c 'concrete' "$source" || true)"
  rg -n "$pattern" "$source" || true
done
