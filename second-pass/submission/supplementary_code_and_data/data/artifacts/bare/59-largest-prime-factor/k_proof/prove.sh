#!/usr/bin/env bash
set -euo pipefail
set -x

proof_build_dir="$(mktemp -d "$PWD/.kproof.XXXXXX")"
trap 'rm -rf -- "$proof_build_dir"' EXIT

# Recreate the submitted constructor term and require it to be current.
python3 py2mpy.py solution.py > "$proof_build_dir/solution.mpy"
cmp solution.mpy "$proof_build_dir/solution.mpy"

# verification.k imports semantic.k, so this compiles both the interpreter and
# the pure reference model into the definition used by krun and kprove.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_build_dir/verification-kompiled"

# Exercise the actual generated program through the custom semantics.
krun solution.mpy --definition "$proof_build_dir/verification-kompiled" \
  -cN=13195 --output pretty | tee "$proof_build_dir/run-13195.out"
grep -F 'result ( 29 )' "$proof_build_dir/run-13195.out"

krun solution.mpy --definition "$proof_build_dir/verification-kompiled" \
  -cN=2048 --output pretty | tee "$proof_build_dir/run-2048.out"
grep -F 'result ( 2 )' "$proof_build_dir/run-2048.out"

# Prove the loop refinement, universal end-to-end result, and both examples.
kprove spec.k \
  --definition "$proof_build_dir/verification-kompiled" \
  --spec-module SPEC \
  --output pretty
