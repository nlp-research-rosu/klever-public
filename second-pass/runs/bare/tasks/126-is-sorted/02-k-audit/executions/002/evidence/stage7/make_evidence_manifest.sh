#!/usr/bin/env bash
set -euo pipefail

echo 'COMMAND: find /audit-output/evidence -type f excluding evidence-manifest.sha256, sort, sha256sum'
find /audit-output/evidence -type f \
  ! -path '/audit-output/evidence/stage7/evidence-manifest.sha256' \
  ! -path '/audit-output/evidence/stage7/evidence-manifest-run.log' \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum
