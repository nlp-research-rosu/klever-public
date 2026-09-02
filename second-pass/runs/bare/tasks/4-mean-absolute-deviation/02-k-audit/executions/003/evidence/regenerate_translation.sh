#!/usr/bin/env bash
set -uo pipefail

scratch_root=/tmp/audit-work/4-mad-audit
generated_path="$scratch_root/regenerated-solution.mpy"
trusted_translator="$scratch_root/trusted/py2mpy.py"
solution_path="$scratch_root/candidate/solution.py"
submitted_path="$scratch_root/candidate/solution.mpy"

printf 'command: python3 %q %q > %q\n' \
  "$trusted_translator" "$solution_path" "$generated_path"
python3 "$trusted_translator" "$solution_path" >"$generated_path"
translate_status=$?
printf 'translator_exit_status: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

printf 'command: cmp -s %q %q\n' "$generated_path" "$submitted_path"
cmp -s "$generated_path" "$submitted_path"
cmp_status=$?
printf 'cmp_exit_status: %d\n' "$cmp_status"
sha256sum "$generated_path" "$submitted_path"
exit "$cmp_status"
