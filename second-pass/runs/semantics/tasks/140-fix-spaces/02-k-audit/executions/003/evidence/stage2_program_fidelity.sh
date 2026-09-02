#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/140-fix-spaces

echo '$ test that the dedicated scratch path does not preexist'
test ! -e "$scratch"
echo "exit=$?"

echo '$ make clean scratch directories'
mkdir -p "$scratch/source"
echo "exit=$?"

echo '$ copy candidate source artifacts and trusted inputs to scratch'
cp -a \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/concrete-tests.py \
  /candidate/concrete-tests.mpy \
  "$scratch/source/"
cp -a /reference/py2mpy.py /reference/prompt.py /reference/canonical.py "$scratch/source/"
cp -a /reference/reference-semantics "$scratch/source/"
echo "exit=$?"

echo '$ regenerate solution.mpy with the trusted translator'
cd "$scratch/source" || exit 90
python3 py2mpy.py solution.py > regenerated-solution.mpy
regen_status=$?
echo "exit=$regen_status"

echo '$ require byte identity between submitted and regenerated solution.mpy'
cmp solution.mpy regenerated-solution.mpy
cmp_status=$?
echo "exit=$cmp_status"
sha256sum solution.mpy regenerated-solution.mpy

echo '$ run independent canonical-versus-candidate differential test'
python3 /audit-output/evidence/differential_test.py canonical.py solution.py
diff_status=$?
echo "exit=$diff_status"

if [ "$regen_status" -ne 0 ] || [ "$cmp_status" -ne 0 ]; then
  exit 1
fi
# A differential mismatch is an audit finding, not a script infrastructure error.
exit 0
