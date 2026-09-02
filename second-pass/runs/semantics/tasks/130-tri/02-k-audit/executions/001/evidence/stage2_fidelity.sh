#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/reconstruction || exit 90

echo '$ python3 /reference/py2mpy.py solution.py | tee solution.regenerated.mpy >/dev/null'
python3 /reference/py2mpy.py solution.py \
  | tee solution.regenerated.mpy >/dev/null
translate_rc=${PIPESTATUS[0]}
echo "exit=$translate_rc"

echo '$ cmp solution.mpy solution.regenerated.mpy'
cmp solution.mpy solution.regenerated.mpy
cmp_rc=$?
echo "exit=$cmp_rc"

echo '$ sha256sum solution.mpy solution.regenerated.mpy'
sha256sum solution.mpy solution.regenerated.mpy
sha_rc=$?
echo "exit=$sha_rc"

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
diff_rc=$?
echo "exit=$diff_rc"

if [ "$translate_rc" -ne 0 ] || [ "$cmp_rc" -ne 0 ] \
   || [ "$sha_rc" -ne 0 ] || [ "$diff_rc" -ne 0 ]; then
  exit 1
fi
exit 0
