#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/fruit67/candidate
cd "$work" || exit 99

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

echo "COMMAND: krun solution.mpy --definition audit-verification-haskell-kompiled --depth 0 --output kast > audit-source.kast 2> audit-source.err"
krun solution.mpy \
  --definition audit-verification-haskell-kompiled \
  --depth 0 \
  --output kast > audit-source.kast 2> audit-source.err
source_status=$?
printf 'SOURCE_KAST_COMMAND_EXIT_STATUS=%s\n' "$source_status"

echo "COMMAND: krun solution-alias.mpy --definition audit-verification-haskell-kompiled --depth 0 --output kast > audit-alias.kast 2> audit-alias.err"
krun solution-alias.mpy \
  --definition audit-verification-haskell-kompiled \
  --depth 0 \
  --output kast > audit-alias.kast 2> audit-alias.err
alias_status=$?
printf 'ALIAS_KAST_COMMAND_EXIT_STATUS=%s\n' "$alias_status"

run cmp -s audit-source.kast audit-alias.kast
cmp_status=$?
sha256sum audit-source.kast audit-alias.kast
printf 'CONSTRUCTOR_IDENTITY=%s\n' "$(
  if [[ "$cmp_status" -eq 0 ]]; then printf true; else printf false; fi
)"

run kompile verification-body-mut.k \
  --main-module VERIFICATION-BODY-MUT \
  --syntax-module VERIFICATION-BODY-MUT \
  --backend haskell \
  --output-definition audit-body-mut-kompiled
build_status=$?

run kprove spec-body-mut.k \
  --definition audit-body-mut-kompiled \
  --spec-module SPEC-BODY-MUT
proof_status=$?

printf 'EXPECTED_BODY_MUTATION_PROOF_FAILURE=%s\n' "$(
  if [[ "$build_status" -eq 0 && "$proof_status" -ne 0 ]]; then
    printf true
  else
    printf false
  fi
)"

[[ "$source_status" -eq 0 && "$alias_status" -eq 0 && "$cmp_status" -eq 0 ]]
identity_status=$?
[[ "$build_status" -eq 0 && "$proof_status" -ne 0 ]]
mutation_status=$?
[[ "$identity_status" -eq 0 && "$mutation_status" -eq 0 ]]
