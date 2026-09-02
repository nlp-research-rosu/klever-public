#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/forty-triples-audit
cd "$scratch/candidate-src" || exit 1

if [[ -e "$scratch/verification-kompiled" ]]; then
  echo "REFUSING_EXISTING_DEFINITION $scratch/verification-kompiled"
  exit 2
fi

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/verification-kompiled"
