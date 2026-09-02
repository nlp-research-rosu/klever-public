#!/usr/bin/env bash
set -u

printf 'working directory: '
pwd
printf 'date (UTC): '
date -u +'%Y-%m-%dT%H:%M:%SZ'
printf 'python: '
python3 --version
kompile --version
kprove --version

printf '\nTrusted input hashes:\n'
sha256sum \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py

printf '\nCandidate source/proof hashes:\n'
sha256sum \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k

printf '\nEvidence files before manifest:\n'
find /audit-output/evidence -maxdepth 1 -type f -printf '%f\n' | LC_ALL=C sort
