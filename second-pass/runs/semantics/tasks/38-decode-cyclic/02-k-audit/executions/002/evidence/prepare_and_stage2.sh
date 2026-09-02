#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/38-decode-cyclic
log=/audit-output/evidence/stage2_fidelity.log

mkdir -p "$scratch/trusted"
cp -a /candidate/solution.py "$scratch/solution.py"
cp -a /candidate/solution.mpy "$scratch/solution.submitted.mpy"
cp -a /candidate/spec.k "$scratch/spec.k"
cp -a /candidate/verification.k "$scratch/verification.k"
cp -a /candidate/prove.sh "$scratch/prove.sh"
cp -a /candidate/concrete_tests.py "$scratch/concrete_tests.candidate.py"
cp -a /candidate/concrete_tests.mpy "$scratch/concrete_tests.candidate.mpy"
cp -a /reference/reference-semantics "$scratch/reference-semantics"
cp -a /reference/canonical.py "$scratch/trusted/canonical.py"
cp -a /reference/prompt.py "$scratch/trusted/prompt.py"
cp -a /reference/py2mpy.py "$scratch/py2mpy.py"

{
  echo '$ python3 /tmp/audit-work/38-decode-cyclic/py2mpy.py /tmp/audit-work/38-decode-cyclic/solution.py > /tmp/audit-work/38-decode-cyclic/solution.regenerated.mpy'
  python3 "$scratch/py2mpy.py" "$scratch/solution.py" >"$scratch/solution.regenerated.mpy"
  regen_status=$?
  echo "TRANSLATE_EXIT_STATUS=$regen_status"

  echo '$ cmp /tmp/audit-work/38-decode-cyclic/solution.regenerated.mpy /tmp/audit-work/38-decode-cyclic/solution.submitted.mpy'
  cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.submitted.mpy"
  cmp_status=$?
  echo "BYTE_IDENTITY_EXIT_STATUS=$cmp_status"

  echo '$ sha256sum /tmp/audit-work/38-decode-cyclic/solution.regenerated.mpy /tmp/audit-work/38-decode-cyclic/solution.submitted.mpy'
  sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.submitted.mpy"
  hash_status=$?
  echo "SHA256_EXIT_STATUS=$hash_status"

  echo '$ python3 /audit-output/evidence/differential_test.py'
  python3 /audit-output/evidence/differential_test.py
  diff_status=$?
  echo "DIFFERENTIAL_EXIT_STATUS=$diff_status"

  if (( regen_status != 0 || cmp_status != 0 || hash_status != 0 || diff_status != 0 )); then
    exit 1
  fi
  exit 0
} >"$log" 2>&1
