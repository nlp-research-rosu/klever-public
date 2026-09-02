#!/usr/bin/env bash
set -euo pipefail

for audit_file in \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/prove.sh \
  /candidate/concrete-tests.py \
  /candidate/concrete-tests.mpy
do
  printf '\nFILE: %s\n' "$audit_file"
  nl -ba "$audit_file"
done
