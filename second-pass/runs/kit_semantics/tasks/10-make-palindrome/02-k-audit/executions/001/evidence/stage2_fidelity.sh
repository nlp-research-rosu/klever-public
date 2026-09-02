#!/usr/bin/env bash
set -euo pipefail

echo 'AUDIT COMMAND: bash /audit-output/evidence/stage2_fidelity.sh'
echo 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-clean/solution.py > /tmp/audit-work/candidate-clean/solution.regenerated.mpy'
python3 \
  /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-clean/solution.py \
  > /tmp/audit-work/candidate-clean/solution.regenerated.mpy
sha256sum \
  /tmp/audit-work/candidate-clean/solution.mpy \
  /tmp/audit-work/candidate-clean/solution.regenerated.mpy
cmp \
  /tmp/audit-work/candidate-clean/solution.mpy \
  /tmp/audit-work/candidate-clean/solution.regenerated.mpy
echo "solution_mpy_byte_identity_exit=$?"

echo 'COMMAND: python3 /audit-output/evidence/differential_test.py --dump-inputs /audit-output/evidence/differential_inputs.jsonl'
python3 \
  /audit-output/evidence/differential_test.py \
  --dump-inputs /audit-output/evidence/differential_inputs.jsonl
echo "differential_exit=$?"
wc -l /audit-output/evidence/differential_inputs.jsonl
sha256sum /audit-output/evidence/differential_inputs.jsonl
echo 'STAGE2_FIDELITY_EXIT=0'
