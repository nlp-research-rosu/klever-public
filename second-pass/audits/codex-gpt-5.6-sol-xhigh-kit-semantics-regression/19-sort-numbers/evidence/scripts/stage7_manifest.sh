#!/usr/bin/env bash
set -u

find /audit-output/evidence -type f \
  ! -name 'stage7-evidence-manifest.log' \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum
