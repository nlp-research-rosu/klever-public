#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/source
build_dir=/tmp/audit-work/reconstruction

run_cmd() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return "$rc"
}

if [[ "$build_dir" != /tmp/audit-work/reconstruction ]]; then
  printf 'Refusing unexpected build directory: %s\n' "$build_dir"
  exit 97
fi

run_cmd rm -rf "$build_dir" || exit $?
run_cmd mkdir -p "$build_dir" || exit $?
run_cmd sha256sum \
  "$source_dir/semantic.k" \
  "$source_dir/verification.k" \
  "$source_dir/spec.k" \
  "$source_dir/solution.mpy" || exit $?
run_cmd kompile --version || exit $?

run_cmd kompile \
  --backend llvm \
  "$source_dir/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/semantics-kompiled" \
  -I "$source_dir" || exit $?

run_cmd kompile \
  --backend haskell \
  "$source_dir/verification.k" \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition "$build_dir/verification-kompiled" \
  -I "$source_dir" || exit $?

printf 'REBUILD_COMPLETE\n'
