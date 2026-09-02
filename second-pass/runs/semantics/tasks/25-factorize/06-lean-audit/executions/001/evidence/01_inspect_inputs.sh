#!/usr/bin/env bash
set -uo pipefail

echo '$ env | grep "^AUDIT_MODE="'
env | grep '^AUDIT_MODE='

echo '$ sha256sum /audit-input.json /reference/lemma-discovery.json /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json /reference/klean-generation/generator-manifest.json /reference/klean-generation/input-manifest.json /reference/klean-generation/export-result.json /reference/klean-generation/generated/obligation-map.json /reference/klean-generation/preflight.json /reference/klean-generation/trust-inventory.json'
sha256sum \
  /audit-input.json \
  /reference/lemma-discovery.json \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-generation/preflight.json \
  /reference/klean-generation/trust-inventory.json

for path in \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-generation/preflight.json \
  /reference/klean-generation/trust-inventory.json \
  /reference/lemma-discovery.json
do
  echo "\$ python3 -m json.tool $path"
  python3 -m json.tool "$path"
done

echo '$ sed -n "1,260p" /reference/k-proof/verification.k'
sed -n '1,260p' /reference/k-proof/verification.k

echo '$ sed -n "1,260p" /reference/k-proof/spec.k'
sed -n '1,260p' /reference/k-proof/spec.k

echo '$ sed -n "1,260p" /reference/k-proof/solution.py'
sed -n '1,260p' /reference/k-proof/solution.py

echo '$ sed -n "1,320p" /reference/k-proof/solution.mpy'
sed -n '1,320p' /reference/k-proof/solution.mpy

echo '$ sed -n "1,260p" /reference/k-proof/reference-semantics/semantics.k'
sed -n '1,260p' /reference/k-proof/reference-semantics/semantics.k

echo '$ find /reference/k-proof/reference-semantics -type f -name "*.k" -printf "%p\\n" | sort'
find /reference/k-proof/reference-semantics -type f -name '*.k' -printf '%p\n' | sort

echo '$ find /reference/klean-generation/generated -type f -printf "%P\\n" | sort'
find /reference/klean-generation/generated -type f -printf '%P\n' | sort

echo '$ if [ -d /candidate ]; then find /candidate -mindepth 1 -print; else echo "/candidate absent (expected in CLASSIFICATION_ONLY)"; fi'
if [ -d /candidate ]; then
  find /candidate -mindepth 1 -print
else
  echo '/candidate absent (expected in CLASSIFICATION_ONLY)'
fi
