#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k \
  /reference/k-proof/semantic.k \
  /reference/k-proof/spec.k \
  /reference/k-proof/solution.py \
  /reference/k-proof/solution.mpy

python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
python3 -m json.tool /reference/klean-generation/input-manifest.json
python3 -m json.tool /reference/klean-generation/export-result.json
python3 -m json.tool /reference/klean-generation/generated/obligation-map.json
python3 -m json.tool /reference/klean-generation/trust-inventory.json
python3 -m json.tool /reference/lemma-discovery.json

nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/prove.sh
