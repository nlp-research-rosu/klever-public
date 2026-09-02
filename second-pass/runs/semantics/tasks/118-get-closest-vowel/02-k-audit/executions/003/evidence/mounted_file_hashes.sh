#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' 'COMMAND: find mounted inputs -type f -print0 | sort -z | xargs -0 sha256sum'
find \
  /candidate \
  /reference \
  /generation-evidence \
  -type f -print0 |
  sort -z |
  xargs -0 sha256sum

printf '%s\n' 'COMMAND: find mounted inputs -printf entry-type/path/link-target'
find \
  /candidate \
  /reference \
  /generation-evidence \
  -printf '%y %p -> %l\n' |
  sort
