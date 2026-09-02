#!/usr/bin/env bash
set -euo pipefail
set -x

scratch=/tmp/audit-work/reconstruction

cp /audit-output/evidence/stage4-ground.k "$scratch/stage4-ground.k"

/audit-output/evidence/stage4_generate_concrete.py \
  --solution "$scratch/solution.py" \
  --output "$scratch/stage4-concrete.py"

python3 "$scratch/py2mpy.py" "$scratch/stage4-concrete.py" \
  > "$scratch/stage4-concrete.mpy"

krun "$scratch/stage4-concrete.mpy" \
  --definition "$scratch/runtime-kompiled"
