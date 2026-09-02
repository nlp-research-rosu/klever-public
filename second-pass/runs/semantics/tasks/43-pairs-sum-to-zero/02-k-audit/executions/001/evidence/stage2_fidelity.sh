#!/usr/bin/env bash
set +e

cd /tmp/audit-work/pairs-audit || exit 99

echo '$ python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy'
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "exit=$translate_status"

echo '$ cmp regenerated-solution.mpy solution.mpy'
cmp regenerated-solution.mpy solution.mpy
cmp_status=$?
echo "exit=$cmp_status"

echo '$ sha256sum regenerated-solution.mpy solution.mpy'
sha256sum regenerated-solution.mpy solution.mpy
echo "exit=$?"

echo '$ python3 /audit-output/evidence/differential.py'
python3 /audit-output/evidence/differential.py
diff_status=$?
echo "exit=$diff_status"

if (( translate_status != 0 || cmp_status != 0 || diff_status != 0 )); then
  exit 1
fi
exit 0
