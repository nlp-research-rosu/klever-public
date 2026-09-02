#!/usr/bin/env bash
set -u

printf '%s\n' '# Candidate source hashes copied into clean scratch'
sha256sum \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k
printf '%s\n' '# Scratch source hashes'
sha256sum \
  /tmp/audit-work/reconstruction/solution.py \
  /tmp/audit-work/reconstruction/solution.mpy \
  /tmp/audit-work/reconstruction/spec.k \
  /tmp/audit-work/reconstruction/verification.k
printf '%s\n' '# Candidate compiled/cache directories were not source inputs'
find /candidate -maxdepth 1 -type d -name '*-kompiled' -printf '%f\n' | sort
printf '%s\n' '# Reviewer build directories created only in scratch'
find /tmp/audit-work/reconstruction -maxdepth 1 -type d \
  -name 'audit-*-kompiled' -printf '%f\n' | sort
