#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 99

printf 'Witness: N=2. Mutated body computes 2*(2+2)//2=4; required triangular(2)=3.\n\n'

printf '$ kompile verification-body-mutation.k --backend haskell --main-module SUM-TO-N-BODY-MUTATION --syntax-module MPY-SYNTAX --output-definition body-mutation-kompiled\n'
kompile verification-body-mutation.k \
  --backend haskell \
  --main-module SUM-TO-N-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled
rc=$?
printf '[exit %d]\n\n' "$rc"

printf '$ kprove spec-body-mutation.k --definition body-mutation-kompiled --spec-module SUM-TO-N-BODY-MUTATION-SPEC\n'
kprove spec-body-mutation.k \
  --definition body-mutation-kompiled \
  --spec-module SUM-TO-N-BODY-MUTATION-SPEC
rc=$?
printf '[exit %d]\n' "$rc"
