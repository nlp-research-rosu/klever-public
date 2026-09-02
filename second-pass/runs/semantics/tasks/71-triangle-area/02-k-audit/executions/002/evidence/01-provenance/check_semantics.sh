#!/usr/bin/env bash
set -euo pipefail
set -x

cmp -s /candidate/prompt.py /reference/prompt.py
cmp -s /candidate/py2mpy.py /reference/py2mpy.py

diff -r --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics

diff -u \
  <(cd /reference/reference-semantics && find . -printf '%P\t%y\t%l\n' | sort) \
  <(cd /candidate/reference-semantics && find . -printf '%P\t%y\t%l\n' | sort)

echo "Trusted semantics regular-file manifest:"
find /reference/reference-semantics -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum

echo "Candidate semantics regular-file manifest:"
find /candidate/reference-semantics -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum

echo "SEMANTICS_TREE_IDENTITY_OK"
