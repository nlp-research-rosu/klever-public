#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n\n' "$status"
  return "$status"
}

cd /tmp/audit-work/109-move-one-ball/candidate || exit 90
export PATH="$HOME/.nix-profile/bin:$PATH"

run find . -maxdepth 1 -type d -name '*-kompiled' -print

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
concrete_status=$?

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
proof_status=$?

printf 'concrete_build_status=%d\n' "$concrete_status"
printf 'proof_build_status=%d\n' "$proof_status"
if (( concrete_status != 0 || proof_status != 0 )); then
  exit 1
fi
