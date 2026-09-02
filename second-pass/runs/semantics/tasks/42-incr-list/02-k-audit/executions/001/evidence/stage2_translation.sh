#!/usr/bin/env bash
set -u

work=/tmp/audit-work/review
candidate="$work/candidate"
trusted="$work/trusted"
generated="$work/solution.trusted-regenerated.mpy"

echo "COMMAND: python3 $trusted/py2mpy.py $candidate/solution.py > $generated"
python3 "$trusted/py2mpy.py" "$candidate/solution.py" >"$generated"
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS=$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

sha256sum "$candidate/solution.mpy" "$generated"
echo "COMMAND: cmp -- $candidate/solution.mpy $generated"
if cmp -- "$candidate/solution.mpy" "$generated"; then
  echo "TRANSLATION_BYTE_IDENTITY=PASS"
  exit 0
fi

compare_status=$?
echo "TRANSLATION_BYTE_IDENTITY=FAIL"
diff -u "$candidate/solution.mpy" "$generated" || true
exit "$compare_status"
