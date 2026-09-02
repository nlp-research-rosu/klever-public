#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/fresh

run_command() {
  local label="$1"
  shift
  printf 'COMMAND [%s]:' "$label"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT [%s]: %s\n' "$label" "$status"
  return "$status"
}

run_command "kompile-version" kompile --version || exit $?
run_command "kprove-version" kprove --version || exit $?
run_command "krun-version" krun --version || exit $?

python3 /reference/py2mpy.py \
  /audit-output/evidence/audit_smoke.py > audit-smoke.mpy
translate_status=$?
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi
# The translation command's normal output is the program; record its status
# explicitly because stdout was intentionally captured as the test input.
printf '%s\n' \
  'COMMAND [translate-audit-smoke]: python3 /reference/py2mpy.py /audit-output/evidence/audit_smoke.py > /tmp/audit-work/fresh/audit-smoke.mpy'
printf 'EXIT [translate-audit-smoke]: %s\n' "$translate_status"

run_command \
  "kompile-concrete" \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled || exit $?

run_command \
  "krun-audit-smoke" \
  krun audit-smoke.mpy \
    --definition audit-runtime-kompiled || exit $?

run_command \
  "kompile-proof" \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION-SYNTAX \
    --output-definition audit-verification-kompiled || exit $?

run_command \
  "kprove-add-loop" \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.add-loop || exit $?

run_command \
  "kprove-add-entry" \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.add-entry || exit $?
