#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the implementation and generate the exact K program constant used
# by the proof definition.
python3 py2mpy.py solution.py > solution.mpy
python3 make_solution_k.py > solution-program.k

# Concrete execution uses the actual translated Module term.
kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled \
  -w none

python3 make_run.py \
  'Call(Name("sorted_list_sum"), ListExpr(Str("aa"), Str("a"), Str("aaa")))' \
  > example-1.run
krun example-1.run --definition semantic-kompiled | tee krun-example-1.out
grep -Fq 'VList ( "aa" , .Words )' krun-example-1.out

python3 make_run.py \
  'Call(Name("sorted_list_sum"), ListExpr(Str("zy"), Str("ab"), Str("x"), Str("aa"), Str("abcd"), Str("ba"), Str("ab")))' \
  > example-2.run
krun example-2.run --definition semantic-kompiled | tee krun-example-2.out
grep -Fq 'VList ( "aa" , "ab" , "ab" , "ba" , "zy" , "abcd" , .Words )' krun-example-2.out

# Compile the semantics plus the independent contract functions for symbolic
# execution, then prove every claim in spec.k in one positive target command.
kompile verification.k \
  --main-module SORTED-LIST-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled \
  -w none

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty \
  -w none | tee kprove.out
grep -Fxq '#Top' kprove.out
