#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/source
definition=/tmp/audit-work/reconstruction/semantics-haskell-kompiled

run_cmd() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return "$rc"
}

if [[ "$definition" != /tmp/audit-work/reconstruction/semantics-haskell-kompiled ]]; then
  exit 97
fi
run_cmd rm -rf "$definition" || exit $?
run_cmd kompile \
  --backend haskell \
  "$source_dir/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition" \
  -I "$source_dir" || exit $?
printf 'CONCRETE_HASKELL_REBUILD_COMPLETE\n'
