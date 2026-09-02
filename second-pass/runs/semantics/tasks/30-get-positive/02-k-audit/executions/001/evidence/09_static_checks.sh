#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
}

run kompile --version
run kprove --version
run krun --version

run sha256sum \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /tmp/audit-work/30-get-positive/solution.py \
  /tmp/audit-work/30-get-positive/solution.mpy \
  /tmp/audit-work/30-get-positive/spec.k \
  /tmp/audit-work/30-get-positive/verification.k

run rg -n \
  '^\s*(syntax|rule|claim)\b|\[(?:[^\]]*\b(?:function|total|functional|macro|simplification|priority|concrete|owise)\b[^\]]*)\]' \
  /candidate/verification.k /candidate/spec.k

run rg -n 'syntax .*\bsymbol\(' \
  /reference/reference-semantics

