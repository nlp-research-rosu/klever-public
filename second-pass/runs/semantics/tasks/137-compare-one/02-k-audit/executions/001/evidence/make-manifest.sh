#!/usr/bin/env bash
set -euo pipefail

cd /audit-output/evidence
find . -maxdepth 1 -type f ! -name MANIFEST.sha256 -print0 \
  | sort -z \
  | xargs -0 sha256sum > MANIFEST.sha256
