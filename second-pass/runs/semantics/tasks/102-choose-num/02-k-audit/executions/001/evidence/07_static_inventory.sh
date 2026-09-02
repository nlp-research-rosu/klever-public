#!/usr/bin/env bash
set +e

output=/audit-output/evidence/rule_inventory.md
printf 'Stage 5 exhaustive static inventory generation\n'
printf '\n$ python3 /audit-output/evidence/rule_inventory.py > %s\n' "$output"
python3 /audit-output/evidence/rule_inventory.py > "$output"
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ wc -l %s\n' "$output"
wc -l "$output"
printf '[exit %d]\n' "$?"

printf '\n$ sha256sum %s\n' "$output"
sha256sum "$output"
printf '[exit %d]\n' "$?"

printf '\n$ sed -n 1,18p %s\n' "$output"
sed -n '1,18p' "$output"
printf '[exit %d]\n' "$?"

printf '\n$ tail -n 20 %s\n' "$output"
tail -n 20 "$output"
printf '[exit %d]\n' "$?"

exit "$status"
