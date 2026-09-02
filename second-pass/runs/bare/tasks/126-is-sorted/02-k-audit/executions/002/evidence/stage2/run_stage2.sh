#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate-fresh
if [[ -e "$scratch" || -L "$scratch" ]]; then
  echo "ERROR: scratch destination already exists: $scratch"
  exit 2
fi

echo "COMMAND: mkdir -p $scratch"
mkdir -p "$scratch" || exit $?
echo "COMMAND: cp explicit candidate source artifacts to $scratch"
cp \
  /candidate/list-domain.k \
  /candidate/mutation-spec.k \
  /candidate/prove.sh \
  /candidate/semantic.k \
  /candidate/solution.mpy \
  /candidate/solution.py \
  /candidate/spec.k \
  /candidate/verification.k \
  "$scratch/" || exit $?

echo 'COMMAND: python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy'
(
  cd "$scratch" &&
  python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
)
translate_status=$?
echo "TRANSLATE_EXIT_STATUS=$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

echo 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_status=$?
echo "BYTE_IDENTITY_EXIT_STATUS=$cmp_status"
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
if [[ "$cmp_status" -ne 0 ]]; then
  diff -u "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy" || true
  exit "$cmp_status"
fi

echo 'COMMAND: python3 /audit-output/evidence/stage2/differential_test.py'
python3 /audit-output/evidence/stage2/differential_test.py
test_status=$?
echo "DIFFERENTIAL_EXIT_STATUS=$test_status"
exit "$test_status"
