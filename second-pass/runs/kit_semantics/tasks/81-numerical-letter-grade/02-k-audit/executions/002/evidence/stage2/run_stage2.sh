#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate-src || exit 90

printf '$ python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy\n'
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translate_rc=$?
printf 'EXIT translator=%s\n' "$translate_rc"

printf '$ cmp -s solution.regenerated.mpy solution.mpy\n'
cmp -s solution.regenerated.mpy solution.mpy
cmp_rc=$?
printf 'EXIT translator_byte_cmp=%s\n' "$cmp_rc"

printf '$ sha256sum solution.py solution.mpy solution.regenerated.mpy /reference/py2mpy.py\n'
sha256sum solution.py solution.mpy solution.regenerated.mpy /reference/py2mpy.py
sha_rc=$?
printf 'EXIT sha256sum=%s\n' "$sha_rc"

printf '$ python3 /audit-output/evidence/stage2/differential_audit.py\n'
python3 /audit-output/evidence/stage2/differential_audit.py
differential_rc=$?
printf 'EXIT differential=%s\n' "$differential_rc"

if (( translate_rc != 0 || cmp_rc != 0 || sha_rc != 0 || differential_rc != 0 )); then
  exit 1
fi
exit 0
