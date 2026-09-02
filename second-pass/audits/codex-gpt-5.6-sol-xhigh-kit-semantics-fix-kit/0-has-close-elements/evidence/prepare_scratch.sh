#!/usr/bin/env bash
set -euo pipefail
set -x

scratch=/tmp/audit-work/reconstruction
test ! -e "$scratch"
mkdir -p "$scratch"

cp -a /reference/reference-semantics "$scratch/reference-semantics"
cp -a /reference/prompt.py "$scratch/prompt.py"
cp -a /reference/canonical.py "$scratch/canonical.py"
cp -a /reference/py2mpy.py "$scratch/py2mpy.py"

cp -a /candidate/solution.py "$scratch/solution.py"
cp -a /candidate/solution.mpy "$scratch/submitted-solution.mpy"
cp -a /candidate/spec.k "$scratch/spec.k"
cp -a /candidate/verification.k "$scratch/verification.k"

find "$scratch" -maxdepth 3 -printf '%y %p -> %l\n' | sort
