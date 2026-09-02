#!/usr/bin/env bash
set -u

script=/audit-output/evidence/02_differential.py
inputs=/audit-output/evidence/02-differential-inputs.json
overall=0

printf '$ python3 %s --dump-inputs > %s\n' "$script" "$inputs"
python3 "$script" --dump-inputs > "$inputs"
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\n$ stat -c %%s %s\n' "$inputs"
stat -c '%s %n' "$inputs"
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\n$ sha256sum %s\n' "$inputs"
sha256sum "$inputs"
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\n$ python3 %s\n' "$script"
python3 "$script"
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

exit "$overall"
