#!/usr/bin/env bash
set -uo pipefail

manifest=/audit-output/evidence/MANIFEST.sha256
find /audit-output/evidence -type f \
  ! -path "$manifest" \
  ! -path "/audit-output/evidence/stage7/manifest_generation.log" \
  ! -path "/audit-output/evidence/stage7/final_review_checks.log" \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum > "$manifest"

printf 'manifest=%s\n' "$manifest"
printf 'entries=%s\n' "$(wc -l < "$manifest")"
sha256sum "$manifest"
