#!/usr/bin/env bash
set -u
trap 'status=$?; printf "EXIT_STATUS=%s\n" "$status"' EXIT
set -x

SCRATCH=/tmp/audit-work/108-count-nums
test ! -e "$SCRATCH"
mkdir "$SCRATCH"
cp /candidate/solution.py "$SCRATCH/solution.py"
cp /candidate/solution.mpy "$SCRATCH/solution.mpy"
cp /candidate/semantic.k "$SCRATCH/semantic.k"
cp /candidate/verification.k "$SCRATCH/verification.k"
cp /candidate/spec.k "$SCRATCH/spec.k"
cp /candidate/prove.sh "$SCRATCH/prove.sh.untrusted"
cp /reference/prompt.py "$SCRATCH/prompt.py"
cp /reference/canonical.py "$SCRATCH/canonical.py"
cp /reference/py2mpy.py "$SCRATCH/py2mpy.py"

python3 "$SCRATCH/py2mpy.py" "$SCRATCH/solution.py" > "$SCRATCH/solution.regenerated.mpy"
cmp "$SCRATCH/solution.mpy" "$SCRATCH/solution.regenerated.mpy"
sha256sum "$SCRATCH/solution.mpy" "$SCRATCH/solution.regenerated.mpy"
python3 /audit-output/evidence/02_differential.py
