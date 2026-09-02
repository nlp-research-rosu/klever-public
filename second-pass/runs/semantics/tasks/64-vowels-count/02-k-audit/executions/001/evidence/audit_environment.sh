#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
}

run kompile --version
run kprove --version
run python3 --version
run sha256sum \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
