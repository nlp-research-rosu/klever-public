#!/usr/bin/env bash
set -uo pipefail
set -x

scratch=/tmp/audit-work/candidate-src
mkdir -p "$scratch"

cp -a \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/bridge-witness.k \
  /candidate/spec-vacuity.k \
  "$scratch/"

cp -a /reference/canonical.py "$scratch/trusted-canonical.py"
cp -a /reference/prompt.py "$scratch/trusted-prompt.py"
cp -a /reference/py2mpy.py "$scratch/trusted-py2mpy.py"
cp -a /reference/reference-semantics "$scratch/"

python3 "$scratch/trusted-py2mpy.py" "$scratch/solution.py" \
  > "$scratch/solution.regenerated.mpy"
translation_status=$?
printf 'trusted_translation_status=%s\n' "$translation_status"

cmp -s "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
identity_status=$?
printf 'solution_mpy_byte_identity_status=%s\n' "$identity_status"
sha256sum "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"

python3 /audit-output/evidence/differential_test.py
differential_status=$?
printf 'differential_test_status=%s\n' "$differential_status"

if (( translation_status != 0 || identity_status != 0 || differential_status != 0 )); then
  exit 1
fi
