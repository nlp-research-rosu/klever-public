#!/usr/bin/env bash
set -o pipefail

find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '07_evidence_manifest.txt' \
  ! -name '07_evidence_manifest.log' \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum
