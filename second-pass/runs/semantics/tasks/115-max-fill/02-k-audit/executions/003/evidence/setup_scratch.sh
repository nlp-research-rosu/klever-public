#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/115-max-fill-audit
mkdir -p "$scratch"
cp -a /reference/reference-semantics "$scratch/reference-semantics"
cp /reference/canonical.py "$scratch/canonical.py"
cp /reference/prompt.py "$scratch/prompt.py"
cp /reference/py2mpy.py "$scratch/py2mpy.py"
cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/solution.submitted.mpy"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/spec.k "$scratch/spec.k"
find "$scratch" -type l -print
find "$scratch" -maxdepth 3 -type f -printf '%P %s bytes\n' | sort
