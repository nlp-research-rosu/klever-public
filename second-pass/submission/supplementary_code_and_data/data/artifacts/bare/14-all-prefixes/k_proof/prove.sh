#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

# Recreate the translated program and bind that exact AST into the proof.
python3 py2mpy.py solution.py > solution.mpy
python3 embed_mpy.py > solution-program.k

# Check the executable Python and exercise the operational K semantics.
python3 -c 'from solution import all_prefixes; assert all_prefixes("") == []; assert all_prefixes("abc") == ["a", "ab", "abc"]'
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
krun solution.mpy --definition verification-kompiled
krun run-empty.mpy --definition verification-kompiled
krun run-abc.mpy --definition verification-kompiled

# Prove the loop invariant without a summary rule.
kprove loop-spec.k --definition verification-kompiled --spec-module LOOP-SPEC

# Compile the proven invariant as a verification lemma, then prove the target.
kompile verified-lemma.k --backend haskell --main-module VERIFIED-LEMMA --syntax-module MPY-SYNTAX
kprove spec.k --definition verified-lemma-kompiled --spec-module SPEC
