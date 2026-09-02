#!/usr/bin/env bash
set -u

work=/tmp/audit-work/87-get-row
status=0

echo "AUDIT COMMAND: bash /audit-output/evidence/02_retranslation_check.sh"
echo "TRANSLATE: python3 /reference/py2mpy.py $work/solution.py > $work/solution.regenerated.mpy"
python3 /reference/py2mpy.py "$work/solution.py" > "$work/solution.regenerated.mpy"
translate_status=$?
echo "TRANSLATE_EXIT=$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

echo "COMPARE: cmp -- $work/solution.mpy $work/solution.regenerated.mpy"
if cmp -- "$work/solution.mpy" "$work/solution.regenerated.mpy"; then
  echo "BYTE_IDENTITY=PASS"
else
  status=$?
  echo "BYTE_IDENTITY=FAIL"
  diff -u "$work/solution.mpy" "$work/solution.regenerated.mpy" || true
fi

sha256sum "$work/solution.mpy" "$work/solution.regenerated.mpy"
echo "SCRIPT_EXIT=$status"
exit "$status"
