#!/usr/bin/env bash
set -euo pipefail

find /audit-output/evidence -maxdepth 1 -type f \
  ! -name evidence-manifest.log \
  -print0 |
  sort -z |
  xargs -0 sha256sum
