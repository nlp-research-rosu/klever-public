#!/usr/bin/env bash
set -euo pipefail

scratch_root=/tmp/audit-work/88-sort-array
if [[ -e "$scratch_root" ]]; then
  printf 'Refusing to overwrite existing scratch path: %s\n' "$scratch_root" >&2
  exit 3
fi

mkdir -p "$scratch_root"
cp /candidate/solution.py "$scratch_root/solution.py"
cp /candidate/solution.mpy "$scratch_root/submitted-solution.mpy"
cp /candidate/spec.k "$scratch_root/spec.k"
cp /candidate/verification.k "$scratch_root/verification.k"
cp /candidate/concrete_tests.py "$scratch_root/candidate-concrete-tests.py"
cp /candidate/concrete_tests.mpy "$scratch_root/candidate-concrete-tests.mpy"
cp /reference/canonical.py "$scratch_root/canonical.py"
cp /reference/prompt.py "$scratch_root/prompt.py"
cp /reference/py2mpy.py "$scratch_root/py2mpy.py"
cp -a /reference/reference-semantics "$scratch_root/reference-semantics"

find "$scratch_root" -printf '%y %p -> %l\n' | sort
