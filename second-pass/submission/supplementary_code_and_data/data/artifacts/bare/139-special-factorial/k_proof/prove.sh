#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted AST term from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution of the prompt's example under the semantics.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-run-kompiled
krun solution.mpy \
  -cN=4 \
  --definition semantic-run-kompiled \
  --output pretty | tee krun-example.out
grep -Fq 'result ( 288 )' krun-example.out

# Compile the symbolic backend used by kprove.
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-proof-kompiled

# Ensure that the exact translated program and the term named in the proof are
# identical after K parsing and macro expansion.
cmp \
  <(kast solution.mpy -d semantic-proof-kompiled -m MPY -s Pgm \
      --expand-macros -o kore) \
  <(kast -e solutionProgram -d semantic-proof-kompiled -m MPY -s Pgm \
      --expand-macros -o kore)

# Prove the ordinary-factorial helper for every positive integer.
kprove spec.k \
  --definition semantic-proof-kompiled \
  --claims SPEC.factorial-call \
  --output pretty

# Reuse the separately proved helper lemma, and prove Brazilian factorial.
kprove spec.k \
  --definition semantic-proof-kompiled \
  --claims SPEC.factorial-call,SPEC.special-factorial-call \
  --trusted SPEC.factorial-call \
  --output pretty

# Reuse both proved call lemmas to prove the exact translated module end-to-end.
kprove spec.k \
  --definition semantic-proof-kompiled \
  --claims SPEC.factorial-call,SPEC.special-factorial-call,SPEC.program-correct \
  --trusted SPEC.factorial-call,SPEC.special-factorial-call \
  --output pretty
