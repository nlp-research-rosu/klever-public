#!/usr/bin/env bash
set -uo pipefail

cd /audit-output || exit 1
find evidence -type f \
  ! -name 'MANIFEST.sha256' \
  ! -name '07_manifest.log' \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum > evidence/MANIFEST.sha256
sha256sum REVIEW.md evidence/MANIFEST.sha256
wc -l evidence/MANIFEST.sha256
