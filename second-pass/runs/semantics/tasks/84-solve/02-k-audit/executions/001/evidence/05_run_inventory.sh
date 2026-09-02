#!/usr/bin/env bash
set -u

generated=/tmp/audit-work/05_rule_inventory.regenerated.md
preserved=/audit-output/evidence/05_rule_inventory.md

printf '$ python3 /audit-output/evidence/05_inventory.py > %s\n' "$generated"
python3 /audit-output/evidence/05_inventory.py > "$generated"
generate_rc=$?
printf '[exit %d]\n' "$generate_rc"

printf '$ cmp %s %s\n' "$generated" "$preserved"
cmp "$generated" "$preserved"
cmp_rc=$?
printf '[exit %d]\n' "$cmp_rc"

printf '$ sha256sum %s %s\n' "$generated" "$preserved"
sha256sum "$generated" "$preserved"
hash_rc=$?
printf '[exit %d]\n' "$hash_rc"

if (( generate_rc == 0 && cmp_rc == 0 && hash_rc == 0 )); then
  exit 0
fi
exit 1
