#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/05_inventory.log
INVENTORY=/audit-output/evidence/05_rule_inventory.txt
ATTRIBUTES=/audit-output/evidence/05_attribute_inventory.txt
WORK=/tmp/audit-work/53-add
exec >"$LOG" 2>&1

cd "$WORK" || exit 1

printf '$ rg -n declarations reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k spec.k > %s\n' "$INVENTORY"
rg -n '^\s*(syntax|configuration|rule|context|claim)\b' \
  reference-semantics/semantics.k \
  reference-semantics/semantics/*.k \
  verification.k \
  spec.k > "$INVENTORY"
rc=$?
printf '[exit %d]\n' "$rc"

printf '\n$ rg -n semantic-attributes ... > %s\n' "$ATTRIBUTES"
rg -n '\[(?:[^]]*\b(?:function|functional|total|simplification|priority|owise|concrete|no-evaluators|symbol|strict|seqstrict|macro|macro-rec)\b[^]]*)\]' \
  reference-semantics/semantics.k \
  reference-semantics/semantics/*.k \
  verification.k \
  spec.k > "$ATTRIBUTES"
rc=$?
printf '[exit %d]\n' "$rc"

printf '\nDeclaration counts by source file:\n'
for file in \
  reference-semantics/semantics.k \
  reference-semantics/semantics/*.k \
  verification.k \
  spec.k; do
  syntax_count=$(rg -c '^\s*syntax\b' "$file" || true)
  rule_count=$(rg -c '^\s*rule\b' "$file" || true)
  context_count=$(rg -c '^\s*context\b' "$file" || true)
  configuration_count=$(rg -c '^\s*configuration\b' "$file" || true)
  claim_count=$(rg -c '^\s*claim\b' "$file" || true)
  printf '%-52s syntax=%-3s rules=%-3s contexts=%-2s config=%-2s claims=%-2s\n' \
    "$file" \
    "${syntax_count:-0}" \
    "${rule_count:-0}" \
    "${context_count:-0}" \
    "${configuration_count:-0}" \
    "${claim_count:-0}"
done

printf '\nSpecial attribute counts:\n'
for attribute in functional simplification total priority concrete no-evaluators symbol owise strict seqstrict macro macro-rec; do
  count=$(rg -o "\\b${attribute}\\b" "$ATTRIBUTES" | wc -l)
  printf '%-16s %s\n' "$attribute" "$count"
done

printf '\nInventory line counts:\n'
wc -l "$INVENTORY" "$ATTRIBUTES"
