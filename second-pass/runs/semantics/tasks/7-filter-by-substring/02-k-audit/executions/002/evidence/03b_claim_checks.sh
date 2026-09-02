#!/usr/bin/env bash
set -u

work=/tmp/audit-work/7-filter-by-substring/candidate
out=/audit-output/evidence
failed=0

run_logged() {
  name=$1
  shift
  log="$out/03_${name}.log"
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
  sed -n '1,200p' "$log"
  if (( lines > 280 )); then
    printf '[... bounded log: middle omitted ...]\n'
    tail -n 80 "$log"
  fi
  if (( status != 0 )); then
    failed=1
  fi
}

run_logged entry_with_proved_loop kprove spec-entry-with-proved-loop.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC-ENTRY-WITH-PROVED-LOOP \
  --output pretty
run_logged all_claims kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC \
  --output pretty

exit "$failed"
