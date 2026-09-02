#!/usr/bin/env bash
set -euo pipefail

# Recreate the pure AST-constructor translation checked by the semantics.
python3 py2mpy.py solution.py > solution.mpy

# kprove requires the Haskell backend.
kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX

# Concrete executions: the empty-list example, the nonempty prompt example,
# and an edge case containing empty strings.
krun solution.mpy -cARG='lVal(.StrList)'
krun solution.mpy -cARG='lVal("a" :: "b" :: "c" :: .StrList)'
krun solution.mpy -cARG='lVal("" :: "hello" :: "" :: " world" :: .StrList)'

# Modular proof.  First discharge the induction invariant itself.  Then prove
# the exact translated program, supplying that proved invariant as a trusted
# circularity.  Each positive target command must print #Top and exit zero.
kprove spec.k \
  --definition semantic-kompiled \
  --claims SPEC.concatenate-loop
kprove spec.k \
  --definition semantic-kompiled \
  --trusted SPEC.concatenate-loop
