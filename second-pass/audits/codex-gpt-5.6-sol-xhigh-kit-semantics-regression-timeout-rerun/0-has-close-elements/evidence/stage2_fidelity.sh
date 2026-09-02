#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/0-has-close-elements
evidence=/audit-output/evidence

printf '%s\n' '$ python3 /reference/py2mpy.py scratch/solution.py > scratch/regenerated-solution.mpy'
python3 /reference/py2mpy.py "$scratch/solution.py" \
  > "$scratch/regenerated-solution.mpy"
translate_status=$?
printf 'translator_exit=%s\n' "$translate_status"

printf '%s\n' '$ cmp -s scratch/regenerated-solution.mpy scratch/solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_status=$?
printf 'solution_mpy_cmp_exit=%s\n' "$cmp_status"
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"

printf '%s\n' '$ python3 -m py_compile scratch/canonical.py scratch/solution.py evidence/differential_audit.py'
PYTHONPYCACHEPREFIX="$scratch/pycache" \
  python3 -m py_compile \
    "$scratch/canonical.py" \
    "$scratch/solution.py" \
    "$evidence/differential_audit.py"
compile_status=$?
printf 'python_compile_exit=%s\n' "$compile_status"

printf '%s\n' '$ python3 evidence/differential_audit.py evidence/differential-inputs.json'
python3 "$evidence/differential_audit.py" \
  "$evidence/differential-inputs.json"
differential_status=$?
printf 'differential_exit=%s\n' "$differential_status"
wc -lc "$evidence/differential-inputs.json"
sha256sum "$evidence/differential-inputs.json"

if (( translate_status != 0 || cmp_status != 0 ||
      compile_status != 0 || differential_status != 0 )); then
  printf '%s\n' 'stage2_script_exit=1'
  exit 1
fi
printf '%s\n' 'stage2_script_exit=0'
