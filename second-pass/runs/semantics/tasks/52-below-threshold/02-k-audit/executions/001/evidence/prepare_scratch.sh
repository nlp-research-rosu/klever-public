#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/52-below-threshold
if [[ -e "$scratch" ]]; then
  echo "refusing to reuse existing scratch path: $scratch" >&2
  exit 73
fi

mkdir -p "$scratch"
cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/submitted-solution.mpy"
cp /candidate/spec.k "$scratch/spec.k"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/concrete-tests.py "$scratch/candidate-concrete-tests.py"
cp /reference/canonical.py "$scratch/canonical.py"
cp /reference/prompt.py "$scratch/prompt.py"
cp /reference/py2mpy.py "$scratch/py2mpy.py"
cp -a /reference/reference-semantics "$scratch/reference-semantics"

echo "SCRATCH=$scratch"
find "$scratch" -type f -printf '%P\n' | sort
