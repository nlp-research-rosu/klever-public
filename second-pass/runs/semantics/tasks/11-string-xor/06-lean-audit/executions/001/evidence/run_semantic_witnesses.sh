#!/usr/bin/env bash
set -euo pipefail

kompile /reference/k-proof/reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/semantic-runtime-kompiled
build_code=$?
echo "KOMPILE_EXIT_CODE=$build_code"

krun /audit-output/evidence/semantic_witnesses.mpy \
  --definition /tmp/audit-work/semantic-runtime-kompiled
witness_code=$?
echo "WITNESSES_EXIT_CODE=$witness_code"

set +e
krun /audit-output/evidence/semantic_counterfactual.mpy \
  --definition /tmp/audit-work/semantic-runtime-kompiled
mutation_code=$?
set -e
echo "COUNTERFACTUAL_EXIT_CODE=$mutation_code"
if [[ "$mutation_code" -eq 0 ]]; then
  echo "ERROR: counterfactual was not rejected"
  exit 90
fi
