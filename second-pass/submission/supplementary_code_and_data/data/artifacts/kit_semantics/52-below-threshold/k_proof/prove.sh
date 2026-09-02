#!/usr/bin/env bash
set -euo pipefail

# Translation and independent executable checks.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py bridge-smoke.py > bridge-smoke.mpy
python3 differential.py

# Concrete execution under the supplied semantics.
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

# The value-summary connection uses only the fixed semantics and definitions.
kompile --backend haskell base-verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

# Prove the operational loop bridges without importing those bridges.
kompile --backend haskell verification-loops.k \
  --main-module VERIFICATION-LOOPS \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-verification-kompiled
kprove loop-spec.k \
  --definition loop-verification-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons

# Compose the already-proved loop claims to prove the source-For bridges.
kprove loop-spec.k \
  --definition loop-verification-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons,LOOP-SPEC.for-empty,LOOP-SPEC.for-cons \
  --trusted LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons

# Required full-domain entry-point proof.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Boundary comparison: fixed and bridge-enabled executions must agree on the
# entire final configuration. This suite avoids floats because the Haskell
# backend lacks a concrete FLOAT.sub hook; LLVM covers floats in smoke.mpy.
task_tmp_dir="$(mktemp -d)"
trap 'rm -rf "$task_tmp_dir"' EXIT
krun bridge-smoke.mpy \
  --definition runtime-kompiled \
  > "$task_tmp_dir/fixed.out"
krun bridge-smoke.mpy \
  --definition verification-kompiled \
  > "$task_tmp_dir/bridged.out"
diff -u "$task_tmp_dir/fixed.out" "$task_tmp_dir/bridged.out"

# Gate A negative probes. Both must exit non-zero.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?
set -e
if [[ "$vacuity_status" -eq 0 ]]; then
  echo "spec-vacuity.k unexpectedly proved"
  exit 1
fi
printf 'spec-vacuity.k expected failure: exit %s\n' "$vacuity_status"

set +e
kprove spec-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-MUTATION
mutation_status=$?
set -e
if [[ "$mutation_status" -eq 0 ]]; then
  echo "spec-mutation.k unexpectedly proved"
  exit 1
fi
printf 'spec-mutation.k expected failure: exit %s\n' "$mutation_status"
