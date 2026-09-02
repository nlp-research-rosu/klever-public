#!/usr/bin/env bash
set -u

work=/tmp/audit-work/59-largest-prime-factor
source_dir="$work/source"
build_dir="$work/build-stage3-fresh"

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

all_status=0

run_and_record kompile "$source_dir/semantic.k" \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/semantic-kompiled" \
  || all_status=1

for input_value in 4 6 9 15 2048 13195; do
  run_and_record krun "$source_dir/solution.mpy" \
    --definition "$build_dir/semantic-kompiled" \
    -cN="$input_value" \
    --output pretty \
    || all_status=1
done

run_and_record kompile "$source_dir/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/verification-kompiled" \
  || all_status=1

for claim_label in \
  SPEC.loop-refines-lpf \
  SPEC.largest-prime-factor-correct \
  SPEC.prompt-example-13195 \
  SPEC.prompt-example-2048
do
  run_and_record kprove "$source_dir/spec.k" \
    --definition "$build_dir/verification-kompiled" \
    --spec-module SPEC \
    --claims "$claim_label" \
    --output pretty \
    || all_status=1
done

exit "$all_status"
