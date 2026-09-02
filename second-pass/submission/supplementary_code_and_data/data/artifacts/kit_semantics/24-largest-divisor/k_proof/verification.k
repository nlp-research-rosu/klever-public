requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical specification of the first divisor encountered while
  // searching downward from D.  The proof only uses it for N >= 2 and D >= 1.
  syntax Int ::= largestDivisorAtOrBelow(Int, Int) [function]

  rule largestDivisorAtOrBelow(N, D) => D
    requires D >=Int 1
     andBool pyMod(N, D) ==Int 0

  rule largestDivisorAtOrBelow(N, D)
    => largestDivisorAtOrBelow(N, D -Int 1)
    requires D >Int 1
     andBool pyMod(N, D) =/=Int 0
endmodule
