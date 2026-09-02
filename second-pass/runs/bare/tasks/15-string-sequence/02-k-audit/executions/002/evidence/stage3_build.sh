#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
printf 'COMMAND: bash /audit-output/evidence/stage3_build.sh\n'
printf 'WORKDIR: %s\n' "$scratch"
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '\nToolchain\n'
command -v kompile
command -v krun
command -v kprove
kompile --version
krun --version
kprove --version

printf '\nPre-build compiled-definition check\n'
find "$scratch" -maxdepth 1 -type d -name '*-kompiled' -printf '%f\n' \
  | LC_ALL=C sort

printf '\nConcrete semantics build\n'
printf '%s\n' \
  'COMMAND: kompile --backend llvm semantic.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled'
(
  cd "$scratch" || exit 1
  kompile --backend llvm semantic.k \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition semantic-llvm-kompiled
)
llvm_status=$?
printf 'llvm_kompile_exit=%s\n' "$llvm_status"

printf '\nProof semantics build\n'
printf '%s\n' \
  'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-haskell-kompiled'
(
  cd "$scratch" || exit 1
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-haskell-kompiled
)
haskell_status=$?
printf 'haskell_kompile_exit=%s\n' "$haskell_status"

printf '\nPost-build definitions\n'
find "$scratch" -maxdepth 1 -type d -name '*-kompiled' -printf '%f\n' \
  | LC_ALL=C sort

final_status=0
if [[ "$llvm_status" != 0 || "$haskell_status" != 0 ]]; then
  final_status=1
fi
printf 'SCRIPT_EXIT=%s\n' "$final_status"
exit "$final_status"
