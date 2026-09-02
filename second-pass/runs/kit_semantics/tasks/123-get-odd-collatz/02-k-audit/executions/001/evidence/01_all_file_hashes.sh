#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

find /candidate -type f -print0 \
  | LC_ALL=C sort -z \
  | xargs -0 sha256sum \
  > /audit-output/evidence/01_candidate_file_hashes.txt
printf 'candidate_individual_hashes_exit=%s\n' "$?"

find /reference -type f -print0 \
  | LC_ALL=C sort -z \
  | xargs -0 sha256sum \
  > /audit-output/evidence/01_reference_file_hashes.txt
printf 'reference_individual_hashes_exit=%s\n' "$?"

find /generation-evidence -type f -print0 \
  | LC_ALL=C sort -z \
  | xargs -0 sha256sum \
  > /audit-output/evidence/01_generation_file_hashes.txt
printf 'generation_individual_hashes_exit=%s\n' "$?"

wc -lc \
  /audit-output/evidence/01_candidate_file_hashes.txt \
  /audit-output/evidence/01_reference_file_hashes.txt \
  /audit-output/evidence/01_generation_file_hashes.txt
sha256sum \
  /audit-output/evidence/01_candidate_file_hashes.txt \
  /audit-output/evidence/01_reference_file_hashes.txt \
  /audit-output/evidence/01_generation_file_hashes.txt
