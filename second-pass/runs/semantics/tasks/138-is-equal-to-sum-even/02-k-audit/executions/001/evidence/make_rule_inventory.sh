#!/usr/bin/env bash
set -euo pipefail

root=/tmp/audit-work/review-138
mapfile -t files < <(
  {
    printf '%s\n' "$root/reference-semantics/semantics.k"
    find "$root/reference-semantics/semantics" -maxdepth 1 -type f -name '*.k' -print
    printf '%s\n' "$root/verification.k" "$root/spec.k"
  } | sort
)

echo "INVENTORY_ROOT: $root"
echo "SEMANTICS_INTEGRITY_PRECONDITION: byte/type tree matched trusted /reference/reference-semantics"
echo
echo "PER_FILE_COUNTS"
printf '%-24s %7s %7s %7s %7s %7s %7s %7s\n' \
  FILE LINES SYNTAX RULES CONTEXT CONFIG CLAIMS PRIORITY
for file in "${files[@]}"; do
  rel="${file#"$root/"}"
  lines="$(wc -l < "$file")"
  syntax="$(grep -Ec '^[[:space:]]*syntax\b' "$file" || true)"
  rules="$(grep -Ec '^[[:space:]]*rule\b' "$file" || true)"
  contexts="$(grep -Ec '^[[:space:]]*context( alias)?\b' "$file" || true)"
  configs="$(grep -Ec '^[[:space:]]*configuration\b' "$file" || true)"
  claims="$(grep -Ec '^[[:space:]]*claim\b' "$file" || true)"
  priorities="$(grep -Ec '\bpriority[[:space:]]*[(]' "$file" || true)"
  printf '%-24s %7s %7s %7s %7s %7s %7s %7s\n' \
    "$rel" "$lines" "$syntax" "$rules" "$contexts" "$configs" "$claims" "$priorities"
done

echo
echo "EVERY_DECLARATION_RULE_CONTEXT_CONFIGURATION_AND_CLAIM_START"
rg -Hn '^[[:space:]]*(syntax|rule|context( alias)?|configuration|claim)\b' "${files[@]}"

echo
echo "EVERY_GUARD_AND_SEMANTIC_ATTRIBUTE_LINE"
rg -Hn '^[[:space:]]*(requires|ensures)\b|\[(function|total|functional|simplification|concrete|owise|priority|macro|macro-rec|strict|seqstrict|symbol|no-evaluators)' "${files[@]}"

echo
echo "OPAQUE_OR_TRUST_MARKERS"
rg -Hn -i 'opaque|trusted|oracle|no-evaluators' "${files[@]}" || true

echo
echo "SOURCE_HASHES"
sha256sum "${files[@]}"
