#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

export PYTHONPATH=/reference
printf 'All image/source provenance fields in audit input\n'
rg -n 'image_id|image|producer|stage4' /audit-input.json
printf '\nDirect file hashes\n'
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k \
  /reference/k-proof/solution.py \
  /reference/k-proof/solution.mpy
printf '\nStructured provenance checks\n'
python3 /audit-output/evidence/check_provenance_hashes.py
