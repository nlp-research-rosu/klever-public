#!/usr/bin/env bash
set -u

python3 /tmp/audit-work/69-search-audit/trusted/py2mpy.py \
  /tmp/audit-work/69-search-audit/src/solution.py \
  > /tmp/audit-work/69-search-audit/build/solution.regenerated.mpy
translate_status=$?

cmp -s \
  /tmp/audit-work/69-search-audit/build/solution.regenerated.mpy \
  /tmp/audit-work/69-search-audit/src/solution.mpy
cmp_status=$?

sha256sum \
  /tmp/audit-work/69-search-audit/build/solution.regenerated.mpy \
  /tmp/audit-work/69-search-audit/src/solution.mpy
printf 'translator exit status: %d\n' "$translate_status"
printf 'byte-identity cmp status: %d\n' "$cmp_status"

if (( translate_status || cmp_status )); then
  exit 1
fi
