#!/usr/bin/env bash
set -uo pipefail

source_py=/tmp/audit-work/tests/concrete_audit.py
program_mpy=/tmp/audit-work/build/concrete_audit.mpy
definition=/tmp/audit-work/build/runtime-kompiled

printf 'COMMAND: python3 /reference/py2mpy.py %q > %q\n' "$source_py" "$program_mpy"
python3 /reference/py2mpy.py "$source_py" > "$program_mpy"
translation_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translation_status"
if (( translation_status != 0 )); then
  exit "$translation_status"
fi

printf 'COMMAND: krun %q --definition %q\n' "$program_mpy" "$definition"
krun "$program_mpy" --definition "$definition"
krun_status=$?
printf 'KRUN_EXIT_STATUS: %d\n' "$krun_status"
exit "$krun_status"
