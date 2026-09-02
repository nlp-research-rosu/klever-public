#!/usr/bin/env bash
set -euo pipefail
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

scratch=/tmp/audit-work/130-tri
test ! -e "$scratch"
mkdir -p "$scratch/candidate" "$scratch/reference" "$scratch/build"

cp -a \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  "$scratch/candidate/"

cp -a \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py \
  "$scratch/reference/"

find "$scratch" -maxdepth 3 -printf '%y %p -> %l\n' | sort
