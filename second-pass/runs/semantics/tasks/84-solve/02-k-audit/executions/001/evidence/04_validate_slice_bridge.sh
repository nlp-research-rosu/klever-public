#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"
base=/tmp/audit-work/base-semantics-kompiled
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    overall=1
  fi
}

run test ! -e "$base"
run kompile \
  /tmp/audit-work/candidate-src/reference-semantics/semantics.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$base"
run kprove /audit-output/evidence/04_slice_connection.k \
  --definition "$base" \
  --spec-module SLICE-CONNECTION \
  --output pretty

exit "$overall"
