#!/usr/bin/env bash
set -u
set -x

scratch=/tmp/audit-work/reconstruction

python3 "$scratch/py2mpy.py" "$scratch/solution.py" \
  > "$scratch/regenerated-solution.mpy"
translate_status=$?

cmp "$scratch/regenerated-solution.mpy" "$scratch/submitted-solution.mpy"
mpy_cmp_status=$?

sha256sum \
  "$scratch/solution.py" \
  "$scratch/regenerated-solution.mpy" \
  "$scratch/submitted-solution.mpy"

python3 -m py_compile "$scratch/canonical.py" "$scratch/solution.py"
python_compile_status=$?

printf 'TRANSLATE_STATUS=%d\n' "$translate_status"
printf 'MPY_CMP_STATUS=%d\n' "$mpy_cmp_status"
printf 'PYTHON_COMPILE_STATUS=%d\n' "$python_compile_status"

if (( translate_status != 0 || mpy_cmp_status != 0 || python_compile_status != 0 )); then
  exit 1
fi

exit 0
