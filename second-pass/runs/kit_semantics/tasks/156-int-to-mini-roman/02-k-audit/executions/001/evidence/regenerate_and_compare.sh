#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/rebuild || exit 1
printf 'COMMAND: python3 py2mpy.py solution.py > regenerated.mpy\n'
python3 py2mpy.py solution.py > regenerated.mpy
translate_rc=$?
printf 'TRANSLATE_EXIT_STATUS: %s\n' "$translate_rc"
if [ "$translate_rc" -ne 0 ]; then
  exit "$translate_rc"
fi

printf 'COMMAND: cmp -s regenerated.mpy solution.mpy\n'
cmp -s regenerated.mpy solution.mpy
compare_rc=$?
printf 'COMPARE_EXIT_STATUS: %s\n' "$compare_rc"
printf 'SUBMITTED_SHA256: '
sha256sum solution.mpy | awk '{print $1}'
printf 'REGENERATED_SHA256: '
sha256sum regenerated.mpy | awk '{print $1}'
exit "$compare_rc"
