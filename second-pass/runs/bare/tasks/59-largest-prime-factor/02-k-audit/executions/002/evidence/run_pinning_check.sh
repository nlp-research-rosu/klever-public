#!/usr/bin/env bash
set -u

work=/tmp/audit-work/59-largest-prime-factor
definition="$work/build-stage3-fresh/verification-kompiled"
source_dir="$work/source"

run_and_record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf 'EXIT: %d\n' "$command_status"
  return "$command_status"
}

all_status=0

run_and_record kast "$source_dir/solution.mpy" \
  --definition "$definition" \
  --module VERIFICATION \
  --sort PyModule \
  --expand-macros \
  --output kore \
  --output-file "$work/solution-source.kore" \
  || all_status=1

run_and_record kast \
  --expression solutionModule \
  --definition "$definition" \
  --module VERIFICATION \
  --sort PyModule \
  --expand-macros \
  --output kore \
  --output-file "$work/solution-macro.kore" \
  || all_status=1

run_and_record cmp -s "$work/solution-source.kore" "$work/solution-macro.kore" \
  || all_status=1
sha256sum "$work/solution-source.kore" "$work/solution-macro.kore"
wc -c "$work/solution-source.kore" "$work/solution-macro.kore"

exit "$all_status"
