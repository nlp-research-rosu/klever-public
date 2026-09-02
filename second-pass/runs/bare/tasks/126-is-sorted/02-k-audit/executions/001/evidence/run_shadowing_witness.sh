#!/usr/bin/env bash
set -u

mpy=/tmp/audit-work/126-is-sorted/candidate-src/shadowing_witness.mpy
python_source=/tmp/audit-work/126-is-sorted/candidate-src/shadowing_witness.py
translator=/tmp/audit-work/126-is-sorted/trusted/py2mpy.py

echo "COMMAND: cmp -l $mpy <(python3 $translator $python_source)"
cmp -l "$mpy" <(python3 "$translator" "$python_source")
compare_status=$?
echo "WITNESS_TRANSLATION_CMP_EXIT=$compare_status"

echo "COMMAND: python3 /audit-output/evidence/run_shadowing_witness.py"
python3 /audit-output/evidence/run_shadowing_witness.py
run_status=$?
echo "WITNESS_RUN_EXIT=$run_status"

if (( compare_status != 0 || run_status != 0 )); then
    exit 1
fi
