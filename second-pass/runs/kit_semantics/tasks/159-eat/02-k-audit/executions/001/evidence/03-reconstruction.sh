#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/159-eat

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
runtime_build_status=$?
echo "runtime_kompile_exit=${runtime_build_status}"

python3 /reference/py2mpy.py \
  /audit-output/evidence/03-concrete-tests.py > fresh-concrete-tests.mpy
concrete_translation_status=$?
echo "concrete_translation_exit=${concrete_translation_status}"

krun fresh-concrete-tests.mpy --definition fresh-runtime-kompiled
concrete_run_status=$?
echo "concrete_krun_exit=${concrete_run_status}"

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
proof_build_status=$?
echo "proof_kompile_exit=${proof_build_status}"

kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
combined_status=$?
echo "combined_kprove_exit=${combined_status}"

kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.eat-enough
enough_status=$?
echo "eat_enough_kprove_exit=${enough_status}"

kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.eat-insufficient
insufficient_status=$?
echo "eat_insufficient_kprove_exit=${insufficient_status}"

if (( runtime_build_status != 0 || concrete_translation_status != 0 ||
      concrete_run_status != 0 || proof_build_status != 0 ||
      combined_status != 0 || enough_status != 0 ||
      insufficient_status != 0 )); then
  exit 1
fi
