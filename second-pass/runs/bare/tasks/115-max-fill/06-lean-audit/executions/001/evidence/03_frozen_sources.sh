#!/usr/bin/env bash
set -u
for path in \
  /reference/k-proof/prompt.py \
  /reference/k-proof/solution.py \
  /reference/k-proof/solution.mpy \
  /reference/k-proof/solution-program.k \
  /reference/k-proof/semantic.k \
  /reference/k-proof/verification.k \
  /reference/k-proof/spec.k \
  /reference/lemma-discovery.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-generation/generated/Klean115MaxFill.lean \
  /reference/klean-generation/generated/Klean115MaxFill/Lemmas.lean \
  /reference/klean-generation/generated/Klean115MaxFill/Func.lean \
  /reference/klean-generation/trust-inventory.json \
  /reference/klean-generation/preflight.json \
  /reference/klean-toolchain.lock.json
do
  echo "$ nl -ba $path"
  nl -ba "$path"
done
