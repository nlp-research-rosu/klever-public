#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

for file in \
  /reference/klean-generation/generated/Klean106F/Lemmas.lean \
  /reference/klean-generation/generated/Klean106F/Prelude.lean \
  /reference/klean-generation/generated/Klean106F/Func.lean \
  /reference/klean-generation/generated/Klean106F/Rewrite.lean \
  /reference/klean-generation/generated/Klean106F.lean \
  /reference/klean-generation/generated/lakefile.toml \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/trust-inventory.json
do
  printf '\n[%s]\n' "$file"
  nl -ba "$file"
done
