#!/usr/bin/env bash
set -u

printf 'REVIEW terminal markers\n'
tail -n 2 /audit-output/REVIEW.md
printf 'REVIEW marker occurrences\n'
rg -n '^(VERDICT|LEGITIMACY):' /audit-output/REVIEW.md
printf 'EVIDENCE SHA-256 manifest (excluding this generated log)\n'
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '07_evidence_manifest.log' -print0 \
  | sort -z \
  | xargs -0 sha256sum
sha256sum /audit-output/REVIEW.md
