#!/usr/bin/env bash
set -euo pipefail

audit_work=/tmp/audit-work
scratch="$audit_work/scratch"
trusted="$audit_work/trusted"

if [[ -e "$scratch" || -e "$trusted" ]]; then
  echo "refusing to reuse an existing scratch or trusted directory" >&2
  exit 73
fi

mkdir -p "$scratch" "$trusted"

cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/submitted-solution.mpy"
cp /candidate/spec.k "$scratch/spec.k"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/concrete_tests.py "$scratch/candidate-concrete_tests.py"
cp /candidate/concrete_tests.mpy "$scratch/submitted-concrete_tests.mpy"

cp /reference/canonical.py "$trusted/canonical.py"
cp /reference/prompt.py "$trusted/prompt.py"
cp /reference/py2mpy.py "$trusted/py2mpy.py"

# Use a fresh copy of the trusted supplied semantics for every executable audit.
cp -a /reference/reference-semantics "$scratch/reference-semantics"

find "$audit_work" -maxdepth 3 -printf '%y %p -> %l\n' | sort
