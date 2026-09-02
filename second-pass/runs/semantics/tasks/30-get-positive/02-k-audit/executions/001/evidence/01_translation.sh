#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive

printf '$ python3 /reference/py2mpy.py %s/solution.py > %s/regenerated-solution.mpy\n' \
  "$work" "$work"
python3 /reference/py2mpy.py "$work/solution.py" > "$work/regenerated-solution.mpy"
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ cmp %s/regenerated-solution.mpy %s/solution.mpy\n' "$work" "$work"
cmp "$work/regenerated-solution.mpy" "$work/solution.mpy"
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ sha256sum %s/regenerated-solution.mpy %s/solution.mpy\n' "$work" "$work"
sha256sum "$work/regenerated-solution.mpy" "$work/solution.mpy"
status=$?
printf '[exit %d]\n' "$status"

