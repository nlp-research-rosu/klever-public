#!/usr/bin/env bash
set -euo pipefail
set -x

scratch=/tmp/audit-work/88-sort-array
test ! -e "$scratch"
mkdir -p "$scratch"

cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/submitted-solution.mpy"
cp /candidate/semantic.k "$scratch/semantic.k"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/spec.k "$scratch/spec.k"

cp /reference/canonical.py "$scratch/trusted_canonical.py"
cp /reference/prompt.py "$scratch/trusted_prompt.py"
cp /reference/py2mpy.py "$scratch/trusted_py2mpy.py"

find "$scratch" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | LC_ALL=C sort
sha256sum "$scratch"/*
