// verification.k — summary for the sum() fold proof (demonstrates the <k>-cell
// sum fold narrows a symbolic iterable, just like the for-loop invariants).

requires "../../../src/lemmas.k"

module SUM-FOLD-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val   // proof-only: a Val may sit in expression position (the symbolic list)

  // structural left-fold sum, matching the sumAcc/sumCont rules; Val head + cast
  // (the loop-break prefixSum pattern) so it reduces on a symbolic list.
  syntax Int ::= sumOf(ValSeq, Int) [function, total]
  rule sumOf(.ValSeq, ACC:Int)                => ACC [simplification]
  rule sumOf(vCons(V:Val, R:ValSeq), ACC:Int) => sumOf(R, ACC +Int projectIntTotal(V)) [simplification]
endmodule
