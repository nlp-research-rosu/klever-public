#!/usr/bin/env bash
set -uo pipefail

mutation_dir=/tmp/audit-work/body-mutation
mkdir -p "$mutation_dir"
cp \
  /tmp/audit-work/proof/semantic.k \
  /tmp/audit-work/proof/verification.k \
  /tmp/audit-work/proof/spec.k \
  "$mutation_dir/"

printf 'COMMAND: patch -d %s -p0 < /audit-output/evidence/body-sensitivity.patch\n' \
  "$mutation_dir"
patch -d "$mutation_dir" -p0 < /audit-output/evidence/body-sensitivity.patch
patch_exit=$?
printf 'body mutation patch exit=%s\n' "$patch_exit"
if (( patch_exit != 0 )); then
  exit 1
fi

cd "$mutation_dir" || exit 90
printf 'MUTATION: targetLoopBody open branch changes depth + 1 to depth - 1\n'
sed -n '75,84p' semantic.k

printf 'COMMAND: kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition body-haskell-kompiled\n'
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition body-haskell-kompiled
build_exit=$?
printf 'body mutation kompile exit=%s\n' "$build_exit"
if (( build_exit != 0 )); then
  exit 1
fi

printf 'COMMAND: kprove spec.k --definition body-haskell-kompiled --spec-module SPEC\n'
kprove spec.k \
  --definition body-haskell-kompiled \
  --spec-module SPEC
proof_exit=$?
printf 'body-mutated original proof exit=%s (nonzero expected)\n' "$proof_exit"
if (( proof_exit == 0 )); then
  exit 1
fi
