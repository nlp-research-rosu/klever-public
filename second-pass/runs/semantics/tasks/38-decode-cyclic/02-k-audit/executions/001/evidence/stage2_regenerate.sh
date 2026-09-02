#!/usr/bin/env bash
set -u

work=/tmp/audit-work/38-decode-cyclic/candidate
trusted_translator=/reference/py2mpy.py
regenerated="$work/solution.regenerated.mpy"

printf 'SUBCOMMAND: python3 %q %q > %q\n' \
  "$trusted_translator" "$work/solution.py" "$regenerated"
python3 "$trusted_translator" "$work/solution.py" >"$regenerated"
translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

printf 'SUBCOMMAND: cmp -s %q %q\n' "$regenerated" "$work/solution.mpy"
cmp -s "$regenerated" "$work/solution.mpy"
cmp_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$cmp_status"

sha256sum "$work/solution.py" "$work/solution.mpy" "$regenerated"
if (( cmp_status != 0 )); then
  diff -u "$work/solution.mpy" "$regenerated" || true
fi
exit "$cmp_status"
