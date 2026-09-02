#!/usr/bin/env bash
set -u

scratch="/tmp/audit-work/37-sort-even"
log="/audit-output/evidence/02-fidelity.log"
regen="$scratch/solution.regenerated.mpy"

printf '%s\n' \
  'COMMAND: python3 /tmp/audit-work/37-sort-even/py2mpy.py /tmp/audit-work/37-sort-even/solution.py > /tmp/audit-work/37-sort-even/solution.regenerated.mpy' \
  'COMMAND: cmp -s /tmp/audit-work/37-sort-even/solution.regenerated.mpy /tmp/audit-work/37-sort-even/solution.mpy' \
  'COMMAND: sha256sum /tmp/audit-work/37-sort-even/solution.regenerated.mpy /tmp/audit-work/37-sort-even/solution.mpy' \
  'COMMAND: python3 /audit-output/evidence/differential_test.py' \
  > "$log"

python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$regen" 2>> "$log"
translate_status=$?
cmp -s "$regen" "$scratch/solution.mpy"
cmp_status=$?
sha256sum "$regen" "$scratch/solution.mpy" >> "$log" 2>&1
hash_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %s\n' "$translate_status" >> "$log"
printf 'BYTE_IDENTITY_EXIT_STATUS: %s\n' "$cmp_status" >> "$log"
printf 'HASH_COMMAND_EXIT_STATUS: %s\n' "$hash_status" >> "$log"

python3 /audit-output/evidence/differential_test.py >> "$log" 2>&1
diff_status=$?
printf 'DIFFERENTIAL_EXIT_STATUS: %s\n' "$diff_status" >> "$log"

if [ "$translate_status" -ne 0 ] || [ "$cmp_status" -ne 0 ] || \
   [ "$hash_status" -ne 0 ] || [ "$diff_status" -ne 0 ]; then
  exit 1
fi
exit 0
