#!/usr/bin/env bash
set -euo pipefail

cd /audit-output
printf 'COMMAND: find evidence -type f excluding EVIDENCE_MANIFEST.sha256; sha256sum in path order\n'
find evidence -type f ! -name EVIDENCE_MANIFEST.sha256 -print0 \
  | sort -z \
  | xargs -0 sha256sum
