#!/usr/bin/env bash
set -u
set -o pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/reconstruction
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translator_rc=$?
echo "TRUSTED_TRANSLATOR_EXIT=$translator_rc"

cmp solution.regenerated.mpy solution.mpy
cmp_rc=$?
echo "REGENERATED_MPY_BYTE_IDENTITY_EXIT=$cmp_rc"

sha256sum solution.py solution.mpy solution.regenerated.mpy \
  /reference/py2mpy.py /candidate/py2mpy.py

python3 /audit-output/evidence/differential_test.py
differential_rc=$?
echo "DIFFERENTIAL_TEST_EXIT=$differential_rc"

exit "$((translator_rc || cmp_rc || differential_rc))"
