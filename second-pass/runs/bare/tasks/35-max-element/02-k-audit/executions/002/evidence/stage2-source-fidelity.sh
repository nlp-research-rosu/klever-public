#!/usr/bin/env bash
set -euo pipefail
set -x

mkdir -p /tmp/audit-work/35-max-element
cp /candidate/solution.py /tmp/audit-work/35-max-element/solution.py
cp /candidate/solution.mpy /tmp/audit-work/35-max-element/solution.mpy
cp /candidate/semantic.k /tmp/audit-work/35-max-element/semantic.k
cp /candidate/verification.k /tmp/audit-work/35-max-element/verification.k
cp /candidate/spec.k /tmp/audit-work/35-max-element/spec.k
cp /candidate/prove.sh /tmp/audit-work/35-max-element/prove.sh
cp /reference/prompt.py /tmp/audit-work/35-max-element/trusted-prompt.py
cp /reference/canonical.py /tmp/audit-work/35-max-element/trusted-canonical.py
cp /reference/py2mpy.py /tmp/audit-work/35-max-element/trusted-py2mpy.py

python3 /reference/py2mpy.py \
  /tmp/audit-work/35-max-element/solution.py \
  > /tmp/audit-work/35-max-element/regenerated-solution.mpy
cmp /tmp/audit-work/35-max-element/solution.mpy \
  /tmp/audit-work/35-max-element/regenerated-solution.mpy
sha256sum \
  /tmp/audit-work/35-max-element/solution.mpy \
  /tmp/audit-work/35-max-element/regenerated-solution.mpy
find /tmp/audit-work/35-max-element \
  -maxdepth 1 -type f -printf '%f %s bytes\n' \
  | sort
