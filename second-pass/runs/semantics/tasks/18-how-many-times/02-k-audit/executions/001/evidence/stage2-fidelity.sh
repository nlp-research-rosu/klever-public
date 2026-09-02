#!/usr/bin/env bash
set -u
set -x

work=/tmp/audit-work/fresh
mkdir -p "$work"
cp /candidate/solution.py "$work/solution.py"
cp /candidate/solution.mpy "$work/submitted-solution.mpy"
cp /candidate/spec.k "$work/spec.k"
cp /candidate/verification.k "$work/verification.k"
cp -a /reference/reference-semantics "$work/reference-semantics"
cp /reference/py2mpy.py "$work/py2mpy.py"

python3 "$work/py2mpy.py" "$work/solution.py" > "$work/regenerated-solution.mpy"
translate_rc=$?
echo "TRANSLATE_EXIT=$translate_rc"
cmp "$work/regenerated-solution.mpy" "$work/submitted-solution.mpy"
cmp_rc=$?
echo "SOLUTION_MPY_CMP_EXIT=$cmp_rc"
sha256sum "$work/regenerated-solution.mpy" "$work/submitted-solution.mpy"

python3 /audit-output/evidence/differential.py
diff_rc=$?
echo "DIFFERENTIAL_EXIT=$diff_rc"

exit "$((translate_rc != 0 || cmp_rc != 0 || diff_rc != 0))"
