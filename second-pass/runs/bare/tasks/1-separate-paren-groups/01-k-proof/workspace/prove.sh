#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the semantics together with its mathematical verification functions.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise the translated program on the prompt example and boundary cases.
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("( ) (( )) (( )( ))")' --output pretty \
  | tee krun-prompt.out
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("")' --output pretty \
  | tee krun-empty.out
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("(((())))")' --output pretty \
  | tee krun-nested.out
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("()(())(()())")' --output pretty \
  | tee krun-adjacent.out

grep -Fq 'OutList ( .Outputs )' krun-empty.out
grep -Fq 'OutList ( out ( LP  LP  LP  LP  RP  RP  RP  RP  .Chars )  .Outputs )' krun-nested.out
expected_three='OutList ( out ( LP  RP  .Chars )  out ( LP  LP  RP  RP  .Chars )  out ( LP  LP  RP  LP  RP  RP  .Chars )  .Outputs )'
grep -Fq "$expected_three" krun-prompt.out
grep -Fq "$expected_three" krun-adjacent.out

# Prove every claim in spec.k. The extra check makes #Top part of the script's
# success condition as well as relying on kprove's zero exit status.
kprove spec.k --definition verification-kompiled --output pretty \
  | tee kprove.out
grep -qx '#Top' kprove.out
