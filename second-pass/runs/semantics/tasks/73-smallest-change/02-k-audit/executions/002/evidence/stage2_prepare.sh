#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/73-smallest-change

if [[ -e "$scratch" ]]; then
  echo "Refusing to overwrite existing scratch path: $scratch" >&2
  exit 73
fi

mkdir -p "$scratch"
cp -a /candidate/solution.py "$scratch/solution.py"
cp -a /candidate/solution.mpy "$scratch/solution.mpy"
cp -a /candidate/spec.k "$scratch/spec.k"
cp -a /candidate/verification.k "$scratch/verification.k"
cp -a /candidate/prove.sh "$scratch/prove.sh"
cp -a /candidate/concrete-tests.py "$scratch/concrete-tests.py"
cp -a /candidate/concrete-tests.mpy "$scratch/concrete-tests.mpy"
cp -a /candidate/prompt.py "$scratch/prompt.py"
cp -a /candidate/py2mpy.py "$scratch/py2mpy.py"
cp -a /candidate/reference-semantics "$scratch/reference-semantics"
cp -a /reference/canonical.py "$scratch/trusted-canonical.py"
cp -a /reference/prompt.py "$scratch/trusted-prompt.py"
cp -a /reference/py2mpy.py "$scratch/trusted-py2mpy.py"

find "$scratch" -maxdepth 3 -printf '%y %P -> %l\n' | sort
