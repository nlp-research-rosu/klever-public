#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
regenerated=$(mktemp /tmp/audit-work/solution-regenerated.XXXXXX.mpy)
python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$regenerated"
translate_status=$?

echo "translator_exit=$translate_status"
sha256sum "$regenerated" "$scratch/solution.mpy" /candidate/solution.mpy
cmp -s "$regenerated" "$scratch/solution.mpy"
cmp_status=$?
echo "byte_identity_cmp_exit=$cmp_status"

cp "$regenerated" "$scratch/solution.regenerated.mpy"
rm -f "$regenerated"

if (( translate_status != 0 )); then
  exit "$translate_status"
fi
exit "$cmp_status"
