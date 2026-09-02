#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"

echo '$ python3 /reference/py2mpy.py /tmp/audit-work/solution.py > /tmp/audit-work/solution.regenerated.mpy'
python3 /reference/py2mpy.py /tmp/audit-work/solution.py \
  > /tmp/audit-work/solution.regenerated.mpy
translate_rc=$?
printf '[exit %d]\n\n' "$translate_rc"

echo '$ cmp -s /tmp/audit-work/solution.regenerated.mpy /tmp/audit-work/solution.mpy'
cmp -s /tmp/audit-work/solution.regenerated.mpy /tmp/audit-work/solution.mpy
cmp_rc=$?
printf '[exit %d]\n\n' "$cmp_rc"

echo '$ sha256sum /tmp/audit-work/solution.regenerated.mpy /tmp/audit-work/solution.mpy'
sha256sum /tmp/audit-work/solution.regenerated.mpy /tmp/audit-work/solution.mpy
hash_rc=$?
printf '[exit %d]\n\n' "$hash_rc"

echo '$ python3 /audit-output/evidence/stage2_differential.py'
python3 /audit-output/evidence/stage2_differential.py
differential_rc=$?
printf '[exit %d]\n\n' "$differential_rc"

if (( translate_rc != 0 || cmp_rc != 0 || hash_rc != 0 || differential_rc != 0 )); then
  exit 1
fi
