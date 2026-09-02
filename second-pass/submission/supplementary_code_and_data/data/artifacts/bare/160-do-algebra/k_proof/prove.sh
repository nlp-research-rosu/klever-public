#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor term from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# verification.k imports semantic.k, so this one definition supports both
# concrete execution and reachability proofs.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition .verification-kompiled

# Prompt example: 2 + 3 * 4 - 5 = 9.
krun solution.mpy --definition .verification-kompiled \
  -cOPS='ops(Op("+", Op("*", Op("-", .Ops))))' \
  -cOPERANDS='ints(Num(2, Num(3, Num(4, Num(5, .Ints)))))' \
  | tee /dev/stderr | rg -Fq 'answer ( 9 )'

# Right-associative exponentiation: 2 ** (3 ** 2) = 512.
krun solution.mpy --definition .verification-kompiled \
  -cOPS='ops(Op("**", Op("**", .Ops)))' \
  -cOPERANDS='ints(Num(2, Num(3, Num(2, .Ints))))' \
  | tee /dev/stderr | rg -Fq 'answer ( 512 )'

# Floor division before addition: 7 // 3 + 2 = 4.
krun solution.mpy --definition .verification-kompiled \
  -cOPS='ops(Op("//", Op("+", .Ops)))' \
  -cOPERANDS='ints(Num(7, Num(3, Num(2, .Ints))))' \
  | tee /dev/stderr | rg -Fq 'answer ( 4 )'

# A mixed case exercising every precedence level.
krun solution.mpy --definition .verification-kompiled \
  -cOPS='ops(Op("+", Op("**", Op("*", Op("-", Op("//", .Ops))))))' \
  -cOPERANDS='ints(Num(2, Num(3, Num(2, Num(4, Num(5, Num(2, .Ints)))))))' \
  | tee /dev/stderr | rg -Fq 'answer ( 36 )'

# Left associativity within one level: (20 // 3) // 2 = 3.
krun solution.mpy --definition .verification-kompiled \
  -cOPS='ops(Op("//", Op("//", .Ops)))' \
  -cOPERANDS='ints(Num(20, Num(3, Num(2, .Ints))))' \
  | tee /dev/stderr | rg -Fq 'answer ( 3 )'

# Required positive target proof: every claim in spec.k must close.
kprove spec.k --definition .verification-kompiled

# Discrimination probe: the deliberately false result claim must not close.
if kprove mutation-spec.k --definition .verification-kompiled; then
  echo 'ERROR: the deliberately false mutation proof unexpectedly closed' >&2
  exit 1
else
  echo 'Mutation proof failed as expected.'
fi
