#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
{
  sha256sum ../REVIEW.md
  find . -maxdepth 1 -type f ! -name MANIFEST.sha256 -print0 \
    | LC_ALL=C sort -z \
    | xargs -0 sha256sum
} > MANIFEST.sha256
