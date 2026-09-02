#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/forty-triples-audit
cd "$scratch/candidate-src" || exit 1

if [[ -e "$scratch/runtime-kompiled" ]]; then
  echo "REFUSING_EXISTING_DEFINITION $scratch/runtime-kompiled"
  exit 2
fi

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/runtime-kompiled"
