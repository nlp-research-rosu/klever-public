#!/usr/bin/env bash
set -u

generator=/audit-output/evidence/inventory_k.py
scratch=/tmp/audit-work/review/candidate
inventory=/audit-output/evidence/k-rule-inventory.md

echo "COMMAND: python3 $generator $scratch > $inventory"
python3 "$generator" "$scratch" >"$inventory"
status=$?
echo "GENERATOR_EXIT_STATUS=$status"
if (( status != 0 )); then
  exit "$status"
fi

wc -l -c "$inventory"
sha256sum "$generator" "$inventory"
tail -1 "$inventory"
