#!/usr/bin/env bash
set -u -o pipefail

SCRATCH=/tmp/audit-work/141-file-name-check
cd "$SCRATCH" || exit 1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf '$ diff -u semantic.k semantic-index-diagnostic.k\n'
diff -u semantic.k semantic-index-diagnostic.k
printf '[exit %d; expected diagnostic difference]\n' "$?"

run kompile \
  --backend llvm \
  semantic-index-diagnostic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-index-diagnostic-kompiled \
  --warnings none || exit $?

run krun \
  solution.mpy \
  --definition audit-index-diagnostic-kompiled \
  '-cINPUT=""'
