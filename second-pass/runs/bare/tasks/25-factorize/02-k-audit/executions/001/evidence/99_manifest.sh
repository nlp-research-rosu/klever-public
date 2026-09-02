#!/usr/bin/env bash
set -euo pipefail

evidence_dir=/audit-output/evidence
manifest="$evidence_dir/MANIFEST.sha256"

echo "$ find $evidence_dir -maxdepth 1 -type f ! -name MANIFEST.sha256 -print0 | sort -z | xargs -0 sha256sum > $manifest"
find "$evidence_dir" -maxdepth 1 -type f ! -name MANIFEST.sha256 -print0 \
  | sort -z \
  | xargs -0 sha256sum > "$manifest"
printf '[exit_status=0]\n'
wc -l "$manifest"
