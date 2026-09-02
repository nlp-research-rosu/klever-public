#!/usr/bin/env bash
set -euo pipefail
set -o xtrace
scratch=/tmp/audit-work/54-same-chars
test ! -e "$scratch"
mkdir -p "$scratch"
cp -a /reference/reference-semantics "$scratch/reference-semantics"
cp /reference/canonical.py "$scratch/canonical.py"
cp /reference/prompt.py "$scratch/prompt.py"
cp /reference/py2mpy.py "$scratch/py2mpy.py"
cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/solution.mpy"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/spec.k "$scratch/spec.k"
cp /candidate/spec-vacuity.k "$scratch/candidate-spec-vacuity.k"
cp /candidate/spec-body-mutation.k "$scratch/candidate-spec-body-mutation.k"
find "$scratch" -type l -print
find "$scratch" -maxdepth 2 -printf '%y %P\n' | sort
printf 'EXIT_STATUS=0\n'
