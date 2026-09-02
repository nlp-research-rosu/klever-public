#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction

echo '$ mkdir -p /tmp/audit-work/reconstruction/reference-semantics'
mkdir -p "$scratch/reference-semantics"
echo "EXIT_STATUS=$?"

echo '$ copy candidate proof sources and trusted inputs into scratch'
cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/solution.mpy"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/spec.k "$scratch/spec.k"
cp /reference/py2mpy.py "$scratch/py2mpy.py"
cp /reference/prompt.py "$scratch/prompt.py"
cp /reference/canonical.py "$scratch/canonical.py"
cp -a /reference/reference-semantics/. "$scratch/reference-semantics/"
copy_status=$?
echo "EXIT_STATUS=$copy_status"

echo '$ python3 trusted py2mpy.py solution.py > regenerated-solution.mpy'
python3 "$scratch/py2mpy.py" "$scratch/solution.py" \
  > "$scratch/regenerated-solution.mpy"
translation_status=$?
echo "EXIT_STATUS=$translation_status"

echo '$ cmp regenerated-solution.mpy submitted solution.mpy'
cmp "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_status=$?
echo "EXIT_STATUS=$cmp_status"
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"

echo '$ python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
differential_status=$?
echo "EXIT_STATUS=$differential_status (1 means an observed semantic mismatch)"

if (( copy_status != 0 || translation_status != 0 || cmp_status != 0 )); then
  exit 2
fi
exit "$differential_status"
