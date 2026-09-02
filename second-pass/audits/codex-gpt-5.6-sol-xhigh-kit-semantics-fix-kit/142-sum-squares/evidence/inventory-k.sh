#!/usr/bin/env bash
set -euo pipefail

if (( $# == 0 )); then
  echo "usage: $0 K_FILE ..." >&2
  exit 64
fi

for file in "$@"; do
  printf '===== FILE %s\n' "$file"
  printf 'COUNTS '
  awk '
    /^[[:space:]]*syntax[[:space:]]/ { syntax++ }
    /^[[:space:]]*rule[[:space:]]/ { rule++ }
    /^[[:space:]]*claim[[:space:]]/ { claim++ }
    /^[[:space:]]*context[[:space:]]/ { context++ }
    /^[[:space:]]*configuration([[:space:]]|$)/ { configuration++ }
    END {
      printf "syntax=%d rules=%d claims=%d contexts=%d configurations=%d\n",
             syntax, rule, claim, context, configuration
    }
  ' "$file"
  printf '%s\n' '-- DECLARATION STARTS --'
  rg -n '^\s*(module|imports|requires|configuration|syntax|context|rule|claim|endmodule)(\s|$)' "$file" || true
  printf '%s\n' '-- SEMANTIC ATTRIBUTES AND OPAQUE MARKERS --'
  rg -n '\[(function|functional|total|concrete|priority|simplification|owise|macro)(\(|,|\]|\s)|\bopaque\b' "$file" || true
done
