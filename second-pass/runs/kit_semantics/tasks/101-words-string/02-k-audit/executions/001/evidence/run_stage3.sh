#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
cd "$scratch" || exit 99

echo 'COMMAND: python3 py2mpy.py smoke.py > regenerated-smoke.mpy'
python3 py2mpy.py smoke.py > regenerated-smoke.mpy
translate_status=$?
echo "EXIT_STATUS: $translate_status"

echo 'COMMAND: cmp -s smoke.mpy regenerated-smoke.mpy'
cmp -s smoke.mpy regenerated-smoke.mpy
smoke_identity_status=$?
echo "EXIT_STATUS: $smoke_identity_status"
if [[ $smoke_identity_status -eq 0 ]]; then
  echo 'SMOKE_TRANSLATION_BYTE_IDENTITY: YES'
else
  echo 'SMOKE_TRANSLATION_BYTE_IDENTITY: NO'
fi

echo 'COMMAND: kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-fresh-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled
llvm_build_status=$?
echo "EXIT_STATUS: $llvm_build_status"

echo 'COMMAND: krun regenerated-smoke.mpy --definition runtime-fresh-kompiled'
krun regenerated-smoke.mpy --definition runtime-fresh-kompiled
smoke_run_status=$?
echo "EXIT_STATUS: $smoke_run_status"

echo 'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-fresh-kompiled'
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
proof_build_status=$?
echo "EXIT_STATUS: $proof_build_status"

echo 'COMMAND: kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC'
kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC
positive_status=$?
echo "EXIT_STATUS: $positive_status"

if [[ $translate_status -ne 0 ||
      $smoke_identity_status -ne 0 ||
      $llvm_build_status -ne 0 ||
      $smoke_run_status -ne 0 ||
      $proof_build_status -ne 0 ||
      $positive_status -ne 0 ]]; then
  exit 1
fi
