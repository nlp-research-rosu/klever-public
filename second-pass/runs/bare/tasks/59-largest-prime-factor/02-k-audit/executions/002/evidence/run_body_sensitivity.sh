#!/usr/bin/env bash
set -u

work=/tmp/audit-work/59-largest-prime-factor
source_dir="$work/source"
build_dir="$work/build-body-mutated"
all_status=0

if [[ -e "$build_dir" ]]; then
  printf 'REFUSING NON-FRESH BUILD DIRECTORY: %s\n' "$build_dir"
  exit 2
fi
mkdir "$build_dir"

run_and_record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf 'EXIT: %d\n' "$command_status"
  return "$command_status"
}

run_and_record kompile "$source_dir/verification-body-mut.k" \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUT \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/verification-kompiled" \
  || all_status=1

run_and_record kast "$source_dir/solution-body-mut.mpy" \
  --definition "$build_dir/verification-kompiled" \
  --module VERIFICATION-BODY-MUT \
  --sort PyModule \
  --expand-macros \
  --output kore \
  --output-file "$work/body-mut-source.kore" \
  || all_status=1

run_and_record kast \
  --expression solutionModule \
  --definition "$build_dir/verification-kompiled" \
  --module VERIFICATION-BODY-MUT \
  --sort PyModule \
  --expand-macros \
  --output kore \
  --output-file "$work/body-mut-macro.kore" \
  || all_status=1

run_and_record cmp -s "$work/body-mut-source.kore" "$work/body-mut-macro.kore" \
  || all_status=1
sha256sum "$work/body-mut-source.kore" "$work/body-mut-macro.kore"

run_and_record krun "$source_dir/solution-body-mut.mpy" \
  --definition "$build_dir/verification-kompiled" \
  -cN=13195 \
  --output pretty \
  || all_status=1

printf '%s\n' 'EXPECTED FAILURE COMMAND FOLLOWS'
run_and_record kprove "$source_dir/spec-body-mut.k" \
  --definition "$build_dir/verification-kompiled" \
  --spec-module SPEC-BODY-MUT \
  --output pretty
proof_status=$?
if (( proof_status == 0 )); then
  printf '%s\n' 'UNEXPECTED: mutated body still proved result 29'
  all_status=1
else
  printf 'EXPECTED_NONZERO_CONFIRMED: %d\n' "$proof_status"
fi

exit "$all_status"
