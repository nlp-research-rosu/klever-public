#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/79-audit/source
mkdir -p "$scratch"

echo '$ cp -a selected candidate source artifacts to /tmp/audit-work/79-audit/source/'
cp -a \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  "$scratch"/

echo '$ cp -a trusted prompt, canonical, translator, and supplied semantics to scratch'
cp -a /reference/prompt.py /reference/canonical.py /reference/py2mpy.py "$scratch"/
cp -a /reference/reference-semantics "$scratch"/

echo '$ find /tmp/audit-work/79-audit/source -maxdepth 2 -printf ...'
find "$scratch" -maxdepth 2 -printf '%y %P -> %l\n' | sort

if find "$scratch" -maxdepth 1 -type d -name '*-kompiled' -print -quit | grep -q .; then
  echo 'ERROR: candidate-built definition copied into scratch' >&2
  exit 1
fi
echo 'SCRATCH_PREPARATION=PASS'
