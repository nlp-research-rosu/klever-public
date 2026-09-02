requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT

  // Definitional summaries for the two accumulators after executing the
  // source loop from counter I through N.  These equations name mathematical
  // values; they do not rewrite or bypass any MPY program computation.
  syntax Int ::= factorialAfter(Int, Int, Int) [function, total]
  rule factorialAfter(I:Int, N:Int, F:Int) => F
    requires I >Int N
  rule factorialAfter(I:Int, N:Int, F:Int)
    => factorialAfter(I +Int 1, N, F *Int I)
    requires I <=Int N

  syntax Int ::= productAfter(Int, Int, Int, Int) [function, total]
  rule productAfter(I:Int, N:Int, _F:Int, R:Int) => R
    requires I >Int N
  rule productAfter(I:Int, N:Int, F:Int, R:Int)
    => productAfter(I +Int 1, N, F *Int I, R *Int (F *Int I))
    requires I <=Int N
endmodule
