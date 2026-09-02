#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruction
mkdir -p "$scratch"

cp -a /reference/reference-semantics "$scratch/reference-semantics"
cp -a /reference/canonical.py "$scratch/canonical.py"
cp -a /reference/prompt.py "$scratch/prompt.py"
cp -a /reference/py2mpy.py "$scratch/py2mpy.py"

for source_name in \
  solution.py solution.mpy verification.k spec.k prove.sh PROOF.md \
  spec-vacuity.k spec-body-mutation.k spec-loop-body-mutation.k \
  spec-value-mutation.k concrete_tests.py concrete_tests.mpy test_solution.py
do
  cp -a "/candidate/$source_name" "$scratch/$source_name"
done

find "$scratch" -maxdepth 3 -type l -print
find "$scratch" -maxdepth 3 -type f -printf '%P\n' | sort
