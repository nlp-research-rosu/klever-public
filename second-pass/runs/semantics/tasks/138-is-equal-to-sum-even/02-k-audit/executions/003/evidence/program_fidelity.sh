#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

printf '%s\n' \
  'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy' \
  'CWD: /tmp/audit-work/reconstruction'
(
  cd "$work" || exit 99
  python3 py2mpy.py solution.py > regenerated-solution.mpy
)
translate_status=$?
printf 'EXIT_STATUS: %s\n' "$translate_status"

printf '%s\n' \
  'COMMAND: cmp -s regenerated-solution.mpy submitted-solution.mpy' \
  'CWD: /tmp/audit-work/reconstruction'
(
  cd "$work" || exit 99
  cmp -s regenerated-solution.mpy submitted-solution.mpy
)
cmp_status=$?
printf 'EXIT_STATUS: %s\n' "$cmp_status"

printf '%s\n' \
  'COMMAND: sha256sum regenerated-solution.mpy submitted-solution.mpy solution.py'
sha256sum \
  "$work/regenerated-solution.mpy" \
  "$work/submitted-solution.mpy" \
  "$work/solution.py"
hash_status=$?
printf 'EXIT_STATUS: %s\n' "$hash_status"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 "$evidence/differential_test.py"
diff_status=$?
printf 'EXIT_STATUS: %s\n' "$diff_status"

if (( translate_status != 0 || cmp_status != 0 || hash_status != 0 || diff_status != 0 )); then
  exit 1
fi
exit 0
