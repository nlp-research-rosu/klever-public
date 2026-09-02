#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf '[exit %d]\n' "$status"
  return "$status"
}

set -e
source_dir=/tmp/audit-work/review-138/candidate-src
build_dir=/tmp/audit-work/review-138/build
mkdir -p "$build_dir"

run test ! -e "$build_dir/semantic-kompiled"
run test ! -e "$build_dir/verification-kompiled"

run kompile "$source_dir/semantic.k" \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/semantic-kompiled"

run kompile "$source_dir/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_dir/verification-kompiled"

run python3 /audit-output/evidence/compare_krun.py

run kprove "$source_dir/spec.k" \
  --definition "$build_dir/verification-kompiled" \
  --spec-module SPEC

for claim in \
  entry-general necessity-four-summands sufficiency-witnesses \
  example-4 example-6 example-8
do
  run kprove "$source_dir/spec-labeled.k" \
    --definition "$build_dir/verification-kompiled" \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.$claim"
done
