#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/19-sort-numbers
python_source=$scratch/concrete-witness.py
mpy_program=$scratch/concrete-witness.mpy
translator=$scratch/trusted/py2mpy.py
definition=$scratch/runtime-kompiled

printf 'COMMAND: python3 %q %q > %q\n' "$translator" "$python_source" "$mpy_program"
python3 "$translator" "$python_source" > "$mpy_program"
translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translate_status"
if [[ $translate_status -ne 0 ]]; then
  exit "$translate_status"
fi

printf 'COMMAND: krun %q --definition %q --output pretty\n' "$mpy_program" "$definition"
krun "$mpy_program" --definition "$definition" --output pretty
run_status=$?
printf 'KRUN_EXIT_STATUS: %d\n' "$run_status"
exit "$run_status"
