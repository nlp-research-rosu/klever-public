#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/147-get-max-triples-clean

printf '$ python3 /audit-output/evidence/inventory_k.py\n'
python3 /audit-output/evidence/inventory_k.py > /audit-output/evidence/K-INVENTORY.md
printf '[exit 0]\n'

printf '$ concatenate every numbered K source file\n'
{
  for file in $(find reference-semantics -type f -name '*.k' | sort); do
    printf '===== %s\n' "$file"
    nl -ba "$file"
  done
  printf '===== verification.k\n'
  nl -ba verification.k
  printf '===== spec.k\n'
  nl -ba spec.k
} > /audit-output/evidence/K-SOURCES-NUMBERED.txt
printf '[exit 0]\n'

printf '$ inventory summary\n'
tail -n 8 /audit-output/evidence/K-INVENTORY.md
printf '[exit 0]\n'

printf '$ enumerate attributes requiring special review\n'
rg -n \
  '\[[^]]*(function|functional|total|symbol|no-evaluators|priority|owise|concrete|macro|macro-rec|strict|seqstrict|simplification)[^]]*\]' \
  reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k spec.k \
  > /audit-output/evidence/K-SPECIAL-ATTRIBUTES.txt
cat /audit-output/evidence/K-SPECIAL-ATTRIBUTES.txt
printf '[exit 0]\n'
