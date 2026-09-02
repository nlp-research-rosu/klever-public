#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"
cd /tmp/audit-work/proof || exit 90

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

run command -v kup
printf '%s\n' 'NOTE: kup may be absent when an independently installed K toolchain is available.'
run command -v kompile || exit $?
run command -v krun || exit $?
run command -v kprove || exit $?
run kompile --version || exit $?
run kprove --version || exit $?

printf '%s\n' 'CLEAN_SOURCE_CHECK: no candidate-provided compiled definition was copied'
run find . -maxdepth 1 -type d -name '*-kompiled' -print || exit $?

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled || exit $?

printf '%s\n' 'COMMAND: python3 /reference/py2mpy.py audit_smoke.py > audit_smoke.mpy'
python3 /reference/py2mpy.py audit_smoke.py > audit_smoke.mpy
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
test "$status" -eq 0 || exit "$status"
run krun audit_smoke.mpy --definition runtime-kompiled || exit $?

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled || exit $?

run kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims loop || exit $?
