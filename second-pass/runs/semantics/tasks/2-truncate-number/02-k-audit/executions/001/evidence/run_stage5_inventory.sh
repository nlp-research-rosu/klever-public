#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run bash -c 'python3 /audit-output/evidence/inventory_k.py > /audit-output/evidence/rule_inventory.md'
run wc -l -c /audit-output/evidence/rule_inventory.md
run rg -n \
  -e '^Total inventoried statements:' \
  -e '^\| `.*\.k` \|' \
  /audit-output/evidence/rule_inventory.md
run rg -c '^### K-[0-9]{4}' /audit-output/evidence/rule_inventory.md
