#!/usr/bin/env bash
set -euo pipefail

find /audit-output/evidence -maxdepth 1 -type f \
  ! -name MANIFEST.sha256 \
  ! -name manifest_generation.log \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > /audit-output/evidence/MANIFEST.sha256
sha256sum /audit-output/REVIEW.md >> /audit-output/evidence/MANIFEST.sha256

printf 'COMMAND: find /audit-output/evidence ... | sort -z | xargs -0 sha256sum > /audit-output/evidence/MANIFEST.sha256; sha256sum /audit-output/REVIEW.md appended\n'
printf 'EXIT STATUS: 0\n'
printf 'MANIFEST ENTRIES: '
wc -l < /audit-output/evidence/MANIFEST.sha256
