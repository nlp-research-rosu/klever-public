#!/usr/bin/env bash
set -u

printf 'COMMAND: find /audit-output/evidence -maxdepth 1 -type f -not -name 07_evidence_manifest.log -print0 | sort -z | xargs -0 sha256sum\n'
find /audit-output/evidence \
  -maxdepth 1 \
  -type f \
  -not -name 07_evidence_manifest.log \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum
printf 'EXIT_STATUS: %d\n' "$?"
