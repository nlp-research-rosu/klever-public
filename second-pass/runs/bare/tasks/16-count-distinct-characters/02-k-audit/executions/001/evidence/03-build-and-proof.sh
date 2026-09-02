#!/usr/bin/env bash
set +e
cd /tmp/audit-work/build || exit 90

run() {
  echo "$ $*"
  "$@"
  status=$?
  echo "exit=$status"
  return "$status"
}

run kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantics-kompiled
llvm_build=$?

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
haskell_build=$?

run kprove spec-universal.k \
  --definition verification-kompiled \
  --spec-module SPEC-UNIVERSAL
universal=$?

run kprove spec-xyz.k \
  --definition verification-kompiled \
  --spec-module SPEC-XYZ
xyz=$?

run kprove spec-jerry.k \
  --definition verification-kompiled \
  --spec-module SPEC-JERRY
jerry=$?

run kprove spec-empty.k \
  --definition verification-kompiled \
  --spec-module SPEC-EMPTY
empty=$?

echo "summary llvm_build=$llvm_build haskell_build=$haskell_build universal=$universal xyz=$xyz jerry=$jerry empty=$empty"
if (( llvm_build || haskell_build || universal || xyz || jerry || empty )); then
  exit 1
fi
