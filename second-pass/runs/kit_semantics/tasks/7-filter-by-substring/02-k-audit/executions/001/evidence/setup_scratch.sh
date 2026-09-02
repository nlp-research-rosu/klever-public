#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruction
test ! -e "$scratch"
mkdir -p "$scratch/reference-semantics"

cp -a /reference/reference-semantics/. "$scratch/reference-semantics/"
cp -a /reference/canonical.py "$scratch/canonical.py"
cp -a /reference/prompt.py "$scratch/prompt.py"
cp -a /reference/py2mpy.py "$scratch/py2mpy.py"

for artifact in \
  solution.py \
  solution.mpy \
  verification.k \
  spec.k \
  prove.sh \
  concrete-smoke.py \
  concrete-smoke.mpy \
  spec-value-check.k \
  spec-vacuity.k \
  spec-body-mutation.k \
  spec-value-opposite.k
do
  cp -a "/candidate/$artifact" "$scratch/$artifact"
done

find "$scratch" -printf '%y %m %s %P -> %l\n' | sort
