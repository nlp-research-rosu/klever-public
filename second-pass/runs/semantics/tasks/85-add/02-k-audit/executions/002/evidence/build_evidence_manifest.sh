#!/usr/bin/env bash
set -eu

cd /audit-output/evidence
find . -type f ! -name evidence_manifest.txt -print0 \
  | sort -z \
  | xargs -0 sha256sum
