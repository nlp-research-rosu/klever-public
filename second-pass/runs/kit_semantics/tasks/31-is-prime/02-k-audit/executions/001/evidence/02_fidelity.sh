#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/prime31

echo '$ cp -a <trusted and candidate source artifacts> /tmp/audit-work/prime31/'
cp -a /reference/reference-semantics "$scratch/reference-semantics"
cp -a /reference/canonical.py "$scratch/canonical.py"
cp -a /reference/prompt.py "$scratch/prompt.py"
cp -a /reference/py2mpy.py "$scratch/py2mpy.py"
cp -a /candidate/solution.py "$scratch/solution.py"
cp -a /candidate/solution.mpy "$scratch/submitted-solution.mpy"
cp -a /candidate/verification.k "$scratch/verification.k"
cp -a /candidate/spec.k "$scratch/spec.k"
echo "EXIT: $?"

echo '$ python3 /reference/py2mpy.py /tmp/audit-work/prime31/solution.py > /tmp/audit-work/prime31/regenerated-solution.mpy'
python3 /reference/py2mpy.py "$scratch/solution.py" > "$scratch/regenerated-solution.mpy"
echo "EXIT: $?"

echo '$ cmp -s regenerated-solution.mpy submitted-solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/submitted-solution.mpy"
echo "EXIT: $?"

echo '$ sha256sum submitted-solution.mpy regenerated-solution.mpy'
sha256sum "$scratch/submitted-solution.mpy" "$scratch/regenerated-solution.mpy"
echo "EXIT: $?"

echo '$ python3 -m py_compile /tmp/audit-work/prime31/solution.py'
python3 -m py_compile "$scratch/solution.py"
echo "EXIT: $?"

echo '$ python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
echo "EXIT: $?"
