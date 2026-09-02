#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/94-skjkasdkd/source
regenerated="$source_dir/solution.regenerated.mpy"

python3 /reference/py2mpy.py "$source_dir/solution.py" > "$regenerated"
translate_status=$?
echo "TRANSLATOR_EXIT: $translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

sha256sum "$source_dir/solution.mpy" "$regenerated"
if cmp -s "$source_dir/solution.mpy" "$regenerated"; then
  echo "BYTE_IDENTITY: PASS"
  exit 0
fi

echo "BYTE_IDENTITY: FAIL"
cmp -l "$source_dir/solution.mpy" "$regenerated" | head -n 40
exit 1
