#!/usr/bin/env bash
set +e
cd /tmp/audit-work/68-pluck || exit 90

echo '$ python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy'
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
translate_rc=$?
echo "exit=$translate_rc"

echo '$ cmp -s regenerated-solution.mpy solution.mpy'
cmp -s regenerated-solution.mpy solution.mpy
cmp_rc=$?
echo "exit=$cmp_rc"

echo '$ sha256sum regenerated-solution.mpy solution.mpy'
sha256sum regenerated-solution.mpy solution.mpy
hash_rc=$?
echo "exit=$hash_rc"

echo '$ python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
diff_rc=$?
echo "exit=$diff_rc"

if (( translate_rc != 0 || cmp_rc != 0 || hash_rc != 0 || diff_rc != 0 )); then
  exit 1
fi
