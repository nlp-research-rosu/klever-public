requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL
  imports MAP
  imports LIST

  // Mathematical Euclidean GCD, normalized to a non-negative result.
  // The guards are disjoint and cover all integer second arguments.
  syntax Int ::= gcdEuclid(Int, Int) [function, total]
  rule gcdEuclid(A:Int, 0) => absInt(A) [simplification]
  rule gcdEuclid(A:Int, B:Int) => gcdEuclid(B, pyMod(A, B))
    requires B =/=Int 0
    [simplification]
endmodule
