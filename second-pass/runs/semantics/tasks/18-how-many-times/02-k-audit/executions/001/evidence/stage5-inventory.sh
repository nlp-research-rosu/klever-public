#!/usr/bin/env bash
set -u
set -x

files=(
  /reference/reference-semantics/semantics.k
  /reference/reference-semantics/semantics/*.k
  /candidate/verification.k
  /candidate/spec.k
)

for file in "${files[@]}"; do
  echo "===== SOURCE: $file ====="
  echo "COUNTS"
  awk '
    /^[[:space:]]*syntax[[:space:]]/ { syntax += 1 }
    /^[[:space:]]*rule([[:space:]]|$)/ { rule += 1 }
    /^[[:space:]]*context([[:space:]]|$)/ { context += 1 }
    /^[[:space:]]*configuration([[:space:]]|$)/ { configuration += 1 }
    /^[[:space:]]*claim([[:space:]]|$)/ { claim += 1 }
    END {
      printf "syntax=%d rule=%d context=%d configuration=%d claim=%d\n",
             syntax, rule, context, configuration, claim
    }
  ' "$file"
  echo "DECLARATION_STARTS"
  rg -n \
    '^[[:space:]]*(syntax|rule|context|configuration|claim)([[:space:]]|$)|\[(function|total|functional|simplification|priority|macro|no-evaluators)' \
    "$file" || true
  echo "NUMBERED_SOURCE"
  nl -ba "$file"
done
