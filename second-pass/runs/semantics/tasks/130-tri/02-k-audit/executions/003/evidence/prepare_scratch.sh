#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/130-tri-audit
if [[ -e "$scratch" || -L "$scratch" ]]; then
  printf 'Refusing to overwrite existing scratch path: %s\n' "$scratch" >&2
  exit 2
fi

printf 'COMMAND: mkdir -p %s\n' "$scratch"
mkdir -p "$scratch"

printf 'COMMAND: cp candidate source artifacts into scratch\n'
cp /candidate/solution.py "$scratch/solution.py"
cp /candidate/solution.mpy "$scratch/solution.submitted.mpy"
cp /candidate/verification.k "$scratch/verification.k"
cp /candidate/spec.k "$scratch/spec.k"
cp /candidate/prove.sh "$scratch/prove.candidate.sh"

printf 'COMMAND: cp trusted prompt, canonical, translator, and supplied semantics into scratch\n'
cp /reference/prompt.py "$scratch/prompt.trusted.py"
cp /reference/canonical.py "$scratch/canonical.trusted.py"
cp /reference/py2mpy.py "$scratch/py2mpy.trusted.py"
cp -a /reference/reference-semantics "$scratch/reference-semantics"

printf 'SCRATCH_SOURCE_TREE\n'
find "$scratch" -printf '%y %p -> %l\n' | sort
printf 'EXIT_STATUS: 0\n'
