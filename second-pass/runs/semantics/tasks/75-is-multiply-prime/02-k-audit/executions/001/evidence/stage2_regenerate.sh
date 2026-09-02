#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/75-prime
generated="$scratch/regenerated-solution.mpy"

python3 "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate/solution.py" >"$generated"
translate_status=$?
echo "translator_exit_status=$translate_status"

sha256sum "$scratch/candidate/solution.mpy" "$generated"
wc -c "$scratch/candidate/solution.mpy" "$generated"

cmp "$scratch/candidate/solution.mpy" "$generated"
cmp_status=$?
echo "cmp_status=$cmp_status"

if (( translate_status != 0 || cmp_status != 0 )); then
  exit 1
fi
