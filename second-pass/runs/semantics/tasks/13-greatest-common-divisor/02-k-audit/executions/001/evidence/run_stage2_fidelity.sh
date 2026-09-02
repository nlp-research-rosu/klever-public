#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /tmp/audit-work/source/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/solution.regenerated.mpy\n'
python3 /tmp/audit-work/source/py2mpy.py /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/source/solution.regenerated.mpy
translate_status=$?
printf 'TRANSLATOR EXIT STATUS: %d\n' "$translate_status"

printf 'COMMAND: cmp -s /tmp/audit-work/source/solution.regenerated.mpy /tmp/audit-work/source/solution.mpy\n'
cmp -s /tmp/audit-work/source/solution.regenerated.mpy /tmp/audit-work/source/solution.mpy
cmp_status=$?
printf 'BYTE IDENTITY EXIT STATUS: %d\n' "$cmp_status"

printf 'COMMAND: sha256sum /tmp/audit-work/source/solution.regenerated.mpy /tmp/audit-work/source/solution.mpy\n'
sha256sum /tmp/audit-work/source/solution.regenerated.mpy /tmp/audit-work/source/solution.mpy
sha_status=$?
printf 'SHA256 EXIT STATUS: %d\n' "$sha_status"

printf 'COMMAND: python3 /audit-output/evidence/differential_gcd.py\n'
python3 /audit-output/evidence/differential_gcd.py
differential_status=$?
printf 'DIFFERENTIAL EXIT STATUS: %d\n' "$differential_status"

if (( translate_status != 0 || cmp_status != 0 || sha_status != 0 || differential_status != 0 )); then
  exit 1
fi
exit 0
