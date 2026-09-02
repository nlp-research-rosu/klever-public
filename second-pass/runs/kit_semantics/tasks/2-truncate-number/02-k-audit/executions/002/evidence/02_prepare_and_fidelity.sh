#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/fresh
if [[ -e "$scratch" ]]; then
  printf 'REFUSING_EXISTING_SCRATCH %s\n' "$scratch"
  exit 90
fi

mkdir -p "$scratch"
cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/submitted-solution.mpy"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/spec.k "$scratch/spec.k"
cp /candidate/spec-vacuity.k "$scratch/candidate-spec-vacuity.k"
cp /candidate/spec-body-mutation.k "$scratch/candidate-spec-body-mutation.k"
cp /candidate/smoke.py "$scratch/smoke.py"
cp /candidate/smoke.mpy "$scratch/submitted-smoke.mpy"
cp /candidate/test_solution.py "$scratch/candidate-test_solution.py"
cp /reference/canonical.py "$scratch/canonical.py"
cp /reference/prompt.py "$scratch/prompt.py"
cp /reference/py2mpy.py "$scratch/py2mpy.py"
cp -a /candidate/reference-semantics "$scratch/reference-semantics"

find "$scratch" -maxdepth 3 -printf '%y %P -> %l\n' | sort
printf 'SCRATCH_SYMLINKS '
find "$scratch" -type l -print | wc -l
printf 'SCRATCH_COMPILED_DIRS '
find "$scratch" -type d -name '*-kompiled' -print | wc -l

cd "$scratch" || exit 91
python3 py2mpy.py solution.py > regenerated-solution.mpy
regen_status=$?
printf 'TRANSLATE_EXIT %s\n' "$regen_status"
cmp -s regenerated-solution.mpy submitted-solution.mpy
cmp_status=$?
printf 'SOLUTION_MPY_BYTE_CMP_EXIT %s\n' "$cmp_status"
sha256sum solution.py submitted-solution.mpy regenerated-solution.mpy

python3 /audit-output/evidence/02_differential.py
diff_status=$?
printf 'DIFFERENTIAL_EXIT %s\n' "$diff_status"

if [[ "$regen_status" -ne 0 || "$cmp_status" -ne 0 || "$diff_status" -ne 0 ]]; then
  exit 1
fi

