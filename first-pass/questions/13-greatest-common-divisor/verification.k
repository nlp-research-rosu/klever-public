requires "../../reference/src/lemmas.k"

module GCD-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof convenience
  syntax Expr ::= Val

  // Euclid: gcdF(A, 0) = A, else gcdF(B, A mod B) — the exact loop recurrence (floored pyMod)
  syntax Int ::= gcdF(Int, Int) [function, total]
  rule gcdF(A:Int, 0)      => A                          [simplification]
  rule gcdF(A:Int, B:Int)  => gcdF(B, pyMod(A, B))
    requires B =/=Int 0                                  [simplification]
endmodule
