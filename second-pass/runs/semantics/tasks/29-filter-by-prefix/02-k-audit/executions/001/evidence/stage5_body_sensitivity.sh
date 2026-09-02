#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/29-filter-by-prefix/candidate-src
evidence=/audit-output/evidence
status=0
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '%s\n' 'MUTATION: Return(Name("result")) -> Return(ListExpr(.Exprs)); witness INPUT=["a"], PREFIX="a" has intended ["a"] but mutated return [].'

for name in verification-body-mutation.k spec-body-mutation.k; do
  printf 'COMMAND: cp /audit-output/evidence/%s /tmp/audit-work/29-filter-by-prefix/candidate-src/%s\n' "$name" "$name"
  cp "$evidence/$name" "$scratch/$name"
  rc=$?
  printf 'EXIT: %d\n\n' "$rc"
  (( rc == 0 )) || status=1
done

cd "$scratch" || exit 1

printf '%s\n' 'COMMAND: kompile verification-body-mutation.k --backend haskell --main-module VERIFICATION-BODY-MUTATION --syntax-module VERIFICATION-BODY-MUTATION --output-definition verification-body-mutation-kompiled'
kompile verification-body-mutation.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module VERIFICATION-BODY-MUTATION \
  --output-definition verification-body-mutation-kompiled
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove spec-body-mutation.k --definition verification-body-mutation-kompiled --spec-module FILTER-BY-PREFIX-BODY-MUTATION-SPEC'
kprove spec-body-mutation.k \
  --definition verification-body-mutation-kompiled \
  --spec-module FILTER-BY-PREFIX-BODY-MUTATION-SPEC
rc=$?
printf 'EXIT: %d\n' "$rc"
if (( rc == 0 )); then
  printf '%s\n' 'UNEXPECTED: wrong body proved the original result/heap obligation.'
  status=1
else
  printf '%s\n' 'EXPECTED: wrong body was rejected.'
fi
printf '\n'

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
