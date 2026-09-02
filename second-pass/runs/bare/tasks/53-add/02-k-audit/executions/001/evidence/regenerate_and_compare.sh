#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/53-add
cd "$scratch" || exit 70

python3 py2mpy.py solution.py > reviewer-regenerated-solution.mpy
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS: $translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

cmp -- solution.mpy reviewer-regenerated-solution.mpy
cmp_status=$?
echo "BYTE_IDENTITY_CMP_STATUS: $cmp_status"
sha256sum solution.mpy reviewer-regenerated-solution.mpy
exit "$cmp_status"
