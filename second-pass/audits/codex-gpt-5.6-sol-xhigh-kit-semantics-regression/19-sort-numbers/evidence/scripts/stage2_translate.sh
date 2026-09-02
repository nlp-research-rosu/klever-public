#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/19-sort-numbers
source_dir=$scratch/source
trusted_dir=$scratch/trusted
regenerated=$scratch/regenerated-solution.mpy

printf 'COMMAND: python3 %q %q > %q\n' \
  "$trusted_dir/py2mpy.py" "$source_dir/solution.py" "$regenerated"
python3 "$trusted_dir/py2mpy.py" "$source_dir/solution.py" > "$regenerated"
translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translate_status"
if [[ $translate_status -ne 0 ]]; then
  exit "$translate_status"
fi

printf 'COMMAND: cmp -s %q %q\n' "$regenerated" "$source_dir/solution.mpy"
cmp -s "$regenerated" "$source_dir/solution.mpy"
cmp_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$cmp_status"
sha256sum "$regenerated" "$source_dir/solution.mpy"
exit "$cmp_status"
