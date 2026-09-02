#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

echo '$ python3 /audit-output/evidence/06_generate_no_bridges.py'
python3 /audit-output/evidence/06_generate_no_bridges.py
echo "generate_no_bridges_exit=$?"

echo '$ kompile verification-no-bridges.k --backend haskell --main-module SPLIT-WORDS-NO-BRIDGES --syntax-module MPY-SYNTAX --output-definition audit-no-bridges-kompiled'
kompile verification-no-bridges.k \
  --backend haskell \
  --main-module SPLIT-WORDS-NO-BRIDGES \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-no-bridges-kompiled
echo "no_bridges_kompile_exit=$?"

for label in whitespace comma odd-lowercase-count; do
  echo "$ timeout 90s kprove spec-no-bridges.k --definition audit-no-bridges-kompiled --spec-module SPEC-NO-BRIDGES --claims SPEC-NO-BRIDGES.$label"
  timeout 90s kprove spec-no-bridges.k \
    --definition audit-no-bridges-kompiled \
    --spec-module SPEC-NO-BRIDGES \
    --claims "SPEC-NO-BRIDGES.$label"
  echo "${label}_no_bridges_kprove_exit=$?"
done
