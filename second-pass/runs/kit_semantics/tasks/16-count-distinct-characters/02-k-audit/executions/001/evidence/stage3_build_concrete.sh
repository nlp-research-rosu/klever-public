#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage3-build-concrete.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

python3 py2mpy.py audit_concrete.py > audit_concrete.mpy
translate_status=$?
printf 'audit_concrete_translation_exit=%d\n' "$translate_status"

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
build_status=$?
printf 'fresh_llvm_kompile_exit=%d\n' "$build_status"

if [[ "$translate_status" -ne 0 ]] || [[ "$build_status" -ne 0 ]]; then
  exit 1
fi
