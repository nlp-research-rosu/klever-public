#!/usr/bin/env bash
set -uo pipefail

source_path="/tmp/audit-work/candidate/solution.py"
translator_path="/tmp/audit-work/trusted/py2mpy.py"
regenerated_path="/tmp/audit-work/candidate/solution.regenerated.mpy"
submitted_path="/tmp/audit-work/candidate/solution.mpy"

printf 'TRANSLATOR_COMMAND: python3 %q %q > %q\n' \
  "$translator_path" "$source_path" "$regenerated_path"
python3 "$translator_path" "$source_path" > "$regenerated_path"
translator_status="$?"
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  exit "$translator_status"
fi

printf 'COMPARE_COMMAND: cmp -s %q %q\n' "$regenerated_path" "$submitted_path"
cmp -s "$regenerated_path" "$submitted_path"
compare_status="$?"
printf 'COMPARE_EXIT_STATUS: %d\n' "$compare_status"
sha256sum "$regenerated_path" "$submitted_path"
exit "$compare_status"
