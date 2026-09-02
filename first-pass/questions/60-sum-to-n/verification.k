// verification.k — summary for the sum_to_n proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module SUM-TO-N-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // sumRange(I, HI, ACC) = ACC + I + (I+1) + ... + (HI-1) — the value the reference's
  // <k>-cell sum fold (#sumAcc over rangeObj(I, HI, 1)) computes. For the entry
  // sum(range(N+1)) = #sumAcc(rangeObj(0, N+1, 1), 0), this is sumRange(0, N+1, 0) =
  // 0 + 1 + ... + N (the docstring spec). [total]: exhaustive on I >= HI / I < HI.
  syntax Int ::= sumRange(Int, Int, Int) [function, total]
  rule sumRange(I:Int, HI:Int, ACC:Int) => ACC                             requires I >=Int HI [simplification]
  rule sumRange(I:Int, HI:Int, ACC:Int) => sumRange(I +Int 1, HI, ACC +Int I) requires I <Int HI [simplification]
endmodule
