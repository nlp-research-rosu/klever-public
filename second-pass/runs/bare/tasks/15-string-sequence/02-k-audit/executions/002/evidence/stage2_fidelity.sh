#!/usr/bin/env bash
set -u

printf 'COMMAND: bash /audit-output/evidence/stage2_fidelity.sh\n'
scratch=/tmp/audit-work/reconstruction
mkdir -p "$scratch"
for name in \
  prompt.py \
  py2mpy.py \
  solution.py \
  solution.mpy \
  semantic.k \
  verification.k \
  spec.k \
  prove.sh
do
  cp "/candidate/$name" "$scratch/$name"
done
cp /reference/canonical.py "$scratch/canonical.py"
cp /reference/prompt.py "$scratch/trusted-prompt.py"
cp /reference/py2mpy.py "$scratch/trusted-py2mpy.py"

printf '\nScratch source inventory\n'
find "$scratch" -maxdepth 1 -type f -printf '%f|%s\n' | LC_ALL=C sort

printf '\nTrusted regeneration\n'
printf 'COMMAND: cd %s && PYTHONDONTWRITEBYTECODE=1 python3 trusted-py2mpy.py solution.py > solution.regenerated.mpy\n' "$scratch"
(
  cd "$scratch" || exit 1
  PYTHONDONTWRITEBYTECODE=1 python3 trusted-py2mpy.py solution.py \
    > solution.regenerated.mpy
)
regen_status=$?
printf 'regeneration_exit=%s\n' "$regen_status"
sha256sum "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"
cmp -s "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"
cmp_status=$?
printf 'submitted_vs_regenerated_cmp_exit=%s\n' "$cmp_status"

printf '\nIndependent Python differential\n'
PYTHONDONTWRITEBYTECODE=1 python3 \
  /audit-output/evidence/differential_test.py
diff_status=$?
printf 'differential_exit=%s\n' "$diff_status"

final_status=0
if [[ "$regen_status" != 0 || "$cmp_status" != 0 || "$diff_status" != 0 ]]; then
  final_status=1
fi
printf 'SCRIPT_EXIT=%s\n' "$final_status"
exit "$final_status"
