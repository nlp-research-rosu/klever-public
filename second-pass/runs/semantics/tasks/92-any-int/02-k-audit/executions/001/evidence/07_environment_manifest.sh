#!/usr/bin/env bash
set -u

echo '$ date --iso-8601=seconds'
date --iso-8601=seconds
echo "exit=$?"

echo '$ command -v kompile kprove krun'
command -v kompile
command -v kprove
command -v krun
echo "exit=$?"

echo '$ kompile --version'
kompile --version
echo "exit=$?"
echo '$ kprove --version'
kprove --version
echo "exit=$?"

echo '$ sha256sum candidate proof/program sources and trusted inputs'
sha256sum \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
echo "exit=$?"

echo '$ sha256sum every candidate supplied-semantics source'
find /candidate/reference-semantics -type f -name '*.k' -print0 |
  sort -z |
  xargs -0 sha256sum
echo "exit=$?"

echo '$ candidate spec-vacuity and proof-report presence'
for name in spec-vacuity.k PROOF.md
do
  if test -e "/candidate/$name" || test -L "/candidate/$name"; then
    echo "PRESENT /candidate/$name"
  else
    echo "ABSENT /candidate/$name"
  fi
done

echo '$ evidence file manifest'
find /audit-output/evidence -maxdepth 2 -type f -printf '%P\t%s bytes\n' | sort
echo "exit=$?"
