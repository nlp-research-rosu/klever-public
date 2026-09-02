#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/38-decode-cyclic
log=/audit-output/evidence/stage4_pinning.log

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

  run_step python3 /audit-output/evidence/extract_decode_body.py || exit 1

  run_step kast decode-body-from-regeneration.mpy \
    --definition verification-kompiled \
    --module VERIFICATION \
    --sort Stmts \
    --expand-macros \
    --output kore \
    --output-file decode-body-from-regeneration.kore || exit 1

  run_step kast decode-body-macro.mpy \
    --definition verification-kompiled \
    --module VERIFICATION \
    --sort Stmts \
    --expand-macros \
    --output kore \
    --output-file decode-body-macro.kore || exit 1

  run_step cmp decode-body-from-regeneration.kore decode-body-macro.kore || exit 1
  run_step sha256sum decode-body-from-regeneration.kore decode-body-macro.kore || exit 1

  run_step kprove spec-ground.k \
    --definition verification-kompiled \
    --spec-module SPEC-GROUND || exit 1
} >"$log" 2>&1
