#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/forty-triples-audit
regenerated="$scratch/regenerated-solution.mpy"

python3 "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate-src/solution.py" > "$regenerated"
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS $translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

sha256sum "$scratch/candidate-src/solution.mpy" "$regenerated"
if cmp -s "$scratch/candidate-src/solution.mpy" "$regenerated"; then
  echo "SOLUTION_MPY_BYTE_IDENTITY OK"
  exit 0
fi

echo "SOLUTION_MPY_BYTE_IDENTITY FAIL"
diff -u "$scratch/candidate-src/solution.mpy" "$regenerated" || true
exit 1
