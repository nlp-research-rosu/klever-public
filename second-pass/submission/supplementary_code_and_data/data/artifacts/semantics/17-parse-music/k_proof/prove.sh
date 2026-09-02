#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -c 'from solution import parse_music; assert parse_music("") == []; assert parse_music("o o| .| o| o| .| .| .| .| o o") == [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]; assert parse_music("  o\t.|\no|  ") == [4, 1, 2]'

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-test.mpy --definition runtime-kompiled

# Prove the inductive loop lemma without making the lemma available as a rule.
kompile verification.k \
  --backend haskell \
  --main-module PARSE-MUSIC-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module PARSE-MUSIC-LOOP-SPEC

# Recompile with the proved lemma, then prove the complete translated call.
kompile verification.k \
  --backend haskell \
  --main-module PARSE-MUSIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module PARSE-MUSIC-ENTRY-SPEC \
  --branching-allowed 100
