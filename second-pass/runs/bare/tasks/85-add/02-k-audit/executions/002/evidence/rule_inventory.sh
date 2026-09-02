#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/85-add-review || exit 2

for source in semantic.k verification.k spec.k; do
  echo "SOURCE=$source"
  echo "SYNTAX_AND_CONFIGURATION"
  rg -n '^[[:space:]]*(syntax|configuration|<[^>]+>)' "$source" || true
  echo "FUNCTION_TOTAL_FUNCTIONAL_OPAQUE_PRIORITY"
  rg -n '\[(function|total|functional|simplification|concrete|priority|macro|symbol)' "$source" || true
  echo "RULES_AND_CLAIMS"
  rg -n '^[[:space:]]*(rule|claim)([[:space:]]|$)' "$source" || true
done
