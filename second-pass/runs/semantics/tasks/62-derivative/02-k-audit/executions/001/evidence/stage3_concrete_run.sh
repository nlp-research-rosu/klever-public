#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference /audit-output/evidence/stage3_concrete.py "$scratch/stage3_concrete.py"
cd "$scratch" || exit 70

python3 py2mpy.py stage3_concrete.py > stage3_concrete.mpy
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

printf '%s\n' 'KRUN_COMMAND: timeout 180 krun stage3_concrete.mpy --definition runtime-kompiled'
timeout 180 krun stage3_concrete.mpy --definition runtime-kompiled
krun_status=$?
printf 'KRUN_EXIT_STATUS: %d\n' "$krun_status"
exit "$krun_status"
