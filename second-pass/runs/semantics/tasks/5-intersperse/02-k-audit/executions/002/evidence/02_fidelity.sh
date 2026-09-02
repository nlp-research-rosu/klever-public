#!/usr/bin/env bash
set -u
set -o pipefail

scratch=/tmp/audit-work/5-intersperse
overall=0

printf 'Regenerate solution.mpy with trusted translator\n'
python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$scratch/solution.regenerated.mpy"
translate_status=$?
printf 'translator_exit=%d\n' "$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  overall=1
fi

if cmp -s "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"; then
  printf 'translation_byte_identity=YES\n'
else
  printf 'translation_byte_identity=NO\n'
  diff -u "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"
  overall=1
fi
sha256sum "$scratch/solution.py" "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"

printf 'Independent Python differential test\n'
python3 /audit-output/evidence/02_differential.py
differential_status=$?
printf 'differential_exit=%d\n' "$differential_status"
if [[ "$differential_status" -ne 0 ]]; then
  overall=1
fi

printf 'FIDELITY_SCRIPT_STATUS=%d\n' "$overall"
exit "$overall"
