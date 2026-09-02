#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' 'COMMAND: find /audit-output/evidence -maxdepth 1 -type f excluding 07_evidence_manifest.log; sort; sha256sum'
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '07_evidence_manifest.log' \
  -printf '%f\n' |
  sort
printf '%s\n' 'SHA256:'
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '07_evidence_manifest.log' \
  -print0 |
  sort -z |
  xargs -0 sha256sum
