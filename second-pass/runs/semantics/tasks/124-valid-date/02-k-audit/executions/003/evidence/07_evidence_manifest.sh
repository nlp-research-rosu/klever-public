#!/usr/bin/env bash
set -uo pipefail

OUT=/audit-output/evidence/07_evidence_manifest.log
TMP=/tmp/audit-work/124-valid-date/07_evidence_manifest.raw

{
  printf '%s\n' 'COMMAND: sha256sum reviewer-authored evidence artifacts'
  find /audit-output/evidence -maxdepth 1 -type f \
    ! -name '07_evidence_manifest.log' \
    -print0 |
    sort -z |
    xargs -0 sha256sum
  printf 'EXIT_STATUS: %s\n' "$?"
} >"$TMP" 2>&1

cp "$TMP" "$OUT"
sed -n '1,320p' "$OUT"
