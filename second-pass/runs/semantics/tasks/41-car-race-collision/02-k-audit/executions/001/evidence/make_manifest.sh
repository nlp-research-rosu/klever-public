#!/usr/bin/env bash
set -euo pipefail

evidence_root=/audit-output/evidence
manifest_path=$evidence_root/SHA256SUMS

find "$evidence_root" -maxdepth 1 -type f \
  ! -name SHA256SUMS \
  ! -name stage7-manifest.log \
  -print0 |
  sort -z |
  xargs -0 sha256sum >"$manifest_path"

printf 'manifest=%s\n' "$manifest_path"
printf 'entry_count=%s\n' "$(wc -l <"$manifest_path")"
