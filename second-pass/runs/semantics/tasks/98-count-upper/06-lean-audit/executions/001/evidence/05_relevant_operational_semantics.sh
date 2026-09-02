#!/usr/bin/env bash
set -euo pipefail

for file in \
  core.k \
  str.k \
  controls.k \
  iter.k \
  bool.k \
  int.k \
  operators.k
do
  nl -ba "/reference/k-proof/reference-semantics/semantics/${file}"
done
