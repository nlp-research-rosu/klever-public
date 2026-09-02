#!/usr/bin/env bash
set -u

cd /tmp/audit-work/135-can-arrange || exit 90

echo 'COMMAND: python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy'
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "EXIT translator: $translate_status"

echo 'COMMAND: cmp regenerated-solution.mpy submitted solution.mpy'
cmp regenerated-solution.mpy solution.mpy
cmp_status=$?
echo "EXIT MPY byte comparison: $cmp_status"

echo 'COMMAND: sha256sum submitted and regenerated MPY'
sha256sum solution.mpy regenerated-solution.mpy
sha_status=$?
echo "EXIT MPY hashes: $sha_status"

echo 'COMMAND: python3 reviewer-authored independent_differential.py'
python3 /audit-output/evidence/independent_differential.py
diff_status=$?
echo "EXIT independent differential: $diff_status"

if test "$translate_status" -eq 0 &&
   test "$cmp_status" -eq 0 &&
   test "$sha_status" -eq 0 &&
   test "$diff_status" -eq 0
then
  exit 0
fi
exit 1
