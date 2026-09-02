#!/usr/bin/env bash
set -u

work=/tmp/audit-work/7-filter-by-substring/candidate
out=/audit-output/evidence
failed=0

run_logged() {
  name=$1
  shift
  log="$out/04_${name}.log"
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

run_logged kast_solution kast \
  --definition audit-verification-kompiled \
  --module FILTER-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file solution.expanded.kore \
  solution.mpy
run_logged kast_macro kast \
  --definition audit-verification-kompiled \
  --module FILTER-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file filterProgram.expanded.kore \
  --expression filterProgram
run_logged constructor_cmp cmp solution.expanded.kore filterProgram.expanded.kore
run_logged constructor_hash sha256sum solution.expanded.kore filterProgram.expanded.kore
run_logged ground_python python3 /audit-output/evidence/04_ground_compare.py
run_logged ground_kprove kprove spec-ground.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC-GROUND \
  --output pretty

exit "$failed"
