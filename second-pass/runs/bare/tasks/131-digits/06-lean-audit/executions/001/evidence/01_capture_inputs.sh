#!/usr/bin/env bash
set -euxo pipefail

pwd
printenv AUDIT_MODE
sha256sum /reference/generation-tools/klean_export.py
sha256sum /reference/generation-tools/klean.py
sha256sum /reference/generation-tools/source-manifest.json
sha256sum /reference/klean-generation/generator-manifest.json
sha256sum /reference/klean-generation/input-manifest.json
sha256sum /reference/klean-generation/export-result.json
sha256sum /reference/klean-generation/preflight.json
sha256sum /reference/klean-generation/trust-inventory.json
sha256sum /reference/lemma-discovery.json
sha256sum /reference/k-proof/verification.k
sha256sum /audit-input.json
sed -n '1,320p' /reference/generation-tools/source-manifest.json
sed -n '1,420p' /reference/klean-generation/generator-manifest.json
sed -n '1,420p' /reference/klean-generation/input-manifest.json
sed -n '1,320p' /reference/klean-generation/export-result.json
sed -n '1,320p' /reference/klean-generation/preflight.json
sed -n '1,420p' /audit-input.json
find /reference/klean-generation -maxdepth 4 -printf '%y %P\n'
if [[ -e /candidate ]]; then
  find /candidate -maxdepth 4 -printf '%y %P\n'
else
  printf '%s\n' '/candidate ABSENT'
fi
