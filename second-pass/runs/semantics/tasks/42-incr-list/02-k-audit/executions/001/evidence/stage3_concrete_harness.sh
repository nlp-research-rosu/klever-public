#!/usr/bin/env bash
set -u

translator=/tmp/audit-work/review/trusted/py2mpy.py
source_file=/audit-output/evidence/stage3_concrete_harness.py
mpy_file=/tmp/audit-work/review/candidate/stage3_concrete_harness.mpy
definition=/tmp/audit-work/review/candidate/runtime-audit-kompiled

echo "COMMAND: python3 $translator $source_file > $mpy_file"
python3 "$translator" "$source_file" >"$mpy_file"
translation_status=$?
echo "TRANSLATOR_EXIT_STATUS=$translation_status"
if (( translation_status != 0 )); then
  exit "$translation_status"
fi
sha256sum "$source_file" "$mpy_file"

echo "COMMAND: krun $mpy_file --definition $definition --output pretty"
krun "$mpy_file" --definition "$definition" --output pretty
krun_status=$?
echo "KRUN_EXIT_STATUS=$krun_status"
exit "$krun_status"
