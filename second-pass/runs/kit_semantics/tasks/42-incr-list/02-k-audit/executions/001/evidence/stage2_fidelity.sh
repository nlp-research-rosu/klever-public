#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/42-incr-list-audit
mkdir -p "$scratch"
cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/submitted-solution.mpy"
cp /candidate/spec.k "$scratch/spec.k"
cp /candidate/verification.k "$scratch/verification.k"
cp /reference/py2mpy.py "$scratch/py2mpy.py"
cp /reference/prompt.py "$scratch/prompt.py"
cp /reference/canonical.py "$scratch/canonical.py"
cp -R /reference/reference-semantics "$scratch/reference-semantics"

echo '$ python3 py2mpy.py solution.py > regenerated-solution.mpy'
(
  cd "$scratch"
  python3 py2mpy.py solution.py > regenerated-solution.mpy
)
echo '$ cmp -s regenerated-solution.mpy submitted-solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/submitted-solution.mpy"
echo "translator_byte_identity_exit=0"
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/submitted-solution.mpy"

echo '$ python3 -m py_compile solution.py'
(
  cd "$scratch"
  python3 -m py_compile solution.py
)

echo '$ python3 /audit-output/evidence/stage2_differential.py'
python3 /audit-output/evidence/stage2_differential.py

echo "STAGE2_FIDELITY_OK"
