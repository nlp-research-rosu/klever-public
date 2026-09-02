#!/usr/bin/env bash
set -u

work=/tmp/audit-work/7-filter-by-substring/bridgefree
out=/audit-output/evidence
failed=0

run_logged() {
  name=$1
  shift
  log="$out/05_${name}.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  (
    cd "$work" || exit 125
    "$@"
  ) >"$log" 2>&1
  status=$?
  printf 'EXIT: %d\n' "$status"
  lines=$(wc -l <"$log")
  printf 'LOG: %s (%d lines)\n' "$log" "$lines"
  sed -n '1,180p' "$log"
  if (( lines > 240 )); then
    printf '[... bounded log: middle omitted ...]\n'
    tail -n 60 "$log"
  fi
  if (( status != 0 )); then
    failed=1
  fi
}

run_logged bridgefree_build kompile bridgefree.k \
  --backend haskell \
  --main-module BRIDGEFREE \
  --syntax-module BRIDGEFREE \
  --output-definition bridgefree-function-kompiled
run_logged bridgefree_proof kprove bridgefree-spec.k \
  --definition bridgefree-function-kompiled \
  --spec-module BRIDGEFREE-SPEC \
  --output pretty

exit "$failed"
