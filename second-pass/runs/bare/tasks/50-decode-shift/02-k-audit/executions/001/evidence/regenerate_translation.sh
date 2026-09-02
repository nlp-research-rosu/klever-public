#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/50-decode-shift
trusted_translator="$scratch/trusted/py2mpy.py"
source_file="$scratch/candidate-src/solution.py"
submitted="$scratch/candidate-src/solution.mpy"
regenerated="$scratch/candidate-src/solution.regenerated.mpy"

python3 "$trusted_translator" "$source_file" > "$regenerated"
translator_status=$?
printf 'TRANSLATOR_EXIT_STATUS\t%s\n' "$translator_status"
if (( translator_status != 0 )); then
  exit "$translator_status"
fi

cmp -s "$submitted" "$regenerated"
cmp_status=$?
printf 'BYTE_IDENTITY_CMP_STATUS\t%s\n' "$cmp_status"
sha256sum "$submitted" "$regenerated"
if (( cmp_status != 0 )); then
  diff -u "$submitted" "$regenerated"
fi
exit "$cmp_status"
