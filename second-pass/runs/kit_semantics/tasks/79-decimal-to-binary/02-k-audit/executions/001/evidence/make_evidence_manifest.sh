#!/usr/bin/env bash
set -euo pipefail

find /audit-output/evidence \
  -maxdepth 1 \
  -type f \
  ! -name '07-evidence-manifest.sha256' \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > /audit-output/evidence/07-evidence-manifest.sha256

echo '$ sha256sum of every reviewer evidence file except the manifest itself'
wc -l /audit-output/evidence/07-evidence-manifest.sha256
echo 'EVIDENCE_MANIFEST=PASS'
