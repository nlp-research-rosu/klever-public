#!/usr/bin/env bash
set -u
export PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return "$rc"
}

run command -v kup
printf '%s\n' 'NOTE: kup is absent; independently installed K tools are present, so the live path continues.'
run command -v kompile || exit $?
run command -v krun || exit $?
run command -v kprove || exit $?
run kompile --version || exit $?
run krun --version || exit $?
run kprove --version || exit $?
run test ! -e "$work/semantic-concrete-kompiled" || exit $?
run test ! -e "$work/verification-audit-kompiled" || exit $?
run kompile "$work/semantic.k" \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/semantic-concrete-kompiled" || exit $?
run kompile "$work/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/verification-audit-kompiled" || exit $?
printf '%s\n' 'CLEAN_BUILD_PASS'
