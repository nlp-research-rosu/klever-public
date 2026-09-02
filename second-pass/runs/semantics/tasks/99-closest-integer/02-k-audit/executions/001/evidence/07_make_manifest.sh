#!/usr/bin/env bash
set -euo pipefail

cd /audit-output
find evidence -maxdepth 1 -type f \
  ! -name MANIFEST.sha256 \
  ! -name 07_manifest.log \
  -print0 \
  | LC_ALL=C sort -z \
  | xargs -0 sha256sum \
  > evidence/MANIFEST.sha256
wc -l evidence/MANIFEST.sha256
