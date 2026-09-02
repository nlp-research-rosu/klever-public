#!/usr/bin/env bash
set -euo pipefail

find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '14_evidence_inventory.log' \
  -print0 |
  sort -z |
  xargs -0 sha256sum
sha256sum /audit-output/REVIEW.md
tail -n 2 /audit-output/REVIEW.md
