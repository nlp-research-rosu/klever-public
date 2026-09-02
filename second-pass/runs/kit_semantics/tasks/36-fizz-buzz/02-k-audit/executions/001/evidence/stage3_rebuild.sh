#!/usr/bin/env bash
set +e

run() {
  printf 'COMMAND: %s\n' "$*"
  "$@"
  local status=$?
  printf 'EXIT STATUS: %s\n' "$status"
  return "$status"
}

run kompile --version || exit $?
run kprove --version || exit $?

printf 'COMMAND: python3 trusted/py2mpy.py audit-concrete-tests.py > audit-concrete-tests.mpy\n'
python3 trusted/py2mpy.py audit-concrete-tests.py > audit-concrete-tests.mpy
status=$?
printf 'EXIT STATUS: %s\n' "$status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

run kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled || exit $?

run krun audit-concrete-tests.mpy \
  --definition audit-runtime-kompiled || exit $?

run kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled || exit $?

run kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC || exit $?

run kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop || exit $?

run kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop || exit $?

run kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.fizz-buzz || exit $?
