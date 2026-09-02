requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY
  imports BOOL
  imports INT

  syntax Bool ::= simplePower(Int, Int) [function, total]

  rule simplePower(1, _N) => true

  rule simplePower(X, 0) => X ==Int 0
    requires X =/=Int 1

  rule simplePower(X, 1) => false
    requires X =/=Int 1

  rule simplePower(X, -1) => X ==Int -1
    requires X =/=Int 1

  rule simplePower(0, N) => false
    requires N <=Int -2 orBool N >=Int 2

  rule simplePower(X, N)
    => simplePower((X -Int pyMod(X, N)) /Int N, N)
    requires X =/=Int 0 andBool X =/=Int 1
     andBool (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) ==Int 0

  rule simplePower(X, N) => false
    requires X =/=Int 0 andBool X =/=Int 1
     andBool (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) =/=Int 0
endmodule
