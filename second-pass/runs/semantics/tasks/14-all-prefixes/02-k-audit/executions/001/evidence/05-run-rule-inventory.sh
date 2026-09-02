#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/05-build-rule-inventory.py\n'
python3 /audit-output/evidence/05-build-rule-inventory.py
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ wc -l /audit-output/evidence/rule-inventory.tsv\n'
wc -l /audit-output/evidence/rule-inventory.tsv
printf '[exit %d]\n' "$?"

printf '\n$ sha256sum /audit-output/evidence/rule-inventory.tsv\n'
sha256sum /audit-output/evidence/rule-inventory.tsv
printf '[exit %d]\n' "$?"

exit "$status"
