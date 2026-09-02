#!/usr/bin/env bash
set -euxo pipefail

export PYTHONPATH=/reference
python /audit-output/evidence/04_independent_classification.py
rg -n \
  '\b(simplification|claim|axiom|opaque|sorry|admit|unsafe|theorem)\b' \
  /reference/k-proof/verification.k \
  /reference/klean-generation/generated
test ! -e /candidate
