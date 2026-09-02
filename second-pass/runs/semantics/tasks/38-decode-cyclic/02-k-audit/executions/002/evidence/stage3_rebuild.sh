#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/38-decode-cyclic
log=/audit-output/evidence/stage3_rebuild.log

run_step() {
  echo
  echo "\$ $*"
  "$@"
  local status=$?
  echo "EXIT_STATUS=$status"
  return "$status"
}

{
  cd "$scratch" || exit 1

  run_step python3 /audit-output/evidence/make_k_concrete_tests.py || exit 1
  run_step python3 py2mpy.py review_concrete_tests.py || exit 1
  python3 py2mpy.py review_concrete_tests.py >review_concrete_tests.mpy
  translate_status=$?
  echo '$ python3 py2mpy.py review_concrete_tests.py > review_concrete_tests.mpy'
  echo "EXIT_STATUS=$translate_status"
  (( translate_status == 0 )) || exit 1

  run_step kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled || exit 1

  run_step krun solution.regenerated.mpy \
    --definition runtime-kompiled || exit 1

  run_step krun review_concrete_tests.mpy \
    --definition runtime-kompiled || exit 1

  run_step kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-kompiled || exit 1

  run_step kprove spec-helper.k \
    --definition verification-kompiled \
    --spec-module SPEC-HELPER || exit 1

  run_step kprove spec-entry.k \
    --definition verification-kompiled \
    --spec-module SPEC-ENTRY || exit 1

  run_step kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC || exit 1
} >"$log" 2>&1
