#!/usr/bin/env bash
set +e
set -x

python3 /audit-output/evidence/static_inventory.py
inventory_exit=$?
printf 'static inventory exit: %s\n' "$inventory_exit"

for source in \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/spec.k
do
  nl -ba "$source"
done

rg -n '\[[^]]*(priority|simplification|total|functional|opaque|owise)[^]]*\]' \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/spec.k
special_attribute_search_exit=$?
printf 'special attribute search exit (1 means none found): %s\n' \
  "$special_attribute_search_exit"

exit "$inventory_exit"
