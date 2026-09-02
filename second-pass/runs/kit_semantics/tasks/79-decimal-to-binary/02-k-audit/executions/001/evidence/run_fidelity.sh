#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/79-audit/fidelity
mkdir -p "$scratch"

echo '$ python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/79-audit/fidelity/regenerated-solution.mpy'
python3 /reference/py2mpy.py /candidate/solution.py > "$scratch/regenerated-solution.mpy"
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS=$translate_status"

echo '$ cmp /tmp/audit-work/79-audit/fidelity/regenerated-solution.mpy /candidate/solution.mpy'
cmp "$scratch/regenerated-solution.mpy" /candidate/solution.mpy
cmp_status=$?
echo "CMP_EXIT_STATUS=$cmp_status"

echo '$ sha256sum /tmp/audit-work/79-audit/fidelity/regenerated-solution.mpy /candidate/solution.mpy'
sha256sum "$scratch/regenerated-solution.mpy" /candidate/solution.mpy
hash_status=$?
echo "SHA256_EXIT_STATUS=$hash_status"

echo '$ python3 /audit-output/evidence/differential.py'
python3 /audit-output/evidence/differential.py
diff_status=$?
echo "DIFFERENTIAL_EXIT_STATUS=$diff_status"

if (( translate_status || cmp_status || hash_status || diff_status )); then
  exit 1
fi
exit 0
