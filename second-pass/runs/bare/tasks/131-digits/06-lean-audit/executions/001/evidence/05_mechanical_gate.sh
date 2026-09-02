#!/usr/bin/env bash
set -euxo pipefail

export PYTHONPATH=/reference
export LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so
python /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json \
  --output /audit-output/evidence/05_mechanical_gate.json
sed -n '1,360p' /audit-output/evidence/05_mechanical_gate.json
