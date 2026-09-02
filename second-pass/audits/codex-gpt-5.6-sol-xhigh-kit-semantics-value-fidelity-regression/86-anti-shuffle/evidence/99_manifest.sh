#!/usr/bin/env bash
set -u

printf 'COMMAND: find /audit-output/evidence -maxdepth 1 -type f -printf ... | sort\n'
find /audit-output/evidence -maxdepth 1 -type f \
  -printf '%f\t%s bytes\n' | sort
printf 'EXIT: %d\n\n' "$?"

printf 'COMMAND: sha256sum /audit-output/REVIEW.md\n'
sha256sum /audit-output/REVIEW.md
printf 'EXIT: %d\n\n' "$?"

printf 'COMMAND: tail -n 2 /audit-output/REVIEW.md\n'
tail -n 2 /audit-output/REVIEW.md
printf 'EXIT: %d\n' "$?"
