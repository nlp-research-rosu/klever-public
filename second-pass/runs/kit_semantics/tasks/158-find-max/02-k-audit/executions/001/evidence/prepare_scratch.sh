#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruct-001
if [[ -e "$scratch" ]]; then
  printf 'Refusing to overwrite existing scratch path: %s\n' "$scratch" >&2
  exit 2
fi

printf '%s\n' \
  '$ mkdir -p /tmp/audit-work/reconstruct-001' \
  '$ cp -a /reference/reference-semantics /tmp/audit-work/reconstruct-001/reference-semantics' \
  '$ cp -a /reference/canonical.py /reference/prompt.py /reference/py2mpy.py /tmp/audit-work/reconstruct-001/' \
  '$ cp -a [candidate source artifacts] /tmp/audit-work/reconstruct-001/'

mkdir -p "$scratch"
cp -a /reference/reference-semantics "$scratch/reference-semantics"
cp -a \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  "$scratch/"
cp -a \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/connection.k \
  /candidate/connection-spec.k \
  /candidate/prove.sh \
  "$scratch/"

find "$scratch" -maxdepth 3 -printf '%y %P -> %l\n' | sort
