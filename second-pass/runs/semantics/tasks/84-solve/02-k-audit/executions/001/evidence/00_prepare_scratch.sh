#!/usr/bin/env bash
set -euo pipefail

printf '$ mkdir -p /tmp/audit-work/candidate-src\n'
mkdir -p /tmp/audit-work/candidate-src

for artifact in \
  prompt.py \
  py2mpy.py \
  solution.py \
  solution.mpy \
  spec.k \
  verification.k \
  prove.sh \
  concrete-tests.py \
  concrete-tests.mpy
do
  printf '$ cp -a /candidate/%s /tmp/audit-work/candidate-src/%s\n' \
    "$artifact" "$artifact"
  cp -a "/candidate/$artifact" "/tmp/audit-work/candidate-src/$artifact"
done

printf '$ cp -a /candidate/reference-semantics /tmp/audit-work/candidate-src/reference-semantics\n'
cp -a \
  /candidate/reference-semantics \
  /tmp/audit-work/candidate-src/reference-semantics

printf '$ cp -a /reference/canonical.py /tmp/audit-work/canonical.py\n'
cp -a /reference/canonical.py /tmp/audit-work/canonical.py
