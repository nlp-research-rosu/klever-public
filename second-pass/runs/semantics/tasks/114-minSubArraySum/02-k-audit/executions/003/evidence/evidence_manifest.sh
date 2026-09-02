#!/usr/bin/env bash
set -u

find -P /audit-output/evidence -maxdepth 1 -type f \
  ! -name evidence_manifest.log \
  -print0 |
  sort -z |
  xargs -0 sha256sum
sha256sum /audit-output/REVIEW.md
