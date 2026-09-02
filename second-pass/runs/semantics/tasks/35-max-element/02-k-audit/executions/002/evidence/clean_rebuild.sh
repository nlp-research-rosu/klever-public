#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/work || exit 2

printf 'K tool versions\n'
run kompile --version
run krun --version
run kprove --version

printf '\nFresh definitions absent before build:\n'
run test ! -e runtime-kompiled
run test ! -e verification-kompiled

printf '\nGenerate independent concrete program:\n'
python3 py2mpy.py audit-concrete.py > audit-concrete.mpy
printf '[translator exit %d]\n' "$?"
run sha256sum audit-concrete.py audit-concrete.mpy

printf '\nBuild and execute supplied semantics from copied source:\n'
run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
run krun audit-concrete.mpy --definition runtime-kompiled

printf '\nBuild proof definition from copied source:\n'
run kompile verification.k \
  --backend haskell \
  --main-module MAX-ELEMENT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

printf '\nOriginal submitted spec: all four claims in one independent run:\n'
run kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC

printf '\nMechanically labeled copy: all four exact claims:\n'
run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED

printf '\nLabeled fold claim alone:\n'
run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims fold

printf '\nLabeled example one alone:\n'
run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims example-one

printf '\nLabeled example two alone:\n'
run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims example-two

printf '\nUniversal plus its inductive fold helper:\n'
run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC-LABELED \
  --claims fold,universal
