#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

echo '$ python3 /audit-output/evidence/07_generate_body_mutation.py'
python3 /audit-output/evidence/07_generate_body_mutation.py
echo "generate_body_mutation_exit=$?"

echo '$ kompile verification-body-mutation.k --backend haskell --main-module SPLIT-WORDS-BODY-MUTATION --syntax-module MPY-SYNTAX --output-definition audit-body-mutation-kompiled'
kompile verification-body-mutation.k \
  --backend haskell \
  --main-module SPLIT-WORDS-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-body-mutation-kompiled
echo "body_mutation_kompile_exit=$?"

echo '$ kprove spec-body-mutation.k --definition audit-body-mutation-kompiled --spec-module SPEC-BODY-MUTATION --claims SPEC-BODY-MUTATION.odd-lowercase-count'
kprove spec-body-mutation.k \
  --definition audit-body-mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.odd-lowercase-count
echo "body_mutation_kprove_exit=$?"
