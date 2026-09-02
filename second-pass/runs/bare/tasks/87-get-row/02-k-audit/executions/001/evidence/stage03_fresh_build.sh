#!/usr/bin/env bash
set -u

status=0
scratch=/tmp/audit-work/87-get-row

printf '%s\n' '$ kompile semantic.k --backend llvm (fresh output directory)'
kompile "$scratch/source/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$scratch/semantic-audit-kompiled"
rc=$?
printf 'semantic_llvm_build_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ kompile verification.k --backend haskell (fresh output directory)'
kompile "$scratch/source/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$scratch/verification-audit-kompiled"
rc=$?
printf 'verification_haskell_build_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ read fresh backend markers'
for path in \
  "$scratch/semantic-audit-kompiled/backend.txt" \
  "$scratch/verification-audit-kompiled/backend.txt"
do
  printf '%s: ' "$path"
  sed -n '1p' "$path"
  rc=$?
  printf 'read_exit=%d\n' "$rc"
  (( rc == 0 )) || status=1
done

printf 'overall_exit=%d\n' "$status"
exit "$status"
