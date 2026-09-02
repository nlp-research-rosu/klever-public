requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports BOOL
  imports INT

  // Mathematical predicate for: there exists an exponent e >= 0 such that
  // N ^ e == X.  The degenerate bases are explicit.  For |N| >= 2, exact
  // division removes one factor; otherwise X is not a power of N.
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

  // Solver-facing consequences of the exhaustive equations above.
  // If no factor can be removed, only exponent zero (X == 1) remains.
  rule ((X ==Int 1) ==Bool simplePower(X, N)) => true
    requires (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) =/=Int 0
    [simplification]

  // On the loop's nonzero exact-divisibility domain, expose the defining
  // factor-removal equation in the operational X /Int N normal form.
  rule simplePower(X, N) => simplePower(X /Int N, N)
    requires X =/=Int 0
     andBool (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) ==Int 0
    [simplification]
endmodule
