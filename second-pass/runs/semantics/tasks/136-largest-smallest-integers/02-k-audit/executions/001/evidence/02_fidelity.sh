#!/usr/bin/env bash
set -u

status=0
scratch=/tmp/audit-work/reconstruction

printf 'COMMAND: bash /audit-output/evidence/02_fidelity.sh\n'
printf 'STAGE: trusted translator regeneration\n'
printf 'RUN: python3 %s/py2mpy.py %s/solution.py\n' "$scratch" "$scratch"
python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$scratch/solution.regenerated.mpy"
translate_status=$?
printf 'EXIT translator: %d\n' "$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN: cmp %s/solution.regenerated.mpy %s/solution.mpy\n' "$scratch" "$scratch"
cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
cmp_status=$?
printf 'EXIT translated-byte-identity: %d\n' "$cmp_status"
sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
if [[ "$cmp_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: Python syntax and independent differential execution\n'
printf 'RUN: python3 -m py_compile %s/solution.py %s/canonical.py\n' "$scratch" "$scratch"
python3 -m py_compile "$scratch/solution.py" "$scratch/canonical.py"
compile_status=$?
printf 'EXIT py_compile: %d\n' "$compile_status"
if [[ "$compile_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN: python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
differential_status=$?
printf 'EXIT differential: %d\n' "$differential_status"
if [[ "$differential_status" -ne 0 ]]; then
  status=1
fi

printf 'FINAL EXIT: %d\n' "$status"
exit "$status"
