#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit

echo 'COMMAND: python3 py2mpy.py solution.py > solution.regenerated.mpy'
(
  cd "${work}" || exit 125
  python3 py2mpy.py solution.py > solution.regenerated.mpy
)
translate_status=$?
echo "EXIT_STATUS: ${translate_status}"

echo 'COMMAND: cmp -s solution.regenerated.mpy solution.submitted.mpy'
cmp -s "${work}/solution.regenerated.mpy" "${work}/solution.submitted.mpy"
cmp_status=$?
echo "EXIT_STATUS: ${cmp_status}"
if [[ ${cmp_status} -eq 0 ]]; then
  echo 'TRANSLATION_BYTE_IDENTITY: PASS'
else
  echo 'TRANSLATION_BYTE_IDENTITY: FAIL'
  diff -u "${work}/solution.submitted.mpy" "${work}/solution.regenerated.mpy"
fi

echo 'COMMAND: sha256sum solution.py solution.submitted.mpy solution.regenerated.mpy'
sha256sum \
  "${work}/solution.py" \
  "${work}/solution.submitted.mpy" \
  "${work}/solution.regenerated.mpy"
hash_status=$?
echo "EXIT_STATUS: ${hash_status}"

echo 'COMMAND: python3 differential_test.py canonical.py solution.py differential_inputs.json'
python3 /audit-output/evidence/differential_test.py \
  "${work}/canonical.py" \
  "${work}/solution.py" \
  /audit-output/evidence/differential_inputs.json
diff_status=$?
echo "EXIT_STATUS: ${diff_status}"

if [[ ${translate_status} -ne 0 || ${cmp_status} -ne 0 || ${hash_status} -ne 0 || ${diff_status} -ne 0 ]]; then
  exit 1
fi
exit 0
